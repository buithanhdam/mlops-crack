import os
import pickle
import hydra
import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from omegaconf import DictConfig
from src.utils import get_logger

logger = get_logger()
class ModelTrainer:
    def __init__(self, config: DictConfig):
        self.config = config
        self.model = None
        self.model_path = config.paths.models_dir
        self.transformed_data_path = config.data.transformed_data_path
        self.scaler = None
        self.metrics = {
            'accuracy': accuracy_score,
            'precision': precision_score,
            'recall': recall_score,
            'f1': f1_score
        }
    def load_transformed_data(self):
        """Load dữ liệu đã được transform"""
        try:
            # Đọc training data
            X_train = pd.read_csv(os.path.join(self.transformed_data_path, 'train_transformed.csv'))
            y_train = X_train[self.config.data.label_col]
            X_train = X_train.drop(self.config.data.label_col, axis=1)

            # Đọc validation data
            X_val = pd.read_csv(os.path.join(self.transformed_data_path, 'val_transformed.csv'))
            y_val = X_val[self.config.data.label_col]
            X_val = X_val.drop(self.config.data.label_col, axis=1)

            # Đọc testing data
            X_test = pd.read_csv(os.path.join(self.transformed_data_path, 'test_transformed.csv'))
            y_test = X_test[self.config.data.label_col]
            X_test = X_test.drop(self.config.data.label_col, axis=1)
            
            # Load scaler
            self.scaler = joblib.load(os.path.join(self.transformed_data_path, 'scaler.joblib'))

            logger.info("Đã load dữ liệu Train và Test đã transform thành công")
            return X_train, X_val, X_test, y_train, y_val, y_test
        except Exception as e:
            logger.error(f"Lỗi khi load dữ liệu đã transform: {e}")
            raise
    def train(self):
        try:
            X_train, X_val, X_test, y_train, y_val, y_test = self.load_transformed_data()
            self.model = self._build_model()
            logger.info(f"Starting model training with model.fit(X_train, y_train)")
            self.model.fit(X_train, y_train)
            logger.info(f"Model training with model.fit(X_train, y_train) successfully!")
            
            train_metrics = self.evaluate(X_train, y_train)
            logger.info(f"Training successfully with training metrics: {train_metrics}")
            val_metrics = self.evaluate(X_val, y_val)
            logger.info(f"Training successfully with validation metrics: {val_metrics}")
            test_metrics = self.evaluate(X_test, y_test)
            logger.info(f"Training successfully with test metrics: {test_metrics}")
            
            return train_metrics, val_metrics, test_metrics
        except Exception as e:
            logger.error(f"Lỗi trong quá trình training: {e}")
            raise
    def evaluate(self, X, y):
        y_pred = self.model.predict(X)
            
        metrics = {}
        for metric_name, metric_func in self.metrics.items():
            if metric_name in ['precision', 'recall', 'f1']:
                metrics[metric_name] = metric_func(y, y_pred, average='macro')
            else:
                metrics[metric_name] = metric_func(y, y_pred)
        return metrics
    def save_model(self):
        """
        Save the trained model to the specified path.

        Returns:
        str: Path to the saved model.
        """
        if self.model is None:
            raise ValueError("Model has not been trained. Cannot save.")

        # Tạo đường dẫn đầy đủ với tên file
        model_file_path = os.path.join(self.model_path,"model.pkl")

        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(self.model_path, exist_ok=True)

        with open(model_file_path, "wb") as f:
            pickle.dump(self.model, f)
        logger.info(f"Model saved successfully at {model_file_path}")
        return model_file_path
    def _build_model(self):
        """
        Build the model based on the configuration.

        Returns:
        sklearn.base.BaseEstimator: The model instance
        """
        model_params = get_model_params(self.config.model)
        model_name = self.config.default_model
        if model_name not in model_params:
            raise ValueError(f"Model name '{model_name}' is not supported.")

        model_class = hydra.utils.get_class(model_params[model_name]["class"])
        model_args = model_params[model_name]["params"]

        return model_class(**model_args)

def get_model_params(config: DictConfig) -> dict:
    model_params = {}
    for model_name, model_info in config.items():
        if isinstance(model_info, DictConfig):
            model_params[model_name] = {
                "class": model_info.model,
                "params": model_info.params
            }
    return model_params