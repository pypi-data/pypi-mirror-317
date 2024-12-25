import os
import numpy as np
import matplotlib.pyplot as plt

titledict = {'fontsize': 20,
                'style': 'normal', # 'oblique' 'italic'
                'fontweight': 'normal'} # 'bold', 'heavy', 'light', 'ultrabold', 'ultralight

labeldict = {'fontsize': 15,
                'style': 'normal', # 'oblique' 'italic'
                'fontweight': 'normal'} # 'bold', 'heavy', 'light', 'ultrabold', 'ultralight'

def plot_losses(train_losses, val_losses, plot_dir, model_name):
    """
    Plots training and validation loss curves and saves the figure to a file.

    Args:
        train_losses (list): List of training losses per epoch.
        val_losses (list): List of validation losses per epoch or None if no validation.
        plot_dir (str): Directory to save the plot image.
    """
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)
    epochs = range(1, len(train_losses) + 1)
    plt.figure()
    plt.plot(epochs, train_losses, 'bo-', label='Train Loss')
    if any(val_losses):
        plt.plot(epochs, val_losses, 'ro-', label='Val Loss')
    plt.title('Training and Validation Loss', **titledict)
    plt.xlabel('Epochs', **labeldict)
    plt.ylabel('Loss', **labeldict)
    plt.legend()
    plt.savefig(os.path.join(plot_dir, f'{model_name}_loss_curve.png'))
    plt.close()

def plot_performance(y_true, y_pred, plot_dir):
    """
    """
    lim = np.array([y_true.min(), y_true.max(), y_pred.min(), y_pred.max()])
    x = np.arange(lim.min(), lim.max()+0.1, 0.1)
    y = x
    
    x_label = "Exact data"
    y_label = "Predict data"

    plt.figure(figsize=(5, 5))
    plt.scatter(y_true, y_pred, s=10, c='black')
    plt.plot(x, y, linestyle='-.', color='red')
    plt.xlim(lim.min(), lim.max())
    plt.ylim(lim.min(), lim.max())
    plt.title("Regression Performance", **titledict)
    plt.xlabel(f'{x_label:>60}', **labeldict)
    plt.ylabel(f'{y_label:>60}', **labeldict)
    plt.legend()
    plt.savefig(os.path.join(plot_dir, 'regression_performance.png'))
    plt.close()