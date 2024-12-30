from torch import nn, Tensor
from transformers import EvalPrediction
from sklearn.metrics import f1_score, roc_auc_score, accuracy_score, classification_report
import numpy as np
from textwrap import dedent
from pathlib import Path
from itertools import batched


def data_batching(total_rows: int, n_size: int):
    batches = list(batched(range(0, total_rows), n_size))
    dict_ = {i: batches[i] for i in range(len(batches))}
    return dict_, len(dict_)


class MultiLabels:
    def __init__(self):
        self.sigmoid = nn.Sigmoid()

    def post_process(self, predictions, threshold: float = .5):
        probs = self.sigmoid(Tensor(predictions))
        y_pred = np.zeros(probs.shape)
        y_pred[np.where(probs >= threshold)] = 1
        return y_pred

    def report(self, predictions, labels, threshold=0.5):
        y_pred = self.post_process(predictions, threshold)

        f1_micro_average = f1_score(y_true=labels, y_pred=y_pred, average='micro')
        roc_auc = roc_auc_score(labels, y_pred, average='micro')
        accuracy = accuracy_score(labels, y_pred)
        metrics = {
            'f1': f1_micro_average,
            'roc_auc': roc_auc,
            'accuracy': accuracy
        }
        return metrics

    def classification_report_html(self, result, labels, target_names: list = None, show: bool = True):
        y_pred = MultiLabels().post_process(result)
        report = classification_report(labels, y_pred, target_names=target_names)
        if show:
            print(report)
        return report


def export_to_md(file_name: Path, config, valid_report, test_report):
    with open(file_name, 'w', encoding="utf-8") as md:
        text = dedent(f"""
        Config:
        {config}

        Valid Classification Report:
        {valid_report}

        Test Classification Report:
        {test_report}
        """)
        md.write(text)


def compute_metrics_multi(p: EvalPrediction):
    preds = p.predictions[0] if isinstance(p.predictions, tuple) else p.predictions
    result = MultiLabels().report(
        predictions=preds,
        labels=p.label_ids
    )
    return result


def post_process_multi_labels(example):
    lst = [i for i in example['logits'] if i['score'] > .5]
    return {
        'label': [i['label'] for i in lst],
        'score': [round(i['score'], 2) for i in lst],
    }
