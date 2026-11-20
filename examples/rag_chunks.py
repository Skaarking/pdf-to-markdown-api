"""PDF URLs -> Markdown -> heading-aware chunks (JSON Lines) for any vector store.

Usage:  APIFY_TOKEN=... python rag_chunks.py <pdf-url> [...] > chunks.jsonl
Each line: {"source": url, "page": n, "heading": "...", "text": "..."}
"""
import json
import re
import sys

from pdf_to_markdown import convert

MAX_CHARS = 1500


def chunks(markdown, source):
    page, heading, buf = 1, "", []

    def flush():
        text = "\n".join(buf).strip()
        if text:
            for i in range(0, len(text), MAX_CHARS):
                yield {"source": source, "page": page, "heading": heading, "text": text[i:i + MAX_CHARS]}
        buf.clear()

    for line in markdown.splitlines():
        m = re.match(r"<!-- Page (\d+) -->", line)
        if m:
            yield from flush()
            page = int(m.group(1))
            continue
        if line.startswith("#"):
            yield from flush()
            heading = line.lstrip("#").strip()
            continue
        buf.append(line)
    yield from flush()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for doc in convert(sys.argv[1:], max_pages=50):
        for c in chunks(doc.get("markdown") or "", doc["url"]):
            print(json.dumps(c, ensure_ascii=False))
