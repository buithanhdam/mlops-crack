import os
from src.data import DVCRemoteManager, DataIngestion, DataTransformer
import mlflow
from hydra import compose, initialize
from src.utils import get_logger
from omegaconf import DictConfig
logger = get_logger()
manager = DVCRemoteManager()

def data_version_update_pipeline(config: DictConfig):
    try:
        logger.info("Starting push new data file to s3 remote by DVC")
            # manager.set_aws_credentials(
            #     aws_access_key='your-access-key',
            #     aws_secret_key='your-secret-key'
            # )
        manager.add_file(os.path.join(config.data.raw_data_path, config.data.data_file))
        manager.push_to_s3()
        manager.check_remote_status()
    except Exception as e:
        logger.error(f"Có lỗi xảy ra: {e}")
        
def data_preprocessing_pipeline(config: DictConfig):
    with mlflow.start_run(run_name="data_preprocessing_pipeline"):
        try:
            # Bước 1: Kéo dữ liệu từ S3
            manager.pull_from_s3()
            mlflow.log_param("raw_data_path", config.data.raw_data_path)
            mlflow.log_param("data_file_name", config.data.data_file)
            mlflow.log_param("label_col", config.data.label_col)
            logger.info("Pulled data from S3 successfully")
                
            # Bước 2: Data ingestion
            logger.info("Starting ingestion data")
            ingestion = DataIngestion(config)
            ingestion.run_ingestion()
                
            mlflow.log_param("train_ratio", config.data.train_ratio)
            mlflow.log_param("test_ratio", config.data.test_ratio)
            mlflow.log_param("val_ratio", config.data.val_ratio)
            mlflow.log_param("random_state", config.data.random_state)
            mlflow.log_artifacts(config.data.processed_data_path, artifact_path="processed_data")

            # Bước 3: Track processed data với DVC
            manager.add_file('data/processed')
            manager.push_to_s3()

            # Bước 4: Data transformation
            logger.info("Starting transformer data")
            transformer = DataTransformer(config)
            transformer.run_transformation()
            mlflow.log_artifacts(config.data.transformed_data_path, artifact_path="transformed_data")

            # Push transformed data lên S3
            manager.add_file('data/transformed')
            manager.push_to_s3()

            logger.info("Data preprocessing pipeline completed successfully")
        except Exception as e:
            logger.error(f"Error in data preprocessing pipeline: {e}")
            mlflow.log_param("error", str(e))
            raise

if __name__ == "__main__":
    # data_version_update()
    data_preprocessing_pipeline()