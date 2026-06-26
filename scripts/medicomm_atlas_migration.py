import argparse
import base64
import csv
import json
import mimetypes
import os
import shutil
import time
import urllib.error
import urllib.request
import uuid
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
TRACKER = ROOT / "docs" / "medicomm-atlas-image-migration.csv"
BANK_FILES = [
    ROOT / "data" / "practice-question-bank.json",
    ROOT / "public" / "practice-question-bank.json",
    ROOT / "dist" / "practice-question-bank.json",
]
UPLOAD_DIRS = [
    ROOT / "public" / "uploads",
    ROOT / "runtime-data" / "uploads",
    ROOT / "data" / "uploads",
    ROOT / "dist" / "uploads",
]
GENERATED_DIR = ROOT / ".atlas-generated"
OPENAI_IMAGES_EDIT_URL = "https://api.openai.com/v1/images/edits"
ATLAS_PROMPT = """Create a professional medical atlas illustration from the provided source image.

Use a pure black (#000000) background. Preserve every anatomical structure, proportion, orientation,
spatial relationship, arrow, pointer line, and diagnostically important detail. Do not invent, remove,
or reposition anatomy. Render crisp, high-contrast, publication-quality textbook artwork.

If numbered labels exist, convert the numbers to Roman numerals inside teal circular markers while
retaining the original pointer lines. Marker text must be high contrast: use white or bright yellow
numerals inside dark green/teal markers, never dark numerals on dark markers. Preserve letter labels. If arrows exist without numbered labels,
preserve them and add no labels. If no arrows or labels exist, add none. Remove unrelated watermarks
and non-anatomical clutter. Preserve anatomically important text only when necessary. Add a small,
subtle light-gray "medicomm" watermark at about 20% opacity in the bottom-left corner.

The result must be a clean, scientifically faithful medical atlas image suitable for postgraduate
medical education. Output only the finished image."""


def read_tracker() -> list[dict]:
    with TRACKER.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def write_tracker(rows: list[dict]) -> None:
    if not rows:
        return
    with TRACKER.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def tracker_status() -> None:
    rows = read_tracker()
    counts = Counter(row["status"] for row in rows)
    print(f"total: {len(rows)}")
    for status, count in sorted(counts.items()):
        print(f"{status}: {count}")


def print_next(limit: int) -> None:
    rows = [row for row in read_tracker() if row["status"] != "done"]
    for row in rows[:limit]:
        print(
            "\t".join(
                [
                    row["questionId"],
                    row["imageSlot"],
                    row["sourceUrl"],
                    row["targetUrl"],
                ]
            )
        )


def find_row(question_id: str, image_slot: str) -> dict:
    for row in read_tracker():
        if row["questionId"] == question_id and row["imageSlot"] == str(image_slot):
            return row
    raise SystemExit(f"No tracker row for {question_id} slot {image_slot}")


def sync_generated_image(source_path: Path, target_url: str) -> str:
    if not source_path.exists():
        raise SystemExit(f"Generated file not found: {source_path}")
    target_name = Path(target_url).name
    for directory in UPLOAD_DIRS:
        directory.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, directory / target_name)
    return f"/uploads/{target_name}"


def update_bank(question_id: str, image_slot: int, source_url: str, target_url: str, note: str) -> None:
    index = image_slot - 1
    for bank_file in BANK_FILES:
        data = json.loads(bank_file.read_text(encoding="utf-8"))
        changed = False
        for subject in data.get("subjects", []):
            for question in subject.get("questions", []):
                if question.get("id") != question_id:
                    continue
                image_urls = list(question.get("imageUrls") or question.get("images") or [])
                if index >= len(image_urls):
                    raise SystemExit(f"{question_id} has no image slot {image_slot} in {bank_file}")
                source_urls = list(question.get("sourceImageUrls") or image_urls)
                while len(source_urls) < len(image_urls):
                    source_urls.append(image_urls[len(source_urls)])
                source_urls[index] = source_url
                image_urls[index] = target_url
                question["imageUrls"] = image_urls
                question["images"] = image_urls
                question["sourceImageUrls"] = source_urls
                question["assetNote"] = note
                changed = True
                break
            if changed:
                break
        if not changed:
            raise SystemExit(f"Question not found in {bank_file}: {question_id}")
        bank_file.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def mark_done(question_id: str, image_slot: str, source_url: str, target_url: str, note: str) -> None:
    rows = read_tracker()
    changed = False
    for row in rows:
        if row["questionId"] == question_id and row["imageSlot"] == str(image_slot):
            row["status"] = "done"
            row["sourceUrl"] = source_url
            row["targetUrl"] = target_url
            row["note"] = note
            changed = True
            break
    if not changed:
        raise SystemExit(f"No tracker row for {question_id} slot {image_slot}")
    write_tracker(rows)


def apply_generated(args: argparse.Namespace) -> None:
    row = find_row(args.question_id, args.image_slot)
    target_url = sync_generated_image(Path(args.generated_path), row["targetUrl"])
    note = args.note or (
        "Medicomm atlas-style educational schematic generated from the original source image; "
        "black background, source anatomy preserved."
    )
    update_bank(args.question_id, int(args.image_slot), row["sourceUrl"], target_url, note)
    mark_done(args.question_id, args.image_slot, row["sourceUrl"], target_url, note)
    print(target_url)


