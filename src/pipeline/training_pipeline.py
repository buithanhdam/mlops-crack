from omegaconf import DictConfig
from src.utils import get_logger
from src.data import DVCRemoteManager
from src.models import ModelTrainer
from hydra import compose, initialize
logger = get_logger()
manager = DVCRemoteManager()

def train_pipeline(config: DictConfig):
    """Train the model."""
    try:
        manager.pull_from_s3()
        manager.check_remote_status()
        logger.info("Starting training pipeline")
        trainer = ModelTrainer(config)
        trainer.train()
        model_file_path = trainer.save_model()
        manager.add_file(model_file_path)
        manager.push_to_s3()
            
        logger.info("Training completed successfully")
    except Exception as e:
        logger.error(f"Error during training: {str(e)}")
        raise e

if __name__ == "__main__":
    train_pipeline()