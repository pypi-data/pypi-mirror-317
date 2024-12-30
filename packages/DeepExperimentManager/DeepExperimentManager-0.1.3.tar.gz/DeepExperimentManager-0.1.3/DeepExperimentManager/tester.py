import importlib
from tqdm import tqdm
import torch

from .visualization import plot_regression
from .tasks import *

TASK_MAP = {
    "classification": ClassificationTask,
    "multilableclassification": MultiLabelClassificationTask,
    "regression": RegressionTask,
    "segmentation": SegmentationTask,
    "objectdetection": ObjectDetectionTask,
    "timeseriesforecasting": TimeSeriesForecastingTask,
    "generation": GenerationTask
}

class Tester:
    """
    Tester class for evaluating the model on a given test dataset.

    Attributes:
        model (nn.Module): The trained PyTorch model.
        test_loader (DataLoader): DataLoader for the test dataset.
        config (dict): Experiment configuration.
        device (torch.device): Computation device.
    """

    def __init__(self, model, test_loader, config, device):
        """
        Initializes the Tester Module.

        Args:
            model (nn.Module): The trained model to be tested.
            test_loader (DataLoader): Test data loader.
            config (dict): Experiment configuration.
            device (torch.device): Computation device (CPU or GPU).
        """
        print("[Initializing] Starting Tester initialization...")
        self.model = model
        self.test_loader = test_loader
        if self.test_loader is None:
            print("[Testing] No test data provided. Exiting test process.")
            return
        self.config = config
        self.device = device
        self.visualization_enabled = self.config.get('visualization', {}).get('enabled', False)
        self.task = self.config.get('task', 'classification')
        self.results = {}
        print("[Initializing] Tester initialized successfully.")

    def test(self):
        """
        Runs the test loop and prints the evaluation metrics based on the configuration.
        """
        print("[Testing] Starting the test process...")
        self.model.eval()
        task = TASK_MAP[self.config.get("task", "classification")]()

        # Retrieve metrics from config
        all_targets, all_preds = [], []

        with tqdm(total=len(self.test_loader), desc="[Testing Progress]", bar_format="{l_bar}{bar:40}{r_bar}", leave=True) as pbar:
            with torch.no_grad():
                for inputs, targets in self.test_loader:
                    inputs, targets = inputs.to(self.device), targets.to(self.device)

                    preds = task.inference(self.model, inputs)

                    all_preds.extend(preds.cpu().numpy())
                    all_targets.extend(targets.cpu().numpy())
                    pbar.update(1)

        metrics = self._get_metrics()
        for path, func in metrics:
            try:
                score = func(all_targets, all_preds)
                self.results[path] = score
                print(f"[Testing] {path}: {score:.4f}")
            except Exception as e:
                print(f"[ERROR] {path} failed: {e}")
            
        print("[Testing] Test process completed.")

    def _get_metrics(self):
        """
        Get metric functions for test process.
        """
        metrics_paths = self.config.get("testing", {}).get("metrics", [])
        metric_funcs = []
        for path in metrics_paths:
            parts = path.split(".")
            module_path = ".".join(parts[:-1])
            func_name = parts[-1]
            module = importlib.import_module(module_path)
            metric_funcs.append((path, getattr(module, func_name)))

        return metric_funcs

    def get_results(self):
        """
        Returns the test results.
        
        Returns:
            self.results (dict) : Recorded test results
        """
        return self.results
