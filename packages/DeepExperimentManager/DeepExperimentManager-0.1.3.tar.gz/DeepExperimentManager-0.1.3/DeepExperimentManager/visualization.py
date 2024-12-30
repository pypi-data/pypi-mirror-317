import os
import numpy as np
import matplotlib.pyplot as plt

titledict = {'fontsize': 20,
                'style': 'normal', # 'oblique' 'italic'
                'fontweight': 'normal'} # 'bold', 'heavy', 'light', 'ultrabold', 'ultralight

labeldict = {'fontsize': 15,
                'style': 'normal', # 'oblique' 'italic'
                'fontweight': 'normal'} # 'bold', 'heavy', 'light', 'ultrabold', 'ultralight'

def plot_losses(train_losses, val_losses, plot_dir, model_name, log_scale=False):
    """
    Plots training and validation loss curves and saves the figure to a file.

    Args:
        train_losses (list): List of training losses per epoch.
        val_losses (list): List of validation losses per epoch or None if no validation.
        plot_dir (str): Directory to save the plot image.
        model_name (str): Name of the model, used for saving the plot.
        log_scale (bool): Whether to plot the curve using a logarithmic scale.

    Saves:
        A PNG file named '<model_name>_loss_curve.png' in the specified `plot_dir`.
    """
    # Create the directory if it does not exist
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)

    # Define the epochs
    epochs = range(1, len(train_losses) + 1)

    if log_scale == True:
        train_losses = np.log(train_losses)
        val_losses = np.log(val_losses)

    # Plot the losses
    plt.figure()
    plt.plot(epochs, train_losses, color='k', linestyle='-', label='Train Loss')  # Black solid line
    if any(val_losses):
        plt.plot(epochs, val_losses, color='gray', linestyle='--', label='Val Loss')  # Gray dashed line
    
    # Add title and labels
    plt.title('Training and Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    # Save the figure
    plt.savefig(os.path.join(plot_dir, f'{model_name}_loss_curve.png'))
    plt.close()

def plot_regression(y_true, y_pred, plot_dir, model_name):
    """
    Plots a regression performance scatter plot and saves the figure to a file.

    This function creates a scatter plot comparing the true values (`y_true`) with the predicted 
    values (`y_pred`). It also includes a reference line (y=x) to visualize the deviation from 
    perfect prediction.

    Args:
        y_true (numpy.ndarray): Array of true values.
        y_pred (numpy.ndarray): Array of predicted values.
        plot_dir (str): Directory to save the plot image.
        model_name (str): Name of the model, used for saving the plot.

    Saves:
        A PNG file named '<model_name>_regression_performance.png' in the specified `plot_dir`.
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
    plt.savefig(os.path.join(plot_dir, f'{model_name}_regression_performance.png'))
    plt.close()