import os
import subprocess
from dotenv import load_dotenv
load_dotenv()
from src.utils import get_logger
logger = get_logger()
class DVCRemoteManager:
    def __init__(self):
        # Kiểm tra xem có file .dvc/config không
        if not os.path.exists('.dvc/config'):
            logger.error("File .dvc/config not found. Make sure you in correct project path")
            raise Exception("File .dvc/config not found. Make sure you in correct project path")

    def add_file(self, file_path):
        try:
            subprocess.run(['dvc', 'add', file_path], check=True)
            logger.info(f"Adding file successfully with {file_path} in DVC tracking")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error when adding file: {e}")
            raise

    def push_to_s3(self):
        try:
            subprocess.run(['dvc', 'push'], check=True)
            logger.info("Push data to s3 successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error when push data to s3: {e}")
            raise

    def pull_from_s3(self):
        try:
            subprocess.run(['dvc', 'pull'], check=True)
            logger.info("Pull data from s3 successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error when pull data from s3: {e}")
            raise

    def set_aws_credentials(self, aws_access_key, aws_secret_key):
        os.environ['AWS_ACCESS_KEY_ID'] = aws_access_key
        os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_key
        logger.info("Initialize AWS credentials key successfully")

    def check_remote_status(self):
        try:
            subprocess.run(['dvc', 'remote', 'list'], check=True)
            logger.info("\nList of tracking file:")
            subprocess.run(['dvc', 'list', '.'])
        except subprocess.CalledProcessError as e:
            logger.error(f"Error when checking remote: {e}")
            raise