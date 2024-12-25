# src/data/data_ingestion.py
import mlflow
import pandas as pd
from sklearn.model_selection import train_test_split
import os
from omegaconf import DictConfig
from src.utils import get_logger

logger = get_logger()


class DataIngestion:

    def __init__(self, config: DictConfig):
        self.config = config
        self.raw_data_path = config.data.raw_data_path
        self.processed_data_path = config.data.processed_data_path
        self.data_file = config.data.data_file
        self.label_col = config.data.label_col
        # Tạo thư mục processed nếu chưa tồn tại
        if not os.path.exists(self.processed_data_path):
            os.makedirs(self.processed_data_path)

    def read_data(self):
        try:
            df = pd.read_csv(os.path.join(self.raw_data_path, self.data_file))
            mlflow.log_param("raw_data_path", self.raw_data_path)
            mlflow.log_param("data_file_name", self.data_file)
            mlflow.log_param("label_col", self.label_col)
            logger.info("Đã đọc dữ liệu thành công")
            return df
        except Exception as e:
            logger.error(f"Lỗi khi đọc dữ liệu: {e}")
            mlflow.log_param("error_read_data", str(e))
            raise

    def split_data(self, df):
        try:
            # Tách features và target
            X = df.drop([self.label_col, "Id"], axis=1)
            y = df[self.label_col]

            # Phân chia train và temp
            X_train, X_temp, y_train, y_temp = train_test_split(
                X,
                y,
                train_size=self.config.data.train_ratio,
                random_state=self.config.data.random_state,
                stratify=y,
            )

            # Phân chia temp thành validation và test
            val_ratio = self.config.data.val_ratio / (1 - self.config.data.train_ratio)
            X_val, X_test, y_val, y_test = train_test_split(
                X_temp,
                y_temp,
                train_size=val_ratio,
                random_state=self.config.data.random_state,
                stratify=y_temp,
            )
            mlflow.log_param("train_ratio", self.config.data.train_ratio)
            mlflow.log_param("test_ratio", self.config.data.test_ratio)
            mlflow.log_param("val_ratio", self.config.data.val_ratio)
            mlflow.log_param("random_state", self.config.data.random_state)

            logger.info("Đã phân chia dữ liệu thành công")
            return X_train, X_val, X_test, y_train, y_val, y_test
        except Exception as e:
            logger.error(f"Lỗi khi phân chia dữ liệu: {e}")
            mlflow.log_param("error_split_data", str(e))
            raise

    def save_splits(self, X_train, X_val, X_test, y_train, y_val, y_test):
        try:
            # Lưu training data
            train_df = X_train.copy()
            train_df[self.label_col] = y_train
            train_df.to_csv(
                os.path.join(self.processed_data_path, "train.csv"), index=False
            )

            # Lưu validation data
            val_df = X_val.copy()
            val_df[self.label_col] = y_val
            val_df.to_csv(
                os.path.join(self.processed_data_path, "val.csv"), index=False
            )

            # Lưu testing data
            test_df = X_test.copy()
            test_df[self.label_col] = y_test
            test_df.to_csv(
                os.path.join(self.processed_data_path, "test.csv"), index=False
            )
            mlflow.log_artifacts(
                    self.processed_data_path, artifact_path="processed_data"
                )
            logger.info("Đã lưu dữ liệu đã phân chia thành công")
        except Exception as e:
            logger.error(f"Lỗi khi lưu dữ liệu: {e}")
            raise

    def run_ingestion(self):
        try:

            # Đọc dữ liệu
            df = self.read_data()
            mlflow.log_metric("total_rows", len(df))
            mlflow.log_metric("total_columns", df.shape[1])

            # Phân chia dữ liệu
            X_train, X_val, X_test, y_train, y_val, y_test = self.split_data(df)
            mlflow.log_metric("train_samples", len(X_train))
            mlflow.log_metric("val_samples", len(X_val))
            mlflow.log_metric("test_samples", len(X_test))

            # Lưu dữ liệu đã phân chia
            self.save_splits(X_train, X_val, X_test, y_train, y_val, y_test)
            logger.info("Ingestion pipeline running successfully")

            return X_train, X_val, X_test, y_train, y_val, y_test
        except Exception as e:
            logger.error(f"Error in data ingestion: {e}")
            raise
