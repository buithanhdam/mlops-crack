# data_validation.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import os
import joblib
from src.utils import get_logger
logger = get_logger()
class DataTransformer:
    def __init__(self, processed_data_path='data/processed', 
                 transformed_data_path='data/transformed'):
        self.processed_data_path = processed_data_path
        self.transformed_data_path = transformed_data_path
        
        # Tạo thư mục transformed nếu chưa tồn tại
        if not os.path.exists(transformed_data_path):
            os.makedirs(transformed_data_path)
        
        self.scaler = StandardScaler()

    def load_data(self):
        try:
            # Đọc training data
            train_df = pd.read_csv(os.path.join(self.processed_data_path, 'train.csv'))
            
            # Đọc testing data
            test_df = pd.read_csv(os.path.join(self.processed_data_path, 'test.csv'))
            
            # Tách features và target
            X_train = train_df.drop('Species', axis=1)
            y_train = train_df['Species']
            X_test = test_df.drop('Species', axis=1)
            y_test = test_df['Species']
            
            logger.info("Đã load dữ liệu thành công")
            return X_train, X_test, y_train, y_test
        except Exception as e:
            logger.error(f"Lỗi khi load dữ liệu: {e}")
            raise

    def transform_features(self, X_train, X_test):
        try:
            # Fit scaler trên training data và transform cả train/test
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Chuyển về DataFrame để giữ tên cột
            X_train_scaled = pd.DataFrame(X_train_scaled, 
                                        columns=X_train.columns, 
                                        index=X_train.index)
            X_test_scaled = pd.DataFrame(X_test_scaled, 
                                       columns=X_test.columns, 
                                       index=X_test.index)
            
            logger.info("Đã transform features thành công")
            return X_train_scaled, X_test_scaled
        except Exception as e:
            logger.error(f"Lỗi khi transform features: {e}")
            raise

    def save_transformed_data(self, X_train_scaled, X_test_scaled, y_train, y_test):
        try:
            # Lưu training data
            train_df = X_train_scaled.copy()
            train_df['Species'] = y_train
            train_df.to_csv(os.path.join(self.transformed_data_path, 'train_transformed.csv'), 
                           index=False)
            
            # Lưu testing data
            test_df = X_test_scaled.copy()
            test_df['Species'] = y_test
            test_df.to_csv(os.path.join(self.transformed_data_path, 'test_transformed.csv'), 
                          index=False)
            
            # Lưu scaler
            joblib.dump(self.scaler, 
                       os.path.join(self.transformed_data_path, 'scaler.joblib'))
            
            logger.info("Đã lưu dữ liệu đã transform thành công")
        except Exception as e:
            logger.error(f"Lỗi khi lưu dữ liệu transformed: {e}")
            raise

    def run_transformation(self):
        try:
            # Load dữ liệu
            X_train, X_test, y_train, y_test = self.load_data()
            
            # Transform features
            X_train_scaled, X_test_scaled = self.transform_features(X_train, X_test)
            
            # Lưu dữ liệu đã transform
            self.save_transformed_data(X_train_scaled, X_test_scaled, y_train, y_test)
            logger.info("Transformer pipeline successfully")
            return X_train_scaled, X_test_scaled, y_train, y_test
        except Exception as e:
            logger.error(f"Lỗi trong quá trình transformation: {e}")
            raise