
# :fire: Torcheasy 0.0.1

**Torcheasy** is a lightweight tool designed to simplify model training with PyTorch.

This project consists of two main components: `Torcheasy.BaseConfig` and `Torcheasy.TrainableModule`. The `BaseConfig` is responsible for creating a unified project configuration, while `TrainableModule` provides a framework for implementing any module that extends `torch.nn.Module`.

## 1. Easy Configuration

In deep learning, managing hyperparameters is crucial. Torcheasy offers a simple way to configure these parameters:

```python
import torcheasy

config = torcheasy.BaseConfig()
config.add_param("batch_size", 16)
config.add_param("lr", 1e-4)
config.add_param("dim", 128)

batch_size = config.batch_size
...
```

Additionally, saving and loading configurations is straightforward:

```python
# Save the configuration
config.save("ModelA")
...
# Load the configuration
config = torcheasy.BaseConfig()
config.load("ModelA")

batch_size = config.batch_size
...
```

The configurations are saved as a JSON file at `ModelA/config.json`:

```json
{
  "batch_size": 16,
  "lr": 0.0001,
  "dim": 128
}
```

## 2. Easy Training

Training PyTorch models with Torcheasy is simple and intuitive:

```python
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torcheasy import TrainableModule, BaseConfig

# Define your model
class MyModel(TrainableModule):
    def __init__(self, config: BaseConfig):
        super().__init__(config)
        self.linear = nn.Linear(config.in_dim, config.out_dim)

    def forward(self, x):
        return self.linear(x)

# Define configurations
config = BaseConfig()
config.add_param("in_dim", 1)
config.add_param("out_dim", 16)
model = MyModel(config)

# Prepare your dataset
train_data = DataLoader(Dataset())  # Customize your train dataset
val_data = DataLoader(Dataset())  # Optional validation dataset
test_data = DataLoader(Dataset())  # Optional test dataset

model.prepare_data(train_data, test_data, val_data, config.batch_size)

# Start training
model.train_model(
    config.epoch, 
    torch.nn.MSELoss(), 
    optimizer=config.opt, 
    lr=config.lr,
    lr_scheduler=..., 
    early_stop=10
)
```

## 3. Easy Control

For more complex training processes, Torcheasy allows customization through various callback functions:

```python
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torcheasy import TrainableModule, BaseConfig

# Define your model
class MyModel(TrainableModule):
    def __init__(self, config: BaseConfig):
        super().__init__(config)
        self.linear = nn.Linear(config.in_dim, config.out_dim)

    def forward(self, x):
        return self.linear(x)

    # Override this method to customize the loss computation
    # The default loss computation looks like this:
    def compute_loss(self, x: torch.Tensor, y: torch.Tensor, criterion) -> torch.Tensor:
        return self.compute_loss(x, y, criterion)
    
    # Actions to perform at the start of each iteration
    def iter_start(self, iteration):
        print("Iteration started.")
        
    # Actions to perform before the optimizer's backward pass
    def iter_end_before_opt(self, iteration):
        print("Iteration ended.")
    
    # Actions to perform before training starts
    def train_start(self):
        print("Training started.")
    
    # Additional customization points...
    ...
```
## More advanced features are still updating!

---