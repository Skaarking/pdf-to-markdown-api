"""Convert PDF URLs to Markdown with the hosted Apify extractor. Standard library only.

Usage:  APIFY_TOKEN=... python pdf_to_markdown.py <pdf-url> [<pdf-url> ...] > out.md
"""
import json
import os
import sys
import urllib.request

ACTOR = "gunpark~pdf-to-markdown-extractor"


def convert(urls, output_mode="markdown", max_pages=10, page_range=""):
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("Set the APIFY_TOKEN environment variable (Apify Console -> Settings -> API & Integrations).")
    body = {"pdfUrls": urls, "outputMode": output_mode, "maxPagesPerDocument": max_pages, "pageRange": page_range}
    req = urllib.request.Request(
        f"https://api.apify.com/v2/acts/{ACTOR}/run-sync-get-dataset-items",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for doc in convert(sys.argv[1:]):
        for w in doc.get("warnings") or []:
            print(f"warning: {w}", file=sys.stderr)
        print(doc.get("markdown") or doc.get("text") or "")
