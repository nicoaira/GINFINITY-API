import os
import torch
from external.GINFINITY.src.model.gin_model import GINModel

def load_model(model_path, device="cpu"):
    """
    Load a trained GIN model from checkpoint.
    """
    model = GINModel.load_from_checkpoint(model_path, device)
    model.to(device)
    model.eval()
    return model