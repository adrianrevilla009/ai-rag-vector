"""Idempotent ingestion: load -> chunk -> embed -> upsert into SQLite, skipping unchanged documents."""
import hashlib, json, math, re, sqlite3

DOCS = {
    "refunds.md": "Refunds are allowed within 30 days.\n\nPartial refunds are not supported.",
    "shipping.md": "Shipping starts after payment.\n\nCarriers are notified through the queue.",
}

def chunk(text):
    return [p.strip() for p in text.split("\n\n") if p.strip()]

def embed(text, dim=32):
    v = [0.0] * dim
    for w in re.findall(r"[a-z]+", text.lower()):
        v[int(hashlib.md5(w.encode()).hexdigest(), 16) % dim] += 1
    n = math.sqrt(sum(x * x for x in v)) or 1
    return [round(x / n, 4) for x in v]

def ingest(db, docs):
    stats = {"ingested": 0, "skipped": 0}
    for name, text in docs.items():
        digest = hashlib.sha256(text.encode()).hexdigest()
        row = db.execute("SELECT digest FROM docs WHERE name=?", (name,)).fetchone()
        if row and row[0] == digest:
            stats["skipped"] += 1
            continue
        db.execute("DELETE FROM chunks WHERE doc=?", (name,))  # replace stale chunks of a changed doc
        for i, c in enumerate(chunk(text)):
            db.execute("INSERT INTO chunks VALUES (?,?,?,?)", (name, i, c, json.dumps(embed(c))))
        db.execute("INSERT OR REPLACE INTO docs VALUES (?,?)", (name, digest))
        stats["ingested"] += 1
    db.commit()
    return stats

if __name__ == "__main__":
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE docs (name TEXT PRIMARY KEY, digest TEXT)")
    db.execute("CREATE TABLE chunks (doc TEXT, pos INT, body TEXT, embedding TEXT)")
    first = ingest(db, DOCS)
    second = ingest(db, DOCS)
    DOCS["refunds.md"] += "\n\nRefunds emit an event."
    third = ingest(db, DOCS)
    n = db.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    print(first, second, third, f"chunks={n}")
    assert first == {"ingested": 2, "skipped": 0} and second == {"ingested": 0, "skipped": 2}
    assert third == {"ingested": 1, "skipped": 1} and n == 5
    print("OK")
