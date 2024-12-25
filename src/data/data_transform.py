# src/data/data_transform.py
import mlflow
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
import os
import joblib
from omegaconf import DictConfig
from src.utils import get_logger

logger = get_logger()


class DataTransformer:
    """
    Class để xử lý và biến đổi dữ liệu Iris dataset sử dụng Hydra config
    """

    def __init__(self, config: DictConfig):
        """
        Args:
            config (DictConfig): Hydra config object
        """
        self.config = config
        self.processed_data_path = config.data.processed_data_path
        self.transformed_data_path = config.data.transformed_data_path
        self.data_file = config.data.data_file
        self.label_col = config.data.label_col
        # Tạo thư mục transformed nếu chưa tồn tại
        if not os.path.exists(self.transformed_data_path):
            os.makedirs(self.transformed_data_path)

        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()

    def load_data(self):
        """Load dữ liệu đã được phân chia"""
        try:
            # Đọc training data
            train_df = pd.read_csv(os.path.join(self.processed_data_path, "train.csv"))

            # Đọc validation data
            val_df = pd.read_csv(os.path.join(self.processed_data_path, "val.csv"))

            # Đọc testing data
            test_df = pd.read_csv(os.path.join(self.processed_data_path, "test.csv"))

            # Tách features và target
            X_train = train_df.drop(self.label_col, axis=1)
            y_train = train_df[self.label_col]
            X_val = val_df.drop(self.label_col, axis=1)
            y_val = val_df[self.label_col]
            X_test = test_df.drop(self.label_col, axis=1)
            y_test = test_df[self.label_col]

            logger.info("Đã load dữ liệu thành công")
            return X_train, X_val, X_test, y_train, y_val, y_test
        except Exception as e:
            logger.error(f"Lỗi khi load dữ liệu: {e}")
            raise

    def transform_features(self, X_train, X_val, X_test):
        """Chuẩn hóa features"""
        try:
            # Fit scaler trên training data và transform tất cả
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_val_scaled = self.scaler.transform(X_val)
            X_test_scaled = self.scaler.transform(X_test)

            # Chuyển về DataFrame để giữ tên cột
            X_train_scaled = pd.DataFrame(
                X_train_scaled, columns=X_train.columns, index=X_train.index
            )
            X_val_scaled = pd.DataFrame(
                X_val_scaled, columns=X_val.columns, index=X_val.index
            )
            X_test_scaled = pd.DataFrame(
                X_test_scaled, columns=X_test.columns, index=X_test.index
            )

            logger.info("Đã transform features thành công")
            return X_train_scaled, X_val_scaled, X_test_scaled
        except Exception as e:
            logger.error(f"Lỗi khi transform features: {e}")
            raise

    def transform_label(self, y_train, y_val, y_test):
        """Chuẩn hóa features"""
        try:
            # Fit scaler trên training data và transform tất cả
            y_train_scaled = self.label_encoder.fit_transform(y_train)
            y_val_scaled = self.label_encoder.transform(y_val)
            y_test_scaled = self.label_encoder.transform(y_test)

            logger.info("Đã transform features thành công")
            return y_train_scaled, y_val_scaled, y_test_scaled
        except Exception as e:
            logger.error(f"Lỗi khi transform label: {e}")
            raise

    def save_transformed_data(
        self, X_train_scaled, X_val_scaled, X_test_scaled, y_train, y_val, y_test
    ):
        """Lưu dữ liệu đã transform"""
        try:
            # Lưu training data
            train_df = X_train_scaled.copy()
            train_df[self.label_col] = y_train
            train_df.to_csv(
                os.path.join(self.transformed_data_path, "train_transformed.csv"),
                index=False,
            )

            # Lưu validation data
            val_df = X_val_scaled.copy()
            val_df[self.label_col] = y_val
            val_df.to_csv(
                os.path.join(self.transformed_data_path, "val_transformed.csv"),
                index=False,
            )

            # Lưu testing data
            test_df = X_test_scaled.copy()
            test_df[self.label_col] = y_test
            test_df.to_csv(
                os.path.join(self.transformed_data_path, "test_transformed.csv"),
                index=False,
            )

            # Lưu scaler
            joblib.dump(
                self.scaler, os.path.join(self.transformed_data_path, "scaler.joblib")
            )
            joblib.dump(
                self.label_encoder,
                os.path.join(self.transformed_data_path, "label_encoder.joblib"),
            )
            mlflow.log_artifacts(
                    self.transformed_data_path, artifact_path="transformed_data"
                )
            logger.info("Đã lưu dữ liệu đã transform thành công")
        except Exception as e:
            logger.error(f"Lỗi khi lưu dữ liệu transformed: {e}")
            raise

    def run_transformation(self):
        try:
            # Load dữ liệu
            X_train, X_val, X_test, y_train, y_val, y_test = self.load_data()

            # Transform features
            X_train_scaled, X_val_scaled, X_test_scaled = self.transform_features(
                X_train, X_val, X_test
            )
            y_train_scaled, y_val_scaled, y_test_scaled = self.transform_label(
                y_train, y_val, y_test
            )

            # Lưu dữ liệu đã transform
            self.save_transformed_data(
                X_train_scaled,
                X_val_scaled,
                X_test_scaled,
                y_train_scaled,
                y_val_scaled,
                y_test_scaled,
            )
            logger.info("Transformation pipeline running successfully")
            return (
                X_train_scaled,
                X_val_scaled,
                X_test_scaled,
                y_train_scaled,
                y_val_scaled,
                y_test_scaled,
            )
        except Exception as e:
            logger.error(f"Error in data transformation: {e}")
            raise
