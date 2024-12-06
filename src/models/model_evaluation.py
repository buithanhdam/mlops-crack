import os
import pickle
import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from omegaconf import DictConfig
from src.utils import get_logger
logger = get_logger()
class ModelEvaluation:
    def __init__(self, config: DictConfig):
        self.config = config
        self.transformed_data_path = config.data.transformed_data_path
        self.model_path = config.paths.models_dir
        self.model = self.load_model()
        self.scaler = joblib.load(os.path.join(self.transformed_data_path, 'scaler.joblib'))
        self.label_encoder = joblib.load(os.path.join(self.transformed_data_path, 'label_encoder.joblib'))
        self.metrics = {
            'accuracy': accuracy_score,
            'precision': precision_score,
            'recall': recall_score,
            'f1': f1_score
        }

    def load_model(self):
        model_file_path = os.path.join(self.model_path,"model.pkl")
        if os.path.exists(model_file_path):
            with open(model_file_path, "rb") as f:
                return pickle.load(f)
        else:
            raise FileNotFoundError(f"Model not found at {model_file_path}")
    def evaluate(self, X, y):
        X_scaled = self.scaler.transform(X)
        y_scaled = self.label_encoder.transform(y)
        y_pred = self.model.predict(X_scaled)
        metrics = {}
        for metric_name, metric_func in self.metrics.items():
            if metric_name == 'f1':
                metrics[metric_name] = metric_func(y_scaled, y_pred, average='weighted')
            else:
                metrics[metric_name] = metric_func(y_scaled, y_pred)
        return metrics

    def predict(self, X):
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)