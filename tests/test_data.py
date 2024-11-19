from src.data import DVCRemoteManager, DataIngestion, DataTransformer
from src.utils import get_logger
logger = get_logger()
def main():
    try:
        logger.info("Starting test data")
        # Khởi tạo DVC manager
        manager = DVCRemoteManager()
        # Thiết lập AWS credentials (nếu chưa được cấu hình trong environment)
        # manager.set_aws_credentials(
        #     aws_access_key='your-access-key',
        #     aws_secret_key='your-secret-key'
        # )

        # Ví dụ sử dụng
        # 1. Thêm file mới vào tracking
        # manager.add_file('data/raw/Iris.csv')

        # 2. Push lên S3
        # manager.push_to_s3()
        # Pull data từ S3
        manager.pull_from_s3()
        
        # Chạy data ingestion
        logger.info("Starting ingestion data")
        ingestion = DataIngestion()
        X_train, X_test, y_train, y_test = ingestion.run_ingestion()
        
        # Track processed data với DVC
        manager.add_file('data/processed')
        
        # Chạy data transformation
        logger.info("Starting transformer data")
        transformer = DataTransformer()
        X_train_scaled, X_test_scaled, y_train, y_test = transformer.run_transformation()
        
        # Track transformed data với DVC
        manager.add_file('data/transformed')
        
        # Push lên S3
        manager.push_to_s3()
        logger.info("Test data successfully")
    except Exception as e:
        logger.error(f"Có lỗi xảy ra: {e}")

if __name__ == "__main__":
    main()