# chunking-embeddings

Three chunking strategies over one short Orders document, with a toy hashing embedding and cosine search in `chunk.py`.

## Goal

Compare fixed-size, sentence-window and paragraph chunking, and show how a chunk becomes a vector. The embedding is a deterministic hashing bag-of-words, so the lab runs offline; in practice you would replace `embed()` with a real model.

## Run it

```bash
python3 chunk.py
```

Expected output:

```
fixed      chunks= 4 avg_len=119 best='rtial refunds are not supported in v1.\n\nShipping s'
sentences  chunks= 5 avg_len= 76 best='Refunds are allowed within 30 days. A refund moves'
paragraphs chunks= 3 avg_len=128 best='Refunds are allowed within 30 days. A refund moves'
OK
```

## What it proves

- The strategy changes the chunk count (4, 5 or 3) and size for the same text.
- Fixed 120-character windows cut mid-word: the best fixed chunk for "how do refunds work" starts at `rtial refunds` and drags in the start of the shipping paragraph.
- Sentence and paragraph chunking both return the refund passage; `chunk.py` asserts that the best paragraph contains "refund".

## Trade-offs

- Small chunks give precise hits but lose context; large chunks keep context but dilute the vector.
- Overlap (30 characters here) softens boundary loss at the cost of more storage and duplicate hits.
- The hashing embedding has no semantics: it only matches shared words, and 64 buckets means collisions.

## When not to use it

- For real retrieval quality, use a trained embedding model and a tokenizer-aware splitter; this only teaches the mechanics.
