from rich import print
from datasets import Dataset
import polars as pl
from accelerate.test_utils.testing import get_backend
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
)
import torch
from torch import nn


print(f"""
*** [Device Summary] ***
Torch version: [green]{torch.__version__}[/]
CUDA Version: [green]{torch.version.cuda}[/]
Device name: [green]{torch.cuda.get_device_properties("cuda").name}[/]
FlashAttention available: [green]{torch.backends.cuda.flash_sdp_enabled()}[/]
""")


class InferenceTextClassification:
    def __init__(
            self,
            path_model: str,
            col: str,
            batch_size: int = 100,
            torch_compile: bool = True,
            fp16: bool = True,
            pretrain_name: str = 'bkai-foundation-models/vietnamese-bi-encoder',

    ):
        self.device, _, _ = get_backend()
        self.path_model = path_model
        self.col = col
        self.batch_size = batch_size

        self.fp16 = fp16
        self.torch_compile = torch_compile

        self.pretrain_name = pretrain_name
        self.tokenizer, self.model = self._load_model()
        self.id2label = list(self.model.config.id2label.values())

        print(f"""
        *** [Inference Summary] ***
        Device: [green]{self.device}[/]
        FP16: [green]{self.fp16}[/]
        Torch Compile: [green]{self.torch_compile}[/]
        Pretrain Name: [green]{self.pretrain_name}[/]
        """)

    def _load_model(self):
        # config
        config = {'pretrained_model_name_or_path': self.path_model}
        if self.fp16:
            config['torch_dtype'] = torch.bfloat16

        # model
        model = AutoModelForSequenceClassification.from_pretrained(**config).to(self.device)
        if self.torch_compile:
            model = torch.compile(model)

        # tokenizer
        tokenizer = AutoTokenizer.from_pretrained(self.pretrain_name)
        return tokenizer, model

    def _pp(self, inputs):
        input_token = self.tokenizer(
            text=inputs[self.col],
            return_tensors='pt',
            truncation=True,
            padding=True,
            max_length=50
        ).to(self.device)

        with torch.inference_mode():
            output = self.model(**input_token).logits
        probs = nn.Sigmoid()(output).half().cpu().detach().numpy().tolist()
        return {'score': probs, 'labels': [self.id2label for i in range(len(probs))]}

    def run(self, data: pl.DataFrame):
        return (
            Dataset.from_polars(data)
            .map(self._pp, batched=True, batch_size=self.batch_size)
        )


# torch compile: 2900 example/s
# torch compile fp 16: 7000 example/s
# no torch compile: 3000 example/s
# no torch compile fp 16: 6000 example/s
# pipeline: 2500 example/s
