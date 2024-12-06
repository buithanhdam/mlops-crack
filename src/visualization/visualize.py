import hydra
import matplotlib.pyplot as plt
import os
from omegaconf import DictConfig
from src.utils import get_logger
logger = get_logger()
@hydra.main(version_base='1.3', config_path="../../configs/", config_name="config")
def visualize_metrics(train_metrics, val_metrics, test_metrics, config: DictConfig):

    os.makedirs(config.paths.visualization_dir, exist_ok=True)
    file_path = os.path.join(config.paths.visualization_dir, "plot_metrics.png")

    plt.figure(figsize=(12, 6))

    # Plot accuracy
    plt.subplot(1, 2, 1)
    plt.plot(train_metrics['accuracy'], label='Training')
    plt.plot(val_metrics['accuracy'], label='Validation')
    plt.plot(test_metrics['accuracy'], label='Test')
    plt.title('Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()

    # Plot F1-score
    plt.subplot(1, 2, 2)
    plt.plot(train_metrics['f1'], label='Training')
    plt.plot(val_metrics['f1'], label='Validation')
    plt.plot(test_metrics['f1'], label='Test')
    plt.title('F1-score')
    plt.xlabel('Epoch')
    plt.ylabel('F1-score')
    plt.legend()

    plt.tight_layout()

    # Lưu hình ảnh
    plt.savefig(file_path, dpi=300)
    logger.info(f"Metrics plot saved to {file_path}")
