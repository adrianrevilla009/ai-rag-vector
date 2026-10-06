# ingestion-pipeline

`ingest.py` loads two Orders documents, chunks, embeds and upserts them into an in-memory SQLite database, skipping unchanged documents.

## Goal

Show the shape of a re-runnable ingestion pipeline: a content hash decides whether a document is skipped or re-ingested, and a changed document has its old chunks deleted first. SQLite stands in for a vector store so it runs anywhere; the same steps apply to the stores in this repo.

## Run it

```bash
python3 ingest.py
```

Expected output:

```
{'ingested': 2, 'skipped': 0} {'ingested': 0, 'skipped': 2} {'ingested': 1, 'skipped': 1} chunks=5
OK
```

## What it proves

- Idempotency: the second run over unchanged input ingests nothing and skips both documents.
- After `refunds.md` gains a paragraph, only that document is re-ingested and the other is skipped.
- Old chunks are deleted before new ones are inserted, so the table ends with 5 chunks (3 for `refunds.md`, 2 for `shipping.md`) and no stale rows.

## Trade-offs

- Hashing whole documents re-embeds everything in a changed document; per-chunk hashes would save embedding cost but add bookkeeping.
- Documents removed from the source are not deleted from the store; a real pipeline needs a sweep for orphans.
- Embeddings are stored as JSON text with a 32-bucket hashing embedding, which is fine for a demo and not for search at scale.

## When not to use it

- For large or streaming corpora, use an orchestrator with batching, retries and a dead-letter queue instead of a single loop.
