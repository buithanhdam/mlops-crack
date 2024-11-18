# src/training/train.py
import hydra
import mlflow
from omegaconf import DictConfig
import logging

logger = logging.getLogger(__name__)

@hydra.main(config_path="../../configs", config_name="config")
def train(config: DictConfig) -> None:
    """Train the model."""
    try:
        mlflow.set_tracking_uri(config.mlflow.tracking_uri)
        mlflow.set_experiment(config.mlflow.experiment_name)
        
        with mlflow.start_run():
            # Log configuration
            mlflow.log_params(dict(config.model.params))
            
            # Load data
            # train_data = load_data(config.data.processed_data_path)
            
            # Train model
            # model = train_model(train_data, config.model.params)
            
            # Evaluate
            # metrics = evaluate_model(model, test_data)
            # mlflow.log_metrics(metrics)
            
            # Save model
            # mlflow.sklearn.log_model(model, "model")
            
            logger.info("Training completed successfully")
            
    except Exception as e:
        logger.error(f"Error during training: {str(e)}")
        raise e

if __name__ == "__main__":
    train()