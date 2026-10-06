# qdrant

A Qdrant v1.12.4 container and `search.py`, which creates a collection, upserts three points and runs a filtered cosine search over REST.

## Goal

Use a dedicated vector database: declare a collection, store points with payloads and combine vector similarity with a payload filter. It runs locally and costs nothing.

## Run it

```bash
bash verify.sh
```

Expected: `verify.sh` starts `compose.yaml`, waits for `/readyz`, runs `search.py`, prints two lines of `score body` (the top one is `refund policy`) and `OK`, then removes the container with `docker compose down -v`.

Not run end to end: Docker was not used when this README was written, so the expected output comes from reading `search.py`, not from a captured run.

## What it proves

- A collection fixes the vector size (3) and distance (`Cosine`) up front.
- The filter `lang = en` is applied inside the search, so the Spanish point `politica de reembolso` (vector `[0.9,0.1,0]`) is excluded even though it is close to the query.
- `search.py` asserts that the top hit is `refund policy` and that every hit has `lang` equal to `en`.

## Trade-offs

- You get purpose-built filtering, quantization and sharding, but run another service that must be kept in sync with your source of truth.
- There are no joins or transactions with relational data.
- `search.py` deletes and recreates the `chunks` collection each run, so it is not safe to point at a shared instance.

## When not to use it

- When the corpus is small and already in Postgres, `pgvector` is simpler to operate.
