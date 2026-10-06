# rag-eval-baseline

`eval.py` scores a baseline retriever with hit rate@k and MRR over five labelled questions and a four-chunk Orders corpus.

## Goal

Measure retrieval before tuning it. The retriever is the offline hashing embedding; replace `search()` with a query against any store in this repo to compare it with the baseline.

## Run it

```bash
python3 eval.py
```

Expected output:

```
hit_rate@1=0.60 mrr=0.70
hit_rate@3=0.60 mrr=0.70
OK
```

## What it proves

- The baseline answers 3 of 5 questions at rank 1, giving a number to beat when you change chunking, embeddings or fusion.
- One question ("can I cancel a subscription") is unanswerable on purpose and is labelled `refunds`; it counts as a miss, so the score is not a trivial 1.0.
- Hit rate@3 stays at 0.60 because both misses rank the right chunk last of four (MRR 0.70 fits that), and `eval.py` asserts hit rate@3 is at least hit rate@1 and that hit rate@1 is at least 0.6.

## Trade-offs

- Hit rate only checks that the right chunk is retrieved, not that the final answer is correct.
- Five questions are an illustration; a useful set needs dozens to hundreds, ideally from real queries.
- Each question has exactly one correct chunk, so questions answered by several chunks are not modelled.

## When not to use it

- For end-to-end answer quality such as faithfulness or citation accuracy, use an answer-level evaluation; this checks retrieval only.
