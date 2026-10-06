"""Hybrid search: BM25 + hashing-vector ranking fused with Reciprocal Rank Fusion (stdlib only)."""
import hashlib, math, re
from collections import Counter

DOCS = {
    "d1": "refund policy: a PAID order can be refunded within 30 days",
    "d2": "shipping queue notifies carriers after payment",
    "d3": "order ORD-1042 was marked DELIVERED by the carrier",
    "d4": "money back guarantee for returned goods",
    "d5": "payment event moves an order from PENDING to PAID",
}

def tok(t):
    return re.findall(r"[a-z0-9\-]+", t.lower())

def bm25(query, docs, k1=1.5, b=0.75):
    toks = {d: tok(t) for d, t in docs.items()}
    avg = sum(map(len, toks.values())) / len(toks)
    df = Counter(w for t in toks.values() for w in set(t))
    out = {}
    for d, t in toks.items():
        tf = Counter(t)
        out[d] = sum(math.log(1 + (len(docs) - df[w] + .5) / (df[w] + .5)) * tf[w] * (k1 + 1)
                     / (tf[w] + k1 * (1 - b + b * len(t) / avg)) for w in tok(query) if w in tf)
    return out

def vec(text, dim=32):
    v = [0.0] * dim
    for w in tok(text):
        # crude "semantic" hook: map synonyms onto one concept before hashing
        w = {"refunded": "refund", "money": "refund", "back": "refund", "returned": "refund"}.get(w, w)
        v[int(hashlib.md5(w.encode()).hexdigest(), 16) % dim] += 1
    n = math.sqrt(sum(x * x for x in v)) or 1
    return [x / n for x in v]

def dense(query, docs):
    q = vec(query)
    return {d: sum(a * b for a, b in zip(q, vec(t))) for d, t in docs.items()}

def ranked(scores):
    return [d for d, s in sorted(scores.items(), key=lambda x: -x[1]) if s > 0]

def rrf(rankings, k=60):
    fused = Counter()
    for r in rankings:
        for pos, d in enumerate(r, 1):
            fused[d] += 1 / (k + pos)
    return [d for d, _ in fused.most_common()]

if __name__ == "__main__":
    for q in ("ORD-1042", "money back"):
        lex, den = ranked(bm25(q, DOCS)), ranked(dense(q, DOCS))
        print(f"{q!r}: bm25={lex[:2]} dense={den[:2]} hybrid={rrf([lex, den])[:2]}")
    assert rrf([ranked(bm25("ORD-1042", DOCS)), ranked(dense("ORD-1042", DOCS))])[0] == "d3"
    assert rrf([ranked(bm25("money back", DOCS)), ranked(dense("money back", DOCS))])[0] in ("d4", "d1")
    print("OK")
