"""Baseline retrieval evaluation: hit rate@k and MRR over a labelled question set (stdlib only)."""
import hashlib, math, re

CORPUS = {
    "refunds": "Refunds are allowed within 30 days and move a PAID order to REFUNDED",
    "shipping": "Shipping starts after payment and carriers are notified through the queue",
    "delivery": "Delivery confirmation moves the order to DELIVERED",
    "payment": "A payment event moves an order from PENDING to PAID",
}
# (question, id of the chunk that answers it)
GOLD = [
    ("how long do I have to get a refund", "refunds"),
    ("when does shipping start", "shipping"),
    ("what happens on delivery confirmation", "delivery"),
    ("how does an order become paid", "payment"),
    ("can I cancel a subscription", "refunds"),  # unanswerable on purpose: shows a miss
]

def vec(text, dim=64):
    v = [0.0] * dim
    for w in re.findall(r"[a-z]+", text.lower()):
        v[int(hashlib.md5(w.encode()).hexdigest(), 16) % dim] += 1
    n = math.sqrt(sum(x * x for x in v)) or 1
    return [x / n for x in v]

def search(q):
    qv = vec(q)
    return [d for d, _ in sorted(CORPUS.items(), key=lambda kv: -sum(a * b for a, b in zip(qv, vec(kv[1]))))]

def evaluate(k=1):
    hits, rr = 0, 0.0
    for q, gold in GOLD:
        ranks = search(q)
        if gold in ranks[:k]:
            hits += 1
        rr += 1 / (ranks.index(gold) + 1)
    return hits / len(GOLD), rr / len(GOLD)

if __name__ == "__main__":
    for k in (1, 3):
        hr, mrr = evaluate(k)
        print(f"hit_rate@{k}={hr:.2f} mrr={mrr:.2f}")
    hr1, _ = evaluate(1)
    hr3, _ = evaluate(3)
    assert hr3 >= hr1 and hr1 >= 0.6
    print("OK")
