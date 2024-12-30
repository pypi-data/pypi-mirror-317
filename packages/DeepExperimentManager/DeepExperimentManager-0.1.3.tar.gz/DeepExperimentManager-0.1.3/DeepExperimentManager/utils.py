import os
import random
import numpy as np

import torch

def set_seed(seed):
    """
    Sets the random seed for reproducibility.

    Args:
        seed (int): The seed value to set.
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

def save_checkpoint(model, epoch, checkpoint_dir):
    """
    Saves a model checkpoint.

    Args:
        model (nn.Module): The model to save.
        epoch (int): The current epoch number.
        checkpoint_dir (str): The directory to save checkpoints.
    """
    if not os.path.exists(checkpoint_dir):
        os.makedirs(checkpoint_dir)
    path = os.path.join(checkpoint_dir, f"{type(model).__name__}_checkpoint_epoch_{epoch+1}.pth")
    torch.save(model.state_dict(), path)

def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)