from typing import Tuple
from collections.abc import Sequence

import torch
from torch import Tensor
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingWarmRestarts
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm

from .models import NeuralPoissonNMF


def poisson_nmf_loss(X: Tensor, X_reconstructed: Tensor) -> Tensor:
    """
    Compute the Poisson NMF loss function (negative log-likelihood).

    Args:
        X: Original document-term matrix.
        X_reconstructed: Reconstructed matrix from the model.

    Returns:
        The computed Poisson NMF loss.
    """
    epsilon: float = 1e-10
    return (
        X_reconstructed - X * torch.log(torch.clamp(X_reconstructed, min=epsilon))
    ).sum()


class IndexTrackingDataset(Dataset):
    """Dataset wrapper that tracks indices through shuffling"""

    def __init__(self, dataset: Dataset | Tensor) -> None:
        self.dataset = dataset
        self.shape: tuple[int, int] = (
            dataset.shape
            if hasattr(dataset, "shape")
            else (len(dataset), dataset[0].shape[0])
        )
        self.is_tensor: bool = isinstance(dataset, torch.Tensor)

    def __len__(self) -> int:
        return len(self.dataset)

    def __getitem__(self, idx: int) -> tuple[Tensor, Tensor]:
        return self.dataset[idx], torch.tensor(idx)


def fit_model(
    X: Tensor | Dataset,
    k: int,
    num_epochs: int = 200,
    batch_size: int = 16,
    base_lr: float = 0.01,
    max_lr: float = 0.05,
    T_0: int = 20,
    T_mult: int = 1,
    weight_decay: float = 1e-5,
    device: torch.device | None = None,
) -> Tuple[NeuralPoissonNMF, Sequence[float]]:
    """
    Fit topic model using sum-to-one constrained neural Poisson NMF.
    Supports both in-memory tensors and custom datasets.

    Args:
        X: Input data, can be:

            - `torch.Tensor`: In-memory document-term matrix.
            - `Dataset`: Custom dataset implementation.
              For example, see `NumpyDiskDataset`.

        k: Number of topics.
        num_epochs: Number of training epochs.
        batch_size: Number of documents per batch.
        base_lr: Minimum learning rate after annealing.
        max_lr: Starting maximum learning rate.
        T_0: Number of epochs until first restart
        T_mult: Factor increasing restart interval.
        weight_decay: Weight decay for AdamW optimizer.
        device: Device to run training on.

    Returns:
        Tuple containing:

            - Trained NeuralPoissonNMF model.
            - List of training losses per epoch.
    """
    device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Handle different input types
    if isinstance(X, Dataset):
        base_dataset = X
        n = len(X)
        m = X.num_terms if hasattr(X, "num_terms") else X[0].shape[0]
    else:  # torch.Tensor
        X = X.to(device)
        n, m = X.shape
        base_dataset = X  # Pass tensor directly

    # Wrap dataset to track indices
    dataset = IndexTrackingDataset(base_dataset)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    model = NeuralPoissonNMF(n=n, m=m, k=k, device=device)
    optimizer = AdamW(model.parameters(), lr=max_lr, weight_decay=weight_decay)
    scheduler = CosineAnnealingWarmRestarts(
        optimizer, T_0=T_0, T_mult=T_mult, eta_min=base_lr
    )

    losses: Sequence[float] = []
    num_batches: int = len(dataloader)

    with tqdm(total=num_epochs, desc="Training Progress") as pbar:
        for epoch in range(num_epochs):
            epoch_loss: float = 0.0

            for batch_i, (batch_X, batch_indices) in enumerate(dataloader):
                batch_X = batch_X.to(device)
                batch_indices = batch_indices.to(device)

                optimizer.zero_grad()
                X_reconstructed = model(batch_indices)
                loss = poisson_nmf_loss(batch_X, X_reconstructed)
                loss.backward()
                optimizer.step()

                # Update per batch for cosine annealing with restarts
                scheduler.step(epoch + batch_i / num_batches)

                epoch_loss += loss.item()

            epoch_loss /= num_batches
            losses.append(epoch_loss)
            pbar.set_postfix({"Loss": f"{epoch_loss:.4f}"})
            pbar.update(1)

    return model, losses
