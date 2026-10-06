# ai-rag-vector

Seven small retrieval labs for RAG: chunking, three vector stores, hybrid search, ingestion and a baseline evaluation, so you can see how each piece is wired and compare them.

## What is inside

| Folder | What it shows | Run |
| --- | --- | --- |
| [`chunking-embeddings`](./chunking-embeddings) | Fixed, sentence and paragraph chunking compared, with a hashing embedding and cosine search | `python3 chunk.py` |
| [`pgvector`](./pgvector) | Postgres with pgvector: `vector(3)` column, HNSW index, cosine query in SQL | `bash verify.sh` |
| [`qdrant`](./qdrant) | Qdrant over REST: collection, upsert with payloads, filtered cosine search | `bash verify.sh` |
| [`opensearch-vector`](./opensearch-vector) | OpenSearch `knn_vector` mapping, bulk index and `knn` query | `bash verify.sh` |
| [`hybrid-search`](./hybrid-search) | BM25 and vector rankings fused with Reciprocal Rank Fusion | `python3 hybrid.py` |
| [`rag-eval-baseline`](./rag-eval-baseline) | Hit rate@k and MRR over a small labelled question set | `python3 eval.py` |
| [`ingestion-pipeline`](./ingestion-pipeline) | Idempotent load, chunk, embed, upsert into SQLite with content hashing | `python3 ingest.py` |

## Prerequisites

- Python 3 (standard library only, no packages to install).
- Docker with Compose v2 for `pgvector`, `qdrant` and `opensearch-vector` (about 1 GB of free RAM for OpenSearch).
- `curl` for the readiness loops in the `verify.sh` scripts.

## How to read it

Start with `chunking-embeddings`, then `hybrid-search` and `rag-eval-baseline`, which need nothing but Python. The three store folders use 3-dimensional vectors so the data stays readable, and the Python folders use an offline hashing embedding instead of a model, so no API keys or downloads are needed. The example text comes from the shared Orders domain.
