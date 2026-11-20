# PDF to Markdown API — recipes for RAG, LLMs and AI agents

Convert any public PDF URL into **clean Markdown** (headings, paragraphs, detected tables), plain text or per-page JSON
with one HTTP call — no servers, no Python PDF libraries to install, pay only per page converted.

These recipes use the hosted **[PDF to Markdown, Text & Tables Extractor](https://apify.com/gunpark/pdf-to-markdown-extractor?utm_source=github&utm_medium=repo&utm_campaign=a1)**
on Apify (maintained by the author of this repo). New Apify accounts get free monthly credit, enough to convert
hundreds of pages before paying anything.

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

## 6. AI agents (MCP)

Add the Apify MCP server to Claude Desktop, Cursor or VS Code and ask:
*"Use gunpark/pdf-to-markdown-extractor to convert https://example.com/report.pdf to Markdown and summarize section 3."*

## Input reference

| Field | Default | Description |
|---|---|---|
| `pdfUrls` | – | List of public PDF URLs |
| `outputMode` | `markdown` | `markdown`, `text` or `json-pages` |
| `pageRange` | all | e.g. `"1-3,7"` |
| `maxPagesPerDocument` | 10 | Upper limit per PDF |
| `maxFileSizeMb` | 50 | Larger files are skipped |
| `timeoutSeconds` | 20 | Download timeout per file |

## Pricing

Pay per converted page (see the [pricing tab](https://apify.com/gunpark/pdf-to-markdown-extractor/pricing?utm_source=github&utm_medium=repo&utm_campaign=a1)).
Failed documents are not charged. Set "Max total charge" on a run to cap spend.

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
