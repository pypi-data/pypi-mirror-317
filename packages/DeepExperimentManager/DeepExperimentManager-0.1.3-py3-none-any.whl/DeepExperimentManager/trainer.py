import time
from tqdm import tqdm

import torch
from torch import nn, optim

from .utils import save_checkpoint
from .visualization import plot_losses

class Trainer:
    """
    Trainer class that manages the training process of a model.

    Attributes:
        model (nn.Module): The model to be trained.
        train_loader (DataLoader or None): DataLoader for the training set.
        val_loader (DataLoader or None): DataLoader for the validation set.
        config (dict): Configuration dictionary.
        device (torch.device): The device to run on (CPU or GPU).
        visualization_enabled (bool): Whether to plot training/validation losses.
        export_loss_enabled (bool): Whether to export the recorded losses to a file.
        train_losses (list): A list of recorded training losses if visualization or export is enabled.
        val_losses (list): A list of recorded validation losses if visualization or export is enabled.
    """

    def __init__(self, model, train_loader, valid_loader, config, device):
        """
        Initializes the Trainer.

        Args:
            model (nn.Module): The PyTorch model to train.
            train_loader (DataLoader or None): Training data loader.
            val_loader (DataLoader or None): Validation data loader.
            config (dict): Experiment configuration.
            device (torch.device): Computation device (CPU or GPU).
        """
        print("[Initializing] Starting trainer initialization...")

        steps = [
            "Loading model",
            "Loading training data loader",
            "Loading validation data loader",
            "Configuring loss function",
            "Configuring optimizer",
            "Finalizing setup"
        ]

        with tqdm(total=len(steps), desc="[Initializing]", bar_format="{l_bar}{bar:40}{r_bar}") as pbar:
            self.model = model
            pbar.set_postfix_str("Loading model...")
            time.sleep(0.5)
            pbar.update(1)

            self.train_loader = train_loader
            if self.train_loader is None:
                raise ValueError("Training data loader (train_loader) is not provided.")
            pbar.set_postfix_str("Loading training data loader...")
            time.sleep(0.5)
            pbar.update(1)

            self.valid_loader = valid_loader
            pbar.set_postfix_str("Loading validation data loader...")
            time.sleep(0.5)
            pbar.update(1)

            self.config = config
            self.device = device

            self.criterion = self._get_loss_function()
            pbar.set_postfix_str("Configuring loss function...")
            time.sleep(0.5)
            pbar.update(1)

            self.optimizer = self._get_optimizer()
            pbar.set_postfix_str("Configuring optimizer...")
            time.sleep(0.5)
            pbar.update(1)

            self.visualization_enabled = self.config.get('visualization', {}).get('enabled', False)
            self.export_results_enabled = self.config.get('export_results', {}).get('enabled', False)

            if self.visualization_enabled or self.export_results_enabled:
                self.train_losses = []
                self.valid_losses = []

            pbar.set_postfix_str("Finalizing setup...")
            time.sleep(0.5)
            pbar.update(1)

        print("[Initializing] Trainer Initialized successfully.")

    def _get_loss_function(self):
        loss_config = self.config.get('loss', {})
        loss_type = loss_config['type']
        loss_args = loss_config.get('args', {})
        loss_class = getattr(nn, loss_type)

        return loss_class(**loss_args)

    def _get_optimizer(self):
        optimizer_config = self.config['training']['optimizer']
        optimizer_type = optimizer_config['type']
        optimizer_args = optimizer_config.get('args', {})
        lr = self.config['training']['learning_rate']
        optimizer_class = getattr(optim, optimizer_type)

        return optimizer_class(self.model.parameters(), lr=lr, **optimizer_args)

    def train(self):
        print("[Training] Starting training process...")
        epochs = self.config['training']['epochs']
        self.zf = len(str(epochs)) # Zero filling
        self.valid_time = 0
        total_start_time = time.time()

        for epoch in range(epochs):
            with tqdm(total=len(self.train_loader), desc=f"Epoch {epoch+1:0{self.zf}d}/{epochs} [Training]",
                      bar_format="{l_bar}{bar:40}{r_bar}", leave=True) as pbar:
                self.model.train()
                total_loss = 0
                for inputs, targets in self.train_loader:
                    inputs, targets = inputs.to(self.device), targets.to(self.device)
                    self.optimizer.zero_grad()
                    outputs = self.model(inputs)
                    loss = self.criterion(outputs, targets)
                    loss.backward()
                    self.optimizer.step()
                    total_loss += loss.item()
                    pbar.set_postfix(loss=loss.item())
                    pbar.update(1)

            avg_loss = total_loss / len(self.train_loader)
            print(f"Epoch {epoch+1:0{self.zf}d}/{epochs} Train Loss: {avg_loss:.4f}")

            if self.visualization_enabled or self.export_results_enabled:
                self.train_losses.append(avg_loss)

            if self.valid_loader is not None: # Validation
                val_start_time = time.time()
                val_loss = self.validate(epoch, epochs)
                val_end_time = time.time()
                self.valid_time += val_end_time - val_start_time
                if self.visualization_enabled or self.export_results_enabled:
                    self.valid_losses.append(val_loss)

            save_checkpoint(self.model, epoch, self.config.get('checkpoint_dir', f'./checkpoints/{type(self.model).__name__}'))

        total_end_time = time.time()
        self.total_time = total_end_time - total_start_time
        print(f"[Training] Training process completed in {self.total_time}s.")

        if self.visualization_enabled:
            plot_dir = self.config['visualization'].get('plot_dir', f'./plots/{type(self.model).__name__}')
            islogscale = self.config['visualization'].get('log_scale', False)
            plot_losses(self.train_losses, self.valid_losses, plot_dir, type(self.model).__name__, islogscale)

    def validate(self, epoch, epochs):
        print(f"[Validation] Starting validation for epoch {epoch+1:0{self.zf}d}/{epochs}...")

        self.model.eval()
        total_loss = 0
        with tqdm(total=len(self.valid_loader), desc=f"Epoch {epoch+1:0{self.zf}d}/{epochs} [Validation]",
                  bar_format="{l_bar}{bar:40}{r_bar}", leave=True) as pbar:
            with torch.no_grad():
                for inputs, targets in self.valid_loader:
                    inputs, targets = inputs.to(self.device), targets.to(self.device)
                    outputs = self.model(inputs)
                    loss = self.criterion(outputs, targets)
                    total_loss += loss.item()
                    pbar.set_postfix(loss=loss.item())
                    pbar.update(1)

        avg_loss = total_loss / len(self.valid_loader)
        print(f"[Validation] Validation completed. Avg Loss: {avg_loss:.4f}")
        return avg_loss

    def get_results(self):
        """
        Retunrs the recorded losses and experiment configuration.
        """
        return self.train_losses, self.valid_losses, self.total_time, self.valid_time
