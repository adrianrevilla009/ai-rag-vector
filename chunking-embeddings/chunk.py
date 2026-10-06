"""Compare three chunking strategies and a toy hashing embedding (stdlib only, deterministic)."""
import hashlib, math, re

DOC = """Orders are created in the PENDING state. A payment event moves an order to PAID.

Refunds are allowed within 30 days. A refund moves a PAID order to REFUNDED and emits an event.
Partial refunds are not supported in v1.

Shipping starts after payment. Carriers are notified through the shipping queue. Delivery
confirmation moves the order to DELIVERED. Lost parcels are handled by support."""

def fixed(text, size=120, overlap=30):
    step = size - overlap
    return [text[i:i + size] for i in range(0, max(len(text) - overlap, 1), step)]

def sentences(text, per=2):
    s = re.split(r"(?<=[.!?])\s+", text.replace("\n", " "))
    return [" ".join(s[i:i + per]) for i in range(0, len(s), per)]

def paragraphs(text):
    return [p.replace("\n", " ") for p in text.split("\n\n") if p.strip()]

def embed(text, dim=64):
    """Hashing-trick bag of words, L2-normalised. A stand-in for a real model."""
    v = [0.0] * dim
    for w in re.findall(r"[a-z]+", text.lower()):
        v[int(hashlib.md5(w.encode()).hexdigest(), 16) % dim] += 1.0
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / n for x in v]

def cosine(a, b):
    return sum(x * y for x, y in zip(a, b))

if __name__ == "__main__":
    q = embed("how do refunds work")
    for name, fn in (("fixed", fixed), ("sentences", sentences), ("paragraphs", paragraphs)):
        chunks = fn(DOC)
        best = max(chunks, key=lambda c: cosine(q, embed(c)))
        print(f"{name:10} chunks={len(chunks):2} avg_len={sum(map(len, chunks)) // len(chunks):3} best={best[:50]!r}")
    assert "refund" in max(paragraphs(DOC), key=lambda c: cosine(q, embed(c))).lower()
    print("OK")
