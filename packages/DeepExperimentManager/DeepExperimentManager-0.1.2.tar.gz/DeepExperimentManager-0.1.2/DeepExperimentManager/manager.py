import os
import sys
import yaml
import importlib
import torch

from .config import load_config
from .trainer import Trainer
from .tester import Tester
from .datasets import get_datasets
from .utils import set_seed, count_parameters

class ExperimentManager:
    """
    ExperimentManager orchestrates the entire experiment workflow:
    - Loads configuration
    - Initializes model, datasets, and preprocessing
    - Sets up training and testing
    - Executes the training and (optionally) testing phases
    """

    def __init__(self, config_path):
        """
        Initializes the ExperimentManager.

        Args:
            config_path (str): The path to the configuration file.
        """
        self.config = load_config(config_path)
        self.device = self._get_device()
        self.export_results_enabled = self.config.get('export_results', {}).get('enabled', False)
        self.trainer = Trainer
        self.tester = Tester

    def _get_device(self):
        """
        Determines the computation device (CPU or GPU).

        Returns:
            torch.device: The device to use.
        """
        return torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def run_experiment(self):
        """
        Runs the full experiment including training and optional testing.
        """
        set_seed(self.config.get('seed', 42))

        # Load model and move to appropriate device
        self.model = self._load_model().to(self.device)

        # Retrieve train, valid, and test loaders based on config
        train_loader, valid_loader, test_loader = get_datasets(self.config['dataset'])

        # Initialize trainer and run training
        self.trainer = self.trainer(self.model, train_loader, valid_loader, self.config, self.device)
        self.trainer.train()

        # If a test loader is available, run testing
        if test_loader is not None:
            self.isTest = True
            self.tester = self.tester(self.model, test_loader, self.config, self.device)
            self.tester.test()
        else:
            self.isTest = False

        if self.export_results_enabled:
            export_dir = self.config['export_results'].get('export_dir', f'./results/{type(self.model).__name__}')
            self._export_results(export_dir)

    def _load_model(self):
        """
        Dynamically loads and instantiates the model specified in the config.

        Returns:
            nn.Module: The instantiated PyTorch model.
        """
        model_config = self.config['model']
        module_name = model_config['module']
        class_name = model_config['class']
        model_args = model_config.get('args', {})

        sys.path.append(os.getcwd())
        module = importlib.import_module(module_name)
        model_class = getattr(module, class_name)
        model = model_class(**model_args)

        return model
    
    def _export_results(self, export_dir):
        """
        Exporting the recorded results and experiment configuration.

        Args:
            export_dir (str): Directory to save the results file.
        """
        print("[Exporting] Exporting recorded results and configuration...")

        total_params = count_parameters(self.model)
        train_losses, valid_losses, total_time, valid_time = self.trainer.get_results()
        if self.isTest:    
            test_results = self.tester.get_results()
        else:
            test_results = {}
        
        model_config = self.config.get('model', {})
        training_config = self.config.get('training', {})
        loss_func = self.config.get('loss', {})

        batch = self.config['dataset']['args']['train']['loader'].get('batch_size', {})
        training_config['batch_size'] = batch

        if not os.path.exists(export_dir):
            os.makedirs(export_dir)

        export_path = os.path.join(export_dir, f'{type(self.model).__name__}_results.yaml')

        if os.path.exists(export_path):
            with open(export_path, 'r') as f:
                existing_data = yaml.safe_load(f)

            if existing_data is None:
                existing_data = {}

            if "records" not in existing_data:
                existing_data = {
                    "records": [existing_data] if existing_data else []
                }
            existing_data["records"].append({
                "model_config": model_config,
                "training_config": training_config,
                "loss_func": loss_func,
                "num_parameters": total_params,
                "total_time": total_time,
                "valid_time": valid_time,
                "train_losses": train_losses,
                "valid_losses": valid_losses,
                "test_results": test_results
            })

            with open(export_path, 'w') as f:
                yaml.safe_dump(existing_data, f, sort_keys=False, default_flow_style=False, indent=4)

        else:
            data_to_export = {
                "records": [
                    {
                        "model_config": model_config,
                        "training_config": training_config,
                        "loss_func": loss_func,
                        "num_parameters": total_params,
                        "total_time": total_time,
                        "valid_time": valid_time,
                        "train_losses": train_losses,
                        "valid_losses": valid_losses,
                        "test_results": test_results    
                    }
                ]
            }
            with open(export_path, 'w') as f:
                yaml.safe_dump(data_to_export, f, sort_keys=False, default_flow_style=False, indent=4)
                
        print(f"[Exporting] Results and configuration exported to {export_path}.")