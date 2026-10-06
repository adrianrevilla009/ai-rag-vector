# opensearch-vector

A single-node OpenSearch 2.17.1 container and `search.py`, which creates a k-NN index, bulk-indexes three documents and runs a `knn` query.

## Goal

Run vector search inside a search engine: a `knn_vector` field with an HNSW method (Lucene engine, cosine similarity), a bulk index call and a `knn` query. The security plugin is disabled in `compose.yaml`, so use it on a local machine only and never expose the port.

## Run it

```bash
bash verify.sh
```

Expected: `verify.sh` starts the container (about 1 GB of RAM), polls port 9200 for up to two minutes, runs `search.py`, prints two lines of `score body` (both containing "refund") and `OK`, then removes the container with `docker compose down -v`.

Not run end to end: Docker was not used when this README was written, so the expected output comes from reading `search.py`, not from a captured run.

## What it proves

- k-NN is an index setting (`"knn": true`) plus a field mapping with dimension 3.
- The query vector `[1,0.05,0]` should return `refund policy` and `refund window` ahead of `shipping rules`; `search.py` asserts that both hits contain "refund".
- The index also has a plain `body` text field, which is the basis for combining keyword and vector search as in `hybrid-search`.

## Trade-offs

- One system covers keywords, filters, aggregations and vectors, but it is heavier to run and tune than Qdrant.
- Search is near-real-time: documents appear only after a refresh, which the script forces with `refresh=true` on the bulk call.
- The script deletes and recreates the `chunks` index every run.

## When not to use it

- If you only need vectors and have no text-search workload, pgvector or a smaller engine is cheaper to operate.
