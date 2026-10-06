# pgvector

Postgres 17 with the pgvector extension: `search.sql` builds a 3-dimensional table, an HNSW index and a cosine nearest-neighbour query.

## Goal

Store embeddings next to relational data and query them with plain SQL. Vectors have three dimensions to keep the rows readable. The container runs locally and costs nothing.

## Run it

```bash
bash verify.sh
```

Expected: `compose.yaml` starts `pgvector/pgvector:0.8.0-pg17`, `search.sql` runs, the last two lines are the nearest rows (`refund policy` and `refund window`), then `OK`. The container and volume are removed on exit with `docker compose down -v`.

Not run end to end: Docker was not used when this README was written, so the expected output above comes from reading `search.sql` and `verify.sh`, not from a captured run.

## What it proves

- `CREATE EXTENSION vector`, a `vector(3)` column and the `<=>` cosine distance operator work in ordinary SQL.
- The index is created with `vector_cosine_ops`, which has to match the `<=>` operator used in the query.
- For the query `[1,0.05,0]` the two refund rows should rank above `shipping rules` and `payment states`; `verify.sh` checks that both returned rows contain "refund".

## Trade-offs

- One database for rows and vectors gives transactions, joins and filters, but vector search shares CPU and memory with your other queries.
- HNSW is approximate and memory hungry; with only four rows the index is not even needed, an exact scan is fine at small sizes.
- The compose file uses a throwaway password (`lab`) and publishes port 5432; it is for local use only.

## When not to use it

- At hundreds of millions of vectors or with strict filtered-search latency targets, a dedicated engine such as the one in `qdrant` fits better.
