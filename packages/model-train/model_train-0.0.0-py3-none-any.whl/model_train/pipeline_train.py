from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding,
    EarlyStoppingCallback
)
import torch
import gc
from rich import print
from .func import compute_metrics_multi


class Pipeline:
    def __init__(self, pretrain_name: str, **kwargs):
        self.pretrain_name = pretrain_name
        self.id2label = kwargs.pop('id2label', {})
        self.label2id = kwargs.pop('label2id', {})
        self._load_model()

    def _load_model(self):
        print(f'Pretrain: {self.pretrain_name}')

        self.tokenizer = AutoTokenizer.from_pretrained(self.pretrain_name)
        self.data_collator = DataCollatorWithPadding(tokenizer=self.tokenizer)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.pretrain_name,
            num_labels=len(self.id2label),
            id2label=self.id2label,
            label2id=self.label2id,
            problem_type='multi_label_classification',
        )

    def train(self, folder: str, train, val, **kwargs):
        log_step = kwargs.get('log_step', 50)
        training_args = TrainingArguments(
            output_dir=folder,
            warmup_ratio=0.1,
            lr_scheduler_type='cosine',
            weight_decay=0.001,
            learning_rate=kwargs.get('learning_rate', 1e-4),
            per_device_train_batch_size=kwargs.get('per_device_train_batch_size', 512),
            per_device_eval_batch_size=kwargs.get('per_device_eval_batch_size', 64),
            fp16=True,
            logging_strategy='steps',
            save_strategy='steps',
            eval_strategy='steps',
            save_steps=log_step,
            eval_steps=log_step,
            logging_steps=log_step,
            save_total_limit=2,
            load_best_model_at_end=True,
            metric_for_best_model='f1',
            report_to="none",
            num_train_epochs=kwargs.get('num_train_epochs', 3),
            optim='adafactor',
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train,
            eval_dataset=val,
            data_collator=self.data_collator,
            compute_metrics=compute_metrics_multi,
            callbacks=[EarlyStoppingCallback(early_stopping_patience=3)],
        )

        train_results = trainer.train()
        trainer.save_model()
        trainer.log_metrics("train", train_results.metrics)
        trainer.save_metrics("train", train_results.metrics)
        trainer.save_state()

        torch.cuda.empty_cache()
        gc.collect()

        return trainer
