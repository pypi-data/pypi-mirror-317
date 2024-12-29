import matplotlib.pyplot as plt
import matplotlib.cm as cm
from IPython.display import clear_output

def plot_training_progress(train_losses, val_losses, epoch, color_scheme='default', y_max=0):
    clear_output(wait=True)
    plt.figure(figsize=(5, 3))
    
    if color_scheme == 'viridis':
        cmap = cm.get_cmap('viridis', 2)
        plt.plot(train_losses, label='Train Loss', marker='o', color=cmap(0))
        plt.plot(val_losses,   label='Validation Loss', marker='x', color=cmap(1))
    else:
        plt.plot(train_losses, label='Train Loss', marker='o')
        plt.plot(val_losses,   label='Validation Loss', marker='x')
    
    plt.title(f'Epoch {epoch + 1}')
    plt.xlabel("Epoch")
    plt.ylabel("Loss")

    if y_max > 0:
        plt.ylim(0, y_max)

    plt.xticks(range(len(train_losses)))
    plt.legend(loc='upper right')
    plt.show()