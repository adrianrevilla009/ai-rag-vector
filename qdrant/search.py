"""Create a collection, upsert points with payloads, run a filtered cosine search (REST, stdlib only)."""
import json, urllib.request

BASE = "http://localhost:6333"

def call(method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.load(r)

call("DELETE", "/collections/chunks")
call("PUT", "/collections/chunks", {"vectors": {"size": 3, "distance": "Cosine"}})
call("PUT", "/collections/chunks/points?wait=true", {"points": [
    {"id": 1, "vector": [1, 0, 0], "payload": {"body": "refund policy", "lang": "en"}},
    {"id": 2, "vector": [0, 1, 0], "payload": {"body": "shipping rules", "lang": "en"}},
    {"id": 3, "vector": [0.9, 0.1, 0], "payload": {"body": "politica de reembolso", "lang": "es"}},
]})
hits = call("POST", "/collections/chunks/points/search", {
    "vector": [1, 0.05, 0], "limit": 2, "with_payload": True,
    "filter": {"must": [{"key": "lang", "match": {"value": "en"}}]},
})["result"]
for h in hits:
    print(round(h["score"], 4), h["payload"]["body"])
assert hits[0]["payload"]["body"] == "refund policy" and all(h["payload"]["lang"] == "en" for h in hits)
print("OK")
