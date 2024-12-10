import os
from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from src.pipeline import data_preprocessing_pipeline, train_pipeline, predict_pipeline
from hydra import compose, initialize
from omegaconf import DictConfig, OmegaConf
from src.utils import get_logger
app = FastAPI()
logger = get_logger()


def get_config() -> DictConfig:
    try:
        with initialize(version_base="1.3", config_path="configs", job_name="mlops-crack"):
            config = compose(config_name="config", return_hydra_config=True)
            logger.info(f"Config loaded successfully at: {os.getcwd()}")
            logger.info(f"Resolved config: {OmegaConf.to_yaml(config)}")  # Log the resolved config
            OmegaConf.resolve(config)
            return config 
    except Exception as e:
        logger.error(f"Error during Hydra config initialization: {e}")
        raise

# Đường dẫn tới thư mục chứa template HTML
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="templates"), name="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Trang chủ để test các pipeline"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/data_pipeline")
async def run_data_pipeline(
    hydra_config: DictConfig = Depends(get_config)
):
    """Chạy data pipeline"""
    try:
        data_preprocessing_pipeline(hydra_config)
        return {"status": "Data pipeline executed successfully"}
    except Exception as e:
        logger.error(f"Error executing data pipeline: {e}")
        return {"status": "Failed to execute data pipeline", "error": str(e)}

@app.post("/training_pipeline")
async def run_training_pipeline(
    hydra_config: DictConfig = Depends(get_config)
):
    """Chạy training pipeline"""
    try:
        train_pipeline(hydra_config)
        return {"status": "Training pipeline executed successfully"}
    except Exception as e:
        logger.error(f"Error executing training pipeline: {e}")
        return {"status": "Failed to execute training pipeline", "error": str(e)}

@app.post("/prediction_pipeline")
async def run_prediction_pipeline(
    hydra_config: DictConfig = Depends(get_config)
):
    """Chạy prediction pipeline"""
    try:
        predict_pipeline(hydra_config)
        return {"status": "Prediction pipeline executed successfully"}
    except Exception as e:
        logger.error(f"Error executing prediction pipeline: {e}")
        return {"status": "Failed to execute prediction pipeline", "error": str(e)}
