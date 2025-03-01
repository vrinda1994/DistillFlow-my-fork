import torch
from transformers import PreTrainedModel


class Distiller:
    def __init__(self, student: PreTrainedModel):
        self.device = 'mps' if torch.backends.mps.is_available() else 'cuda' if torch.cuda.is_available() else 'cpu'
        self.student = student

    def fine_tune(self, dataset, output_dir):
        raise NotImplementedError("Distiller must implement the fine_tune method.")

    def inference(self, query):
        raise NotImplementedError("Distiller must implement the inference method.")
