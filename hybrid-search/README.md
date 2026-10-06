# hybrid-search

BM25 and a hashing-vector ranking over five Orders snippets, fused with Reciprocal Rank Fusion in `hybrid.py`.

## Goal

Show how lexical and vector rankings are combined with RRF. Everything is plain Python so the fusion logic is visible; in a real stack the two rankings would come from a search engine or from Postgres full-text plus a vector index. The "embedding" is a hashing trick with a tiny synonym map (`money`, `back`, `returned` map to `refund`) standing in for semantics.

## Run it

```bash
python3 hybrid.py
```

Expected output:

```
'ORD-1042': bm25=['d3'] dense=['d3', 'd5'] hybrid=['d3', 'd5']
'money back': bm25=['d4'] dense=['d4', 'd1'] hybrid=['d4', 'd1']
OK
```

## What it proves

- The identifier query `ORD-1042` finds `d3` through BM25 because the tokenizer keeps the hyphenated token intact.
- The paraphrase `money back` matches `d4` ("money back guarantee") in BM25, and the synonym map lets the dense side also surface `d1` (the refund policy), so the fused list is `d4`, `d1`.
- RRF uses only rank positions (`1/(60+rank)`), so no score normalisation between the two rankers is needed.

## Trade-offs

- RRF ignores score magnitude, so a very confident single retriever gets no extra weight.
- `k=60` is a common default and was not tuned; two retrievals double the query cost.
- The dense side here is a hand-written synonym map, not a trained model. The outputs above are specific to these five documents.

## When not to use it

- When queries are only exact lookups or only semantic questions, a single retriever is simpler and good enough.
