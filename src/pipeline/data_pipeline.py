import os
from src.data import DVCRemoteManager, DataIngestion, DataTransformer
import hydra
from omegaconf import DictConfig
from src.utils import get_logger
logger = get_logger()
manager = DVCRemoteManager()

@hydra.main(version_base='1.3',config_path="../../configs/", config_name="config")
def data_version_update(config: DictConfig):
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
        
@hydra.main(version_base='1.3',config_path="../../configs/", config_name="config")
def data_preprocessing_pipeline(config: DictConfig):
    
    manager.pull_from_s3()
    # Chạy data ingestion
    logger.info("Starting ingestion data")
    ingestion = DataIngestion(config)
    ingestion.run_ingestion()
        
    # Track processed data với DVC
    manager.add_file('data/processed')
    manager.push_to_s3()
    # Chạy data transformation
    logger.info("Starting transformer data")
    transformer = DataTransformer(config)
    transformer.run_transformation()
        
    # Track transformed data với DVC
    manager.add_file('data/transformed')
        
    # Push lên S3
    manager.push_to_s3()
    logger.info("Test data pipeline successfully")


if __name__ == "__main__":
    # data_version_update()
    data_preprocessing_pipeline()