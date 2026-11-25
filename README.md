# PDF to Markdown API — recipes for RAG, LLMs and AI agents

Convert public **text-layer** PDF URLs into Markdown (headings, paragraphs, tables), plain text or per-page JSON with one
HTTP call — no servers or PDF libraries to install. **Flat $0.003 per PDF** (any length up to 500 pages), no start fee;
image-only, empty and failed documents are free. Scanned pages are not OCR'd.

**Typical job:** every week, convert the newly published reports, filings or papers on your list into page-referenced
Markdown for your RAG index (schedule the run in Apify and pass the new URLs).

## Real outputs (public-domain US government documents)

| Document | Pages | Text pages | Tables found | Output |
|---|---:|---:|---:|---|
| Census "New Residential Construction" (table-heavy) | 7 | 7 | 31 | [Markdown](examples/real-outputs/census-new-residential-construction.md) · [JSON](examples/real-outputs/census-new-residential-construction.json) |
| FEC filing (mixed text + scanned pages) | 68 | 52 | 32 | [Markdown](examples/real-outputs/fec-filing-mixed-scanned.md) · [JSON](examples/real-outputs/fec-filing-mixed-scanned.json) |
| DOE/NETL semi-annual report (long) | 180 | 179 | 85 | [Markdown](examples/real-outputs/doe-netl-report-180-pages.md) · [JSON](examples/real-outputs/doe-netl-report-180-pages.json) |

Each of these cost **$0.003** to convert. Measured on 2026-11-20 against `pdftotext` as an independent reference, word
recall was 0.999 (Census) and 0.951 (FEC) — on par with the most-used PDF Actor on Apify Store, which charges a $0.005
start fee plus $0.005 per PDF (Free-tier list prices; paid tiers differ). Benchmark method and raw numbers are in
the project's records; these are three documents, not a general accuracy claim.

These recipes use the hosted **[PDF to Markdown, Text & Tables Extractor](https://apify.com/gunpark/pdf-to-markdown-extractor?utm_source=github&utm_medium=repo&utm_campaign=a1)**
on Apify (maintained by the author of this repo). Apify's Free plan includes $5 of monthly usage credit; how many
conversions that covers depends on your remaining credit and the run charges.

- Markdown output with `#` headings and GitHub-style tables, ready for chunking
- Page ranges (`"1-5,9"`) and a max-pages limit to control cost
- Metadata: title, author, page count, per-page text
- Works from curl, Python, JavaScript, Make, Zapier, n8n and the Apify MCP server (Claude, Cursor, etc.)
- Text-layer PDFs only (no OCR of scanned images)

## 1. Get a token

Create a free account at [apify.com](https://apify.com?utm_source=github&utm_medium=repo&utm_campaign=a1) and copy your API token from
*Console → Settings → API & Integrations*. Export it:

```bash
export APIFY_TOKEN=your_token_here
```

## 2. curl (one call, waits for the result)

```bash
curl -s -X POST \
  "https://api.apify.com/v2/acts/gunpark~pdf-to-markdown-extractor/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"pdfUrls":["https://arxiv.org/pdf/1706.03762"],"outputMode":"markdown","maxPagesPerDocument":5}' \
  | jq -r '.[0].markdown'
```

The response is a JSON array with one item per PDF:

```json
[{
  "url": "https://arxiv.org/pdf/1706.03762",
  "author": "...",
  "pageCount": 15,
  "processedPageCount": 5,
  "outputMode": "markdown",
  "markdown": "<!-- Page 1 -->\n\n## Attention Is All You Need\n\n| Ashish Vaswani | Noam Shazeer | ...",
  "tables": [{ "pageNumber": 1, "rows": [["Ashish Vaswani", "Noam Shazeer"], ["Google Brain", "Google Brain"]] }],
  "warnings": []
}]
```

## 3. Python

See [`examples/pdf_to_markdown.py`](examples/pdf_to_markdown.py) (standard library only):

```bash
python examples/pdf_to_markdown.py https://arxiv.org/pdf/1706.03762 > paper.md
```

## 4. JavaScript / Node 18+

See [`examples/pdf-to-markdown.mjs`](examples/pdf-to-markdown.mjs):

```bash
node examples/pdf-to-markdown.mjs https://arxiv.org/pdf/1706.03762 > paper.md
```

## 5. RAG: PDF → Markdown → chunks for your vector store

[`examples/rag_chunks.py`](examples/rag_chunks.py) converts PDFs and splits the Markdown by headings into
chunks with source/page metadata — paste the output into LangChain, LlamaIndex or any vector database.

```bash
python examples/rag_chunks.py https://arxiv.org/pdf/1706.03762 > chunks.jsonl
```

## 6. AI agents (MCP): PDF and image text extraction as agent tools

Both tools are available to MCP clients (Claude Desktop, Cursor, VS Code, etc.) through Apify's hosted MCP server.
Each user signs in with their own Apify account (OAuth) or an Apify API token; usage is billed to that account
(flat $0.003 per PDF with text, $0.003 per image with text; failed and empty inputs are free).

```json
{
  "mcpServers": {
    "pdf-and-image-to-text": {
      "url": "https://mcp.apify.com/?tools=gunpark/pdf-to-markdown-extractor,gunpark/bulk-image-ocr"
    }
  }
}
```

Then ask your agent, for example: *"Convert https://arxiv.org/pdf/1706.03762 to Markdown and list the section headings"*
or *"Read the text in these receipt images"*. Text-layer PDFs only (scanned PDFs are not OCR'd); OCR supports
English and Spanish images.

## Input reference

| Field | Default | Description |
|---|---|---|
| `pdfUrls` | – | List of public PDF URLs |
| `outputMode` | `markdown` | `markdown`, `text` or `json-pages` |
| `pageRange` | all | e.g. `"1-3,7"` |
| `maxPagesPerDocument` | 200 | Upper limit per PDF (max 500); longer PDFs are flagged `truncatedByPageLimit` |
| `maxFileSizeMb` | 50 | Larger files are skipped |
| `timeoutSeconds` | 20 | Download timeout per file |

## Pricing

Flat $0.003 per PDF that yields text; image-only, empty and failed documents are free (see the [pricing tab](https://apify.com/gunpark/pdf-to-markdown-extractor/pricing?utm_source=github&utm_medium=repo&utm_campaign=a1)).
Download or parsing failures are not charged. Set "Max total charge" on a run to cap spend.

## Also useful: bulk image conversion

Convert/compress images (PNG/JPEG → WebP/AVIF) by URL with the
[Bulk Image Converter & Compressor](https://apify.com/gunpark/image-converter-compressor?utm_source=github&utm_medium=repo&utm_campaign=a1):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/gunpark~image-converter-compressor/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"imageUrls":["https://raw.githubusercontent.com/github/explore/main/topics/python/python.png"],"targetFormat":"webp","quality":80}' \
  | jq '.[0] | {publicUrl, sizeBefore, sizeAfter, savingsPercent}'
```

## License

The example code in this repository is MIT licensed. The hosted extractor is a paid service operated on Apify.
