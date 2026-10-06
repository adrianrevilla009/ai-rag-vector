CREATE EXTENSION IF NOT EXISTS vector;
DROP TABLE IF EXISTS chunks;
CREATE TABLE chunks (id serial PRIMARY KEY, body text, embedding vector(3));
INSERT INTO chunks (body, embedding) VALUES
  ('refund policy',  '[1,0,0]'),
  ('shipping rules', '[0,1,0]'),
  ('payment states', '[0,0,1]'),
  ('refund window',  '[0.9,0.1,0]');
-- HNSW index with cosine distance; <=> is the cosine distance operator
CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops);
-- nearest two neighbours of a "refund-like" query vector
SELECT body, round((embedding <=> '[1,0.05,0]')::numeric, 4) AS dist
FROM chunks ORDER BY embedding <=> '[1,0.05,0]' LIMIT 2;
