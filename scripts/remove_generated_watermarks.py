"""Auditable, conservative cleanup of owned generated-illustration watermarks."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import sys
import math
import difflib
import html
from PIL import Image, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/watermark-removal'
UPLOADS = [ROOT / d / 'uploads' for d in ['public', 'data', 'runtime-data', 'dist']]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'ocr').mkdir(exist_ok=True)
    (OUT / 'inputs').mkdir(exist_ok=True)
    unique = {}
    for directory in UPLOADS:
        for p in sorted(directory.glob('medicomm*')):
            if p.suffix.lower() not in {'.png', '.jpg', '.jpeg', '.webp'}:
                continue
            h = digest(p)
            if h not in unique:
                with Image.open(p) as im:
                    width, height = im.size
                    # OCR copy only: enlarge small text, keep coordinates reversible.
                    scale = min(1, 3000 / max(width, height))
                    ocr_path = p
                    if scale < 1:
                        preview = im.convert('RGB').resize((round(width * scale), round(height * scale)))
                        ocr_path = OUT / 'inputs' / (h + '.png')
                        preview.save(ocr_path, compress_level=1)
                unique[h] = dict(hash=h, paths=[], width=width, height=height,
                                 scale=scale, ocrPath=str(ocr_path))
            unique[h]['paths'].append(str(p.relative_to(ROOT)))
    items = list(unique.values())
    (OUT / 'inventory.json').write_text(json.dumps(items, indent=2))
    print(f'{len(items)} unique raster images across {sum(len(x["paths"]) for x in items)} installed copies', flush=True)

def svg_cleanup():
    pattern = re.compile(r'<text\b[^>]*>\s*(?:medicomm|medulla)\s*</text>', re.I)
    changes = []
    for directory in UPLOADS:
        for p in directory.glob('medicomm*.svg'):
            raw = p.read_bytes()
            text = raw.decode('utf-8')
            updated, count = pattern.subn('', text)
            if not count:
                continue
            backup = OUT / 'backups' / p.relative_to(ROOT)
            backup.parent.mkdir(parents=True, exist_ok=True)
            if not backup.exists():
                backup.write_bytes(raw)
            p.write_bytes(updated.encode('utf-8'))
            changes.append(dict(path=str(p.relative_to(ROOT)), removed=count, before=hashlib.sha256(raw).hexdigest(), after=digest(p)))
    (OUT / 'svg-manifest.json').write_text(json.dumps(changes, indent=2))
    print(f'Removed watermark text from {len(changes)} SVG copies')

def matches_brand(text):
    text = re.sub('[^a-z]', '', text.lower())
    return difflib.SequenceMatcher(None, text, 'medicomm').ratio() >= .72

def enhance():
    items = json.loads((OUT / 'inventory.json').read_text())
    (OUT / 'ocr2').mkdir(exist_ok=True)
    (OUT / 'enhanced').mkdir(exist_ok=True)
    enhanced=[]
    for item in items:
        with Image.open(ROOT / item['paths'][0]) as im:
            y = int(im.height*.75)
            crop = im.convert('L').crop((0,y,int(im.width*.6),im.height))
            crop = crop.point([round(255*(v/255)**.35) for v in range(256)])
            crop = ImageOps.invert(crop).resize((crop.width*2,crop.height*2))
            path=OUT/'enhanced'/(item['hash']+'.png')
            crop.save(path,compress_level=1)
        enhanced.append(dict(hash=item['hash'],ocrPath=str(path),scale=2,offsetY=y))
    (OUT/'enhanced.json').write_text(json.dumps(enhanced,indent=2))
    print('Prepared',len(enhanced),'enhanced watermark crops')

def audit():
    items = json.loads((OUT / 'inventory.json').read_text())
    results = []
    for item in items:
        path = OUT / 'ocr' / (item['hash'] + '.json')
        if not path.exists():
            continue
        lines = json.loads(path.read_text(encoding='utf-8-sig')) or []
        if isinstance(lines, dict): lines = [lines]
        for line in lines:
            line['scale']=item['scale']; line['offsetY']=0
        extra=OUT/'ocr2'/(item['hash']+'.json')
        if extra.exists():
            supplemental=json.loads(extra.read_text(encoding='utf-8-sig')) or []
            if isinstance(supplemental,dict): supplemental=[supplemental]
            for line in supplemental:
                line['scale']=2; line['offsetY']=int(item['height']*.75)
            lines+=supplemental
        boxes = []
        for line in lines:
            words = line['words']
            candidates = [[w] for w in words]
            candidates += [words[i:i+2] for i in range(len(words)-1)]
            for group in candidates:
                text = ''.join(w['text'] for w in group)
                if not matches_brand(text): continue
                x = min(w['x'] for w in group) / line['scale']
                y = min(w['y'] for w in group) / line['scale'] + line['offsetY']
                r = max(w['x']+w['width'] for w in group) / line['scale']
                b = max(w['y']+w['height'] for w in group) / line['scale'] + line['offsetY']
                # Only margin branding can be automatically removed.
                if y < item['height'] * .75: continue
                box = [max(0, math.floor(x)-4), max(0, math.floor(y)-4), min(item['width'], math.ceil(r)+4), min(item['height'], math.ceil(b)+4)]
                if not any(box[0] >= old['box'][0] and box[1] >= old['box'][1] and box[2] <= old['box'][2] and box[3] <= old['box'][3] for old in boxes):
                    boxes.append(dict(text=text, box=box))
        merged=[]
        for candidate in boxes:
            x,y,r,b=candidate['box']
            for old in merged:
                ox,oy,orr,ob=old['box']
                if x < orr and ox < r and y < ob and oy < b:
                    old['box']=[min(x,ox),min(y,oy),max(r,orr),max(b,ob)]
                    break
            else:
                merged.append(candidate)
        boxes=merged
        with Image.open(ROOT / item['paths'][0]) as source:
            im = source.convert('RGB')
            for candidate in boxes:
                x,y,r,b = candidate['box']
                ring = list(im.crop((x,y,r,min(y+3,b))).getdata()) + list(im.crop((x,max(y,b-3),r,b)).getdata())
                ring += list(im.crop((x,y,min(x+3,r),b)).getdata()) + list(im.crop((max(x,r-3),y,r,b)).getdata())
                bg = Counter(ring).most_common(1)[0][0]
                near = sum(max(abs(v[i]-bg[i]) for i in range(3)) <= 8 for v in ring)/len(ring)
                candidate.update(background=list(bg), borderAgreement=round(near,4), safe=near >= .99)
        results.append(dict(**item, boxes=boxes, status='detected' if boxes else 'needs-review'))
    (OUT / 'audit.json').write_text(json.dumps(results, indent=2))
    print(Counter(x['status'] for x in results))
    print('Safe boxes:',sum(b['safe'] for x in results for b in x['boxes']))
    for kind in ['detected','needs-review']:
        selected = [x for x in results if x['status'] == kind]
        for offset in range(0,len(selected),40):
            sheet = Image.new('RGB',(1500,1200),'#303030')
            draw = ImageDraw.Draw(sheet)
            for index,item in enumerate(selected[offset:offset+40]):
                with Image.open(ROOT / item['paths'][0]) as im:
                    # Bottom-left to bottom-right strip, with useful surrounding context.
                    crop = im.convert('RGB').crop((0, int(im.height*.82), im.width, im.height))
                    crop.thumbnail((370,90))
                    x=(index%4)*375; y=(index//4)*120
                    sheet.paste(crop,(x,y+22))
                    label=f'{offset+index}: {Path(item["paths"][0]).stem.replace("medicomm-","")}'
                    draw.text((x+2,y+2),label[:52], fill='white')
            sheet.save(OUT / f'{kind}-{offset//40:02}.jpg', quality=90)

def apply_rasters():
    results=json.loads((OUT/'audit.json').read_text())
    changes=[]; flagged=[]
    for item in results:
        safe=[b for b in item['boxes'] if b['safe']]
        unsafe=[b for b in item['boxes'] if not b['safe']]
        if not safe or unsafe:
            flagged.append(dict(paths=item['paths'],hash=item['hash'],reason='Watermark overlaps content or nonuniform background' if unsafe else 'No confidently detected watermark'))
        if not safe: continue
        source=ROOT/item['paths'][0]
        # Keep JPEGs untouched: recompression would change pixels outside the edit.
        if source.suffix.lower() in {'.jpg','.jpeg'}:
            flagged.append(dict(paths=item['paths'],hash=item['hash'],reason='JPEG requires lossless replacement workflow'))
            continue
        original=source.read_bytes()
        with Image.open(source) as im:
            before=im.convert('RGBA')
            after=before.copy()
            draw=ImageDraw.Draw(after)
            for box in safe:
                x,y,r,b=box['box']
                draw.rectangle((x,y,r-1,b-1),fill=tuple(box['background'])+(255,))
            # Prove that every pixel outside the explicitly audited boxes is unchanged.
            restored=after.copy()
            for box in safe:
                bounds=tuple(box['box'])
                restored.paste(before.crop(bounds),bounds)
            assert restored.tobytes()==before.tobytes(),source
            dest=OUT/'cleaned'/source.name
            dest.parent.mkdir(exist_ok=True)
            if im.mode=='RGB': after=after.convert('RGB')
            after.save(dest,format='PNG',compress_level=3)
        clean=dest.read_bytes()
        for rel in item['paths']:
            p=ROOT/rel
            assert digest(p)==item['hash'],f'Source changed during audit: {p}'
            backup=OUT/'backups'/rel
            backup.parent.mkdir(parents=True,exist_ok=True)
            if not backup.exists(): backup.write_bytes(original)
            p.write_bytes(clean)
        changes.append(dict(paths=item['paths'],before=item['hash'],after=hashlib.sha256(clean).hexdigest(),boxes=safe,pixelsOutsideBoxesUnchanged=True))
        if len(changes)%50==0: print('Cleaned',len(changes),'unique images',flush=True)
    (OUT/'raster-manifest.json').write_text(json.dumps(changes,indent=2))
    (OUT/'flagged.json').write_text(json.dumps(flagged,indent=2))
    print('Cleaned',len(changes),'unique rasters;',len(flagged),'flagged')

def report():
    changes=json.loads((OUT/'raster-manifest.json').read_text())
    flagged=json.loads((OUT/'flagged.json').read_text())
    svgs=json.loads((OUT/'svg-manifest.json').read_text())
    audit=json.loads((OUT/'audit.json').read_text())
    by_hash={x['hash']:x for x in audit}
    changed_hashes={x['before'] for x in changes}
    summary=dict(rasterImagesEdited=len(changes),rasterCopiesEdited=sum(len(x['paths']) for x in changes),
                 svgFilesEdited=len({Path(x['path']).name for x in svgs}),svgCopiesEdited=len(svgs),
                 imagesFlagged=len({x['hash'] for x in flagged}),outsideEditPixelsVerified=True)
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2))
    cards=[]
    for item in flagged:
        path=Path(item['paths'][0])
        state='Safe margin watermark removed; additional review needed.' if item['hash'] in changed_hashes else 'Unchanged pending review.'
        cards.append(f'<article><h2>{html.escape(path.name)}</h2><p>{html.escape(item["reason"])}. {state}</p><a href="../../{path.as_posix()}"><img loading="lazy" src="../../{path.as_posix()}" alt="Image requiring watermark review"></a></article>')
    content='<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Watermark removal review</title><style>body{background:#111827;color:#e5e7eb;font:15px system-ui;margin:24px}h2{font-size:14px;overflow-wrap:anywhere}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(350px,1fr));gap:20px}article{padding:16px;background:#1f2937;border-radius:12px}img{width:100%;max-height:500px;object-fit:contain;background:#000}p{line-height:1.5}</style>'
    content+=f'<h1>Watermark removal review</h1><p>{summary["rasterImagesEdited"]} distinct raster images and {summary["svgFilesEdited"]} SVG filenames cleaned. {summary["imagesFlagged"]} images flagged for review. Some flagged images had their safe margin watermark removed, but still contain another mark over medical content. Existing image paths were preserved. Backups and per-file hashes are saved beside this report.</p><div class="grid">'+''.join(cards)+'</div>'
    (OUT/'review.html').write_text(content,encoding='utf-8')
    # A compact before/after sheet from the installed results.
    selected=changes[::max(1,len(changes)//12)][:12]
    sheet=Image.new('RGB',(1200,120*len(selected)),'#303030')
    draw=ImageDraw.Draw(sheet)
    for row,item in enumerate(selected):
        rel=Path(item['paths'][0])
        for col,path in enumerate([OUT/'backups'/rel,ROOT/rel]):
            with Image.open(path) as im:
                crop=im.convert('RGB').crop((0,int(im.height*.87),im.width,im.height))
                crop.thumbnail((590,90))
                sheet.paste(crop,(col*600,row*120+24))
            draw.text((col*600+4,row*120+4),('Before: ' if col==0 else 'After: ')+rel.stem[:70],fill='white')
    sheet.save(OUT/'before-after.jpg',quality=93)
    print(json.dumps(summary))

def verify():
    manifests=[json.loads((OUT/name).read_text()) for name in ['raster-manifest.json','svg-manifest.json']]
    checked=0
    for rows in manifests:
        for item in rows:
            for rel in item.get('paths',[item.get('path')]):
                assert digest(ROOT/rel)==item['after'],f'Installed file differs from manifest: {rel}'
                checked+=1
    print('Verified hashes of',checked,'installed files')
    items=json.loads((OUT/'audit.json').read_text())
    edited={x['before'] for x in manifests[0]}
    (OUT/'post-ocr').mkdir(exist_ok=True)
    check=[]
    for item in items:
        if item['hash'] in edited:
            check.append(dict(hash=item['hash'],ocrPath=str(ROOT/item['paths'][0])))
    (OUT/'post-check.json').write_text(json.dumps(check,indent=2))


if __name__ == '__main__':
    {'inventory': inventory, 'svg': svg_cleanup, 'audit': audit, 'enhance': enhance, 'apply': apply_rasters, 'report': report, 'verify': verify}[sys.argv[1]]()