def source_path_for(row: dict) -> Path:
    relative = row["sourceUrl"].removeprefix("/")
    if relative.startswith("uploads/"):
        relative = relative.removeprefix("uploads/")
    path = ROOT / "public" / "uploads" / relative
    if not path.exists():
        raise FileNotFoundError(f"Source image not found: {path}")
    return path


def normalized_png(path: Path) -> tuple[bytes, str]:
    with Image.open(path) as opened:
        image = ImageOps.exif_transpose(opened).convert("RGB")
        width, height = image.size
        if width > height * 1.2:
            size = "1536x1024"
        elif height > width * 1.2:
            size = "1024x1536"
        else:
            size = "1024x1024"
        buffer = BytesIO()
        image.save(buffer, format="PNG", optimize=True)
        return buffer.getvalue(), size


def multipart_body(fields: dict[str, str], file_field: str, filename: str, content: bytes) -> tuple[bytes, str]:
    boundary = f"----medicomm-{uuid.uuid4().hex}"
    chunks: list[bytes] = []
    for name, value in fields.items():
        chunks.extend(
            [
                f"--{boundary}\r\n".encode(),
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode(),
                str(value).encode("utf-8"),
                b"\r\n",
            ]
        )
    content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    chunks.extend(
        [
            f"--{boundary}\r\n".encode(),
            f'Content-Disposition: form-data; name="{file_field}"; filename="{filename}"\r\n'.encode(),
            f"Content-Type: {content_type}\r\n\r\n".encode(),
            content,
            b"\r\n",
            f"--{boundary}--\r\n".encode(),
        ]
    )
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def generate_one(row: dict, api_key: str, model: str, quality: str, retries: int) -> tuple[dict, Path]:
    source_path = source_path_for(row)
    image_bytes, size = normalized_png(source_path)
    body, content_type = multipart_body(
        {
            "model": model,
            "prompt": ATLAS_PROMPT,
            "size": size,
            "quality": quality,
            "output_format": "png",
        },
        "image",
        source_path.with_suffix(".png").name,
        image_bytes,
    )
    request = urllib.request.Request(
        OPENAI_IMAGES_EDIT_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": content_type,
        },
        method="POST",
    )
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=300) as response:
                payload = json.load(response)
            encoded = payload["data"][0]["b64_json"]
            GENERATED_DIR.mkdir(parents=True, exist_ok=True)
            output_path = GENERATED_DIR / Path(row["targetUrl"]).name
            output_path.write_bytes(base64.b64decode(encoded))
            return row, output_path
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")
            if attempt >= retries or error.code not in {408, 409, 429, 500, 502, 503, 504}:
                raise RuntimeError(f"OpenAI API {error.code}: {detail[:1000]}") from error
        except (TimeoutError, urllib.error.URLError) as error:
            if attempt >= retries:
                raise RuntimeError(f"OpenAI request failed: {error}") from error
        time.sleep(2**attempt)
    raise RuntimeError("Image generation failed after retries")


def batch_generate(args: argparse.Namespace) -> None:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is not set in this process.")
    rows = [row for row in read_tracker() if row["status"] != "done"]
    if args.subject:
        rows = [row for row in rows if row["subjectId"] == args.subject]
    if args.limit:
        rows = rows[: args.limit]
    if not rows:
        print("No pending images matched.")
        return

    print(f"Generating {len(rows)} image(s) with {args.model}; workers={args.workers}")
    succeeded = 0
    failed = 0
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(generate_one, row, api_key, args.model, args.quality, args.retries): row
            for row in rows
        }
        for future in as_completed(futures):
            row = futures[future]
            try:
                completed_row, output_path = future.result()
                apply_generated(
                    argparse.Namespace(
                        question_id=completed_row["questionId"],
                        image_slot=completed_row["imageSlot"],
                        generated_path=str(output_path),
                        note=(
                            "Medicomm atlas-style educational image generated from the original source image "
                            "with the OpenAI Images API; black background, source anatomy preserved."
                        ),
                    )
                )
                succeeded += 1
                print(f"[{succeeded + failed}/{len(rows)}] done: {row['questionId']}")
            except Exception as error:
                failed += 1
                print(f"[{succeeded + failed}/{len(rows)}] FAILED {row['questionId']}: {error}")
    print(f"Batch complete: {succeeded} succeeded, {failed} failed")
    if failed:
        raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Medicomm atlas image migration helper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status")

    next_parser = subparsers.add_parser("next")
    next_parser.add_argument("--limit", type=int, default=10)

    apply_parser = subparsers.add_parser("apply")
    apply_parser.add_argument("--question-id", required=True)
    apply_parser.add_argument("--image-slot", default="1")
    apply_parser.add_argument("--generated-path", required=True)
    apply_parser.add_argument("--note", default="")

    batch_parser = subparsers.add_parser("batch", help="Generate and apply pending images with OpenAI")
    batch_parser.add_argument("--limit", type=int, default=0, help="Maximum images; 0 means all")
    batch_parser.add_argument("--subject", default="", help="Optional subject id filter")
    batch_parser.add_argument("--model", default="gpt-image-1.5")
    batch_parser.add_argument("--quality", choices=["low", "medium", "high"], default="high")
    batch_parser.add_argument("--workers", type=int, default=3)
    batch_parser.add_argument("--retries", type=int, default=3)

    args = parser.parse_args()
    if args.command == "status":
        tracker_status()
    elif args.command == "next":
        print_next(args.limit)
    elif args.command == "apply":
        apply_generated(args)
    elif args.command == "batch":
        batch_generate(args)


if __name__ == "__main__":
    main()
