"""Import theory prompts from New Bhalani.pdf, retaining page and source text.
Requires PyMuPDF. Glyph advances repair missing PDF space mappings.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[1]
TOPICS = {
 'HNF': 'Head, Neck & Face', 'UpperLimb': 'Upper Limb', 'Thorax': 'Thorax',
 'Neuroanatomy': 'Neuroanatomy', 'Abdomen&Pelvis': 'Abdomen & Pelvis',
 'LowerLimb': 'Lower Limb', 'GeneralAnatomy': 'General Anatomy',
 'Histology-Diagramsonly': 'Histology', 'Embryology': 'Embryology', 'Genetics': 'Genetics',
 'CVS-': 'Cardiovascular System', 'GIT-': 'Gastrointestinal System',
 'EndocrineSystem-': 'Endocrine System', 'ReproductiveSystem-': 'Reproductive System',
 'RSandTempregulations-': 'Respiration & Temperature Regulation', 'CNS-': 'Central Nervous System',
 'RenalPhysiology-': 'Renal Physiology', 'SpecialSenses': 'Special Senses',
 'Nerve-': 'Nerve & Muscle', 'Blood--': 'Blood', 'GeneralPhysiology-': 'General Physiology',
 'ProteinMetabolism': 'Protein Metabolism', 'NucleotideMetabolism': 'Nucleotide Metabolism',
 'Hemoglobin': 'Hemoglobin', 'Vitamins': 'Vitamins', 'Enzymes': 'Enzymes',
 'BiologicalOxidation': 'Biological Oxidation', 'MolecularBiology': 'Molecular Biology',
 'Proteins': 'Proteins', 'Nucleotides': 'Nucleotides', 'FreeRadicalsandAntioxidants': 'Free Radicals & Antioxidants',
 'Nutrition': 'Nutrition', 'PlasmaProteins': 'Plasma Proteins',
 'CarbohydrateMetabolism': 'Carbohydrate Metabolism', 'LipidMetabolism': 'Lipid Metabolism',
 'MineralMetabolism': 'Mineral Metabolism', 'IntegrationofMetabolism': 'Integration of Metabolism',
 'Acid-BaseBalance': 'Acid-Base Balance', 'Insulin,GlucoseHomeostasisandDM': 'Insulin, Glucose Homeostasis & Diabetes',
 'OrganFunctionTests': 'Organ Function Tests', 'Carbohydrates': 'Carbohydrates', 'Lipid': 'Lipids',
 'DigestionandAbsorption': 'Digestion & Absorption', 'Hormones': 'Hormones', 'Cancer': 'Cancer',
 'Detoxification': 'Detoxification', 'LCD': 'Laboratory Techniques',
 'OverviewofBiophysicalChemistry': 'Biophysical Chemistry',
}

def slug(value):
 return re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')

def page_lines(doc, page):
 font = fitz.Font(fontbuffer=doc.extract_font(page.get_fonts()[0][0])[3])
 for block in page.get_text('rawdict')['blocks']:
  for line in block.get('lines', []):
   text, previous = '', None
   for span in line['spans']:
    for char in span['chars']:
     x = char['origin'][0]
     if previous and x - previous[0] - previous[1] > 1.3:
      text += ' '
     text += char['c']
     previous = (x, font.glyph_advance(ord(char['c'])) * span['size'])
   if text.strip(): yield text.strip()

def clean(text):
 text = re.sub(r"[\ufffd'\u2019]\s*s\b", "'s", text)
 text = text.replace('\ufffd', ' - ')
 text = re.sub(r'\*+', '', text)
 text = re.sub(r'\s+([,;:)])', r'\1', text)
 text = re.sub(r'([,;])(?=\S)', r'\1 ', text)
 text = re.sub(r'\(\s+', '(', text)
 text = re.sub(r'\s+', ' ', text).strip()
 # Obvious spelling errors in the source; sourceText remains untouched for audit.
 corrections = {
  'Duralw venous': 'Dural venous', 'Deloid': 'Deltoid', 'nuerovascular': 'neurovascular',
  'intercoastal space': 'intercostal space', 'syndorme': 'syndrome', 'Contrictions': 'Constrictions',
  'Third ventrical': 'Third ventricle', 'Occulomotor': 'Oculomotor', 'Ascending tracks': 'Ascending tracts',
  'Descending tracks': 'Descending tracts', 'Hysterosalphingography': 'Hysterosalpingography',
  'serious and mucous acini': 'serous and mucous acini', 'Notocord': 'Notochord',
  'pounches': 'pouches', 'Setal defects': 'Septal defects', 'Developmental detects': 'Developmental defects',
  'Remenants': 'Remnants', 'Milleu Interior': 'Milieu Interior', 'Properties of Never Fibres': 'Properties of Nerve Fibres',
  'Complete Transaction of Spinal Cord': 'Complete Transection of Spinal Cord',
 }
 for source, corrected in corrections.items(): text = text.replace(source, corrected)
 return text

def extract(pdf):
 doc = fitz.open(pdf)
 subjects, current, topic, kind, pending = [], None, None, None, None
 audit_lines=[]
 def flush():
  nonlocal pending
  if not pending: return
  raw=' '.join(pending.pop('lines'))
  stars=max([len(m) for m in re.findall(r'\*+',raw)] or [0])
  pending.update(prompt=clean(raw), sourceText=raw, emphasis=stars)
  if topic['title'] == 'Histology': pending['prompt'] = 'Draw a labelled diagram: ' + pending['prompt']
  # This repeated "1." is a wrapped subpart, not a separate source question.
  if topic['title']=='Biological Oxidation' and kind=='long-answer' and topic['questions'] and topic['questions'][-1]['sourceText'].endswith('Sites of'):
   previous=topic['questions'][-1]
   previous['sourceText'] += ' ' + raw
   previous['prompt']=clean(previous['sourceText'])
   previous['emphasis']=max(previous['emphasis'],stars)
  else:
   pending['id']=f"bhalani-{current['id']}-{topic['id']}-{len(topic['questions'])+1:03d}"
   topic['questions'].append(pending)
  pending=None
 for page_num,page in enumerate(doc,1):
  for line in page_lines(doc,page):
   audit_lines.append(f'{page_num:02d} {line}')
   compact=re.sub(r'\s+','',line)
   if compact in ('ANATOMY','PHYSIOLOGY','BIOCHEMISTRY'):
    flush(); current={'id':compact.lower(),'title':compact.title(),'topics':[]};subjects.append(current);topic=None;kind=None;continue
   topic_title=next((v for k,v in TOPICS.items() if (compact.startswith(k) if k.endswith('-') else compact==k)),None)
   if topic_title:
    flush();topic={'id':slug(topic_title),'title':topic_title,'questions':[]};current['topics'].append(topic)
    kind='short-note' if topic_title in ('General Anatomy','Histology','Embryology','Genetics') else None
    continue
   if compact in ('SN','LAQ'):
    flush();kind='short-note' if compact=='SN' else 'long-answer';continue
   if compact.startswith(('Vivaandpractical','Practical','Coursesandbranches','inLAQsoforgans','Smallbranches')):
    flush();kind=None;continue
   if compact.startswith('Paper'):flush();kind=None;continue
   if not topic or not kind:continue
   match=re.match(r'^(\d+)\.\s*(.*)',line)
   if match:
    flush();pending={'sourceNumber':match[1],'kind':kind,'sourcePage':page_num,'lines':[match[2]]}
   elif compact.startswith('Vit-') and topic['title']=='Vitamins':
    flush();pending={'sourceNumber':None,'kind':kind,'sourcePage':page_num,'lines':[line]}
   elif pending:pending['lines'].append(line)
 flush()
 for subject in subjects:
  for topic in subject['topics']:
   if not topic['questions']:raise ValueError(f"Empty topic: {subject['id']}/{topic['id']}")
 questions=[q for s in subjects for t in s['topics'] for q in t['questions']]
 assert len({q['id'] for q in questions})==len(questions)
 assert all(q['prompt'] and '\ufffd' not in q['prompt'] for q in questions)
 data={'version':1,'source':{'title':'New Bhalani','fileName':pdf.name,'pageCount':len(doc),'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest()},'questionCount':len(questions),'subjects':subjects}
 return data,audit_lines

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('pdf',nargs='?',default=r'F:\shortnotes\New Bhalani.pdf');args=parser.parse_args()
 data,lines=extract(Path(args.pdf))
 out=ROOT/'public'/'short-notes.json';out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 audit=ROOT/'output'/'short-notes';audit.mkdir(parents=True,exist_ok=True)
 (audit/'extracted-lines.txt').write_text('\n'.join(lines),encoding='utf-8')
 (audit/'question-audit.txt').write_text('\n'.join(f"{s['title']} / {t['title']} / {q['kind']} / p{q['sourcePage']}: {q['prompt']}" for s in data['subjects'] for t in s['topics'] for q in t['questions']),encoding='utf-8')
 print(json.dumps({'questions':data['questionCount'],'subjects':[{ 'title':s['title'],'topics':len(s['topics']),'questions':sum(len(t['questions']) for t in s['topics'])} for s in data['subjects']]}))
