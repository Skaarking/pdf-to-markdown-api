// Convert PDF URLs to Markdown with the hosted Apify extractor (Node 18+, no dependencies).
// Usage: APIFY_TOKEN=... node pdf-to-markdown.mjs <pdf-url> [<pdf-url> ...] > out.md
const token = process.env.APIFY_TOKEN;
const urls = process.argv.slice(2);
if (!token) throw new Error('Set APIFY_TOKEN (Apify Console -> Settings -> API & Integrations).');
if (urls.length === 0) throw new Error('Pass at least one PDF URL.');

const res = await fetch('https://api.apify.com/v2/acts/gunpark~pdf-to-markdown-extractor/run-sync-get-dataset-items', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({ pdfUrls: urls, outputMode: 'markdown', maxPagesPerDocument: 10 }),
});
if (!res.ok) throw new Error(`Apify API error ${res.status}: ${await res.text()}`);
for (const doc of await res.json()) {
    for (const w of doc.warnings ?? []) console.error(`warning: ${w}`);
    console.log(doc.markdown ?? doc.text ?? '');
}
