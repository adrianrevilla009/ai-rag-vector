"""OpenSearch k-NN index: mapping, bulk index, knn query (REST, stdlib only)."""
import json, urllib.request

BASE = "http://localhost:9200"

def call(method, path, body=None, raw=None):
    data = raw.encode() if raw else (json.dumps(body).encode() if body is not None else None)
    req = urllib.request.Request(BASE + path, method=method, data=data,
                                 headers={"Content-Type": "application/x-ndjson" if raw else "application/json"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)

try:
    call("DELETE", "/chunks")
except Exception:
    pass  # index did not exist
call("PUT", "/chunks", {
    "settings": {"index": {"knn": True}},
    "mappings": {"properties": {
        "body": {"type": "text"},
        "embedding": {"type": "knn_vector", "dimension": 3,
                      "method": {"name": "hnsw", "space_type": "cosinesimil", "engine": "lucene"}},
    }},
})
docs = [("refund policy", [1, 0, 0]), ("shipping rules", [0, 1, 0]), ("refund window", [0.9, 0.1, 0])]
bulk = "".join(json.dumps({"index": {"_index": "chunks", "_id": i}}) + "\n" +
               json.dumps({"body": b, "embedding": e}) + "\n" for i, (b, e) in enumerate(docs))
call("POST", "/_bulk?refresh=true", raw=bulk)
res = call("POST", "/chunks/_search", {"size": 2, "query": {"knn": {"embedding": {"vector": [1, 0.05, 0], "k": 2}}}})
hits = [(h["_score"], h["_source"]["body"]) for h in res["hits"]["hits"]]
for s, b in hits:
    print(round(s, 4), b)
assert all("refund" in b for _, b in hits)
print("OK")
