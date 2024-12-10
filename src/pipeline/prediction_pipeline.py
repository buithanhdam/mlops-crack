from omegaconf import DictConfig
from src.utils import get_logger
from src.models import ModelEvaluation
import pandas as pd
from src.data import DVCRemoteManager
from hydra import compose, initialize
logger = get_logger()
manager = DVCRemoteManager()

def predict_pipeline(config: DictConfig):
    try:
        manager.pull_from_s3()
        manager.check_remote_status()
        logger.info("Starting predict pipeline")
        evaluator = ModelEvaluation(config)
            
            # Load the data to be predicted
        cols = ["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"]
        values = [[6.1, 3.5, 2.0, 0.2]] 
        X_test = pd.DataFrame(columns=cols, data=values)
            
        logger.info(f"X_test data with shape: {X_test.shape} and values: \n{X_test}")
            # Make predictions
        y_pred = evaluator.predict(X_test)
        logger.info(f"Final predict label: {y_pred}")
        logger.info("Predict pipeline successfully!")
            
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise e

if __name__ == "__main__":
    predict_pipeline()