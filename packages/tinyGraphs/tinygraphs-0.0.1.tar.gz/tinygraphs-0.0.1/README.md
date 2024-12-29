# tinyGraphs

A minimal library for plotting training progress in Jupyter/COLAB notebooks.

## Installation

pip install tinyGraphs

## Usage

```python

train_losses, val_losses = [], []
epochs = 3

for epoch in range(epochs):
    # Training
    model.train()
    running_train_loss = 0
    for x, y in train_loader:
        x, y = x.to(device), y.to(device)
        optimizer.zero_grad()
        loss = criterion(model(x), y)
        loss.backward()
        optimizer.step()
        running_train_loss += loss.item()
    train_losses.append(running_train_loss / len(train_loader))

    # Validation
    model.eval()
    running_val_loss = 0
    with torch.no_grad():
        for x, y in val_loader:
            x, y = x.to(device), y.to(device)
            loss = criterion(model(x), y)
            running_val_loss += loss.item()
    val_losses.append(running_val_loss / len(val_loader))

    # Plot using tinyGraphs
    plot_training_progress(train_losses, val_losses, epoch, y_max = 0.5)