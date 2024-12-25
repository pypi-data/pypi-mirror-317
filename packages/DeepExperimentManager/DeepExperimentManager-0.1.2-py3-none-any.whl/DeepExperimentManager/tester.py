from tqdm import tqdm
import torch
from sklearn.metrics import accuracy_score, mean_squared_error, mean_absolute_error, f1_score

from .visualization import plot_performance

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
        Initializes the Tester.

        Args:
            model (nn.Module): The trained model to be tested.
            test_loader (DataLoader): Test data loader.
            config (dict): Experiment configuration.
            device (torch.device): Computation device (CPU or GPU).
        """
        print("[Initializing] Starting Tester initialization...")
        self.model = model
        self.test_loader = test_loader
        self.config = config
        self.device = device
        self.visualization_enabled = self.config.get('visualization', {}).get('enabled', False)
        print("[Initializing] Tester initialized successfully.")

    def test(self):
        """
        Runs the test loop and prints the evaluation metrics based on the configuration.
        """
        if self.test_loader is None:
            print("[Testing] No test data provided. Exiting test process.")
            return

        print("[Testing] Starting the test process...")
        self.model.eval()

        # Retrieve metrics from config
        metrics = self.config.get("testing", {}).get("metrics", ["accuracy"])
        all_targets = []
        all_preds = []

        with tqdm(total=len(self.test_loader), desc="[Testing Progress]", bar_format="{l_bar}{bar:40}{r_bar}", leave=True) as pbar:
            with torch.no_grad():
                for inputs, targets in self.test_loader:
                    inputs, targets = inputs.to(self.device), targets.to(self.device)
                    outputs = self.model(inputs)

                    if any(metric in ["accuracy", "f1"] for metric in metrics):
                        _, preds = torch.max(outputs, 1)
                        all_targets.extend(targets.cpu().numpy())
                        all_preds.extend(preds.cpu().numpy())

                    if any(metric in ["mse", "mae"] for metric in metrics):
                        all_targets.extend(targets.cpu().numpy())
                        all_preds.extend(outputs.cpu().numpy())

                    pbar.update(1)

        # Calculate and store each metric
        self.results = {}
        if "accuracy" in metrics:
            self.results["accuracy"] = accuracy_score(all_targets, all_preds)
            print(f"[Testing] Test Accuracy: {self.results['accuracy']:.4f}")

        if "f1" in metrics:
            self.results["f1"] = f1_score(all_targets, all_preds, average="weighted")
            print(f"[Testing] Test F1 Score: {self.results['f1']:.4f}")

        if "mse" in metrics:
            self.results["mse"] = mean_squared_error(all_targets, all_preds)
            print(f"[Testing] Test Mean Squared Error: {self.results['mse']:.4f}")

        if "mae" in metrics:
            self.results["mae"] = mean_absolute_error(all_targets, all_preds)
            print(f"[Testing] Test Mean Absolute Error: {self.results['mae']:.4f}")

        print("[Testing] Test process completed.")
        """ In developing...
        if self.visualization_enabled:
            plot_dir = self.config['visualization'].get('plot_dir', './plots')
            plot_performance(self.train_losses, self.valid_losses, plot_dir)
        """

    def get_results(self):
        """
        Returns the test results.
        
        Returns:
            self.results (dict) : Recorded test results
        """
        return self.results
