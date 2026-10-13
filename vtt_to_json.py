import json
import re
from pathlib import Path

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def extract_vtt_text(content):
    ts = re.compile(
        r"\d{2}:\d{2}:\d{2}\.\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}\.\d{3}"
    )

    lines = []

    for line in content.splitlines():
        line = line.strip()

        if not line:
            continue

        if line == "WEBVTT":
            continue

        if ts.match(line):
            continue

        lines.append(line)

    return " ".join(lines)


for file_path in RAW_DIR.iterdir():

    if not file_path.is_file():
        continue

    content_type = None

    file_name = file_path.name.lower()

    if file_name.endswith(".txt"):
        content_type = "Chat"

    elif ".cc." in file_name:
        content_type = "ClosedCaptioning"

    elif ".transcript." in file_name:
        content_type = "Transcript"

    else:
        print(f"Skipping: {file_path.name}")
        continue

    with open(file_path, "r", encoding="utf-8") as f:
        raw_content = f.read()

    if file_path.suffix.lower() == ".vtt":
        content = extract_vtt_text(raw_content)
    else:
        content = raw_content

    data = {
        "id": "",

        "project": "Trust over IP",

        "organizational_unit": [
            "Ecosystem Governance Working Group"
        ],

        "date": "",

        "source_system": "Zoom",

        "asset_type": "Meeting",

        "content_type": content_type,

        "title": "Ecosystem Governance Working Group Meeting",

        "identifier": "",
        "identifier_type": "SAID",

        "source_url": "",

        "content": content,

        "collected_at": ""
    }

    output_file = PROCESSED_DIR / f"{file_path.stem}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Created {output_file}")