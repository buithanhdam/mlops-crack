# data_ingestion.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os
from src.utils import get_logger
logger = get_logger()
class DataIngestion:
    """
    Class để đọc và phân chia dữ liệu Iris dataset
    """
    def __init__(self, raw_data_path='data/raw/Iris.csv', 
                 processed_data_path='data/processed'):
        self.raw_data_path = raw_data_path
        self.processed_data_path = processed_data_path
        
        # Tạo thư mục processed nếu chưa tồn tại
        if not os.path.exists(processed_data_path):
            os.makedirs(processed_data_path)

    def read_data(self):
        """Đọc dữ liệu từ file CSV"""
        try:
            df = pd.read_csv(self.raw_data_path)
            logger.info("Đã đọc dữ liệu thành công")
            return df
        except Exception as e:
            logger.error(f"Lỗi khi đọc dữ liệu: {e}")
            raise

    def split_data(self, df, test_size=0.2, random_state=42):
        """Phân chia dữ liệu thành tập train và test"""
        try:
            # Tách features và target
            X = df.drop(['Species', 'Id'], axis=1)
            y = df['Species']
            
            # Phân chia dữ liệu
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=random_state, stratify=y
            )
            
            logger.info("Đã phân chia dữ liệu thành công")
            return X_train, X_test, y_train, y_test
        except Exception as e:
            logger.error(f"Lỗi khi phân chia dữ liệu: {e}")
            raise

    def save_splits(self, X_train, X_test, y_train, y_test):
        """Lưu các phần dữ liệu đã phân chia"""
        try:
            # Lưu training data
            train_df = X_train.copy()
            train_df['Species'] = y_train
            train_df.to_csv(os.path.join(self.processed_data_path, 'train.csv'), 
                           index=False)
            
            # Lưu testing data
            test_df = X_test.copy()
            test_df['Species'] = y_test
            test_df.to_csv(os.path.join(self.processed_data_path, 'test.csv'), 
                          index=False)
            
            logger.info("Đã lưu dữ liệu đã phân chia thành công")
        except Exception as e:
            logger.error(f"Lỗi khi lưu dữ liệu: {e}")
            raise

    def run_ingestion(self):
        """Chạy toàn bộ quá trình ingestion"""
        try:
            # Đọc dữ liệu
            df = self.read_data()
            
            # Phân chia dữ liệu
            X_train, X_test, y_train, y_test = self.split_data(df)
            
            # Lưu dữ liệu đã phân chia
            self.save_splits(X_train, X_test, y_train, y_test)
            logger.info("Ingestion pipeline successfully")
            return X_train, X_test, y_train, y_test
        except Exception as e:
            logger.error(f"Lỗi trong quá trình ingestion: {e}")
            raise