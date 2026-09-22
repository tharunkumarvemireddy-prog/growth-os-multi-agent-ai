from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)


data = {
    "question": [
        "What does the manufacturing company focus on?"
    ],
    "answer": [
        "The company focuses on industrial automation, production efficiency and predictive maintenance."
    ],
    "contexts": [
        [
            "ABC Industrial Systems provides industrial automation solutions.",
            "Key themes include predictive maintenance, production efficiency and operational visibility."
        ]
    ],
    "ground_truth": [
        "The company focuses on industrial automation, production efficiency and predictive maintenance."
    ],
}

dataset = Dataset.from_dict(data)

result = evaluate(
    dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
    ],
)

print(result)
