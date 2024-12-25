# MLOps Crack

A comprehensive self-learning MLOps course repository with practical implementations and resources.

---

## Table of Contents

1. [Overview](#overview)  
2. [Installation](#installation)  
   - [Clone the Repository](#1-clone-the-repository)  
   - [Set Up Virtual Environment](#2-set-up-virtual-environment)  
   - [Install Dependencies](#3-install-dependencies)  
   - [Environment Configuration](#4-environment-configuration)  
   - [Configure DVC with S3 Bucket](#5-configure-dvc-with-s3-bucket)  
3. [Configuration](#configuration)  
   - [Config Structure](#config-structure)  
   - [Configuration Details](#configuration-details)  
4. [Testing](#testing)  
   - [Testing Data Pipeline](#testing-data-pipeline)  
   - [Testing Training Pipeline](#testing-training-pipeline)  
   - [Prediction Pipeline](#prediction-pipeline)  
5. [Run with Docker](#run-with-docker)  
   - [Build and Start Services](#build-and-start-services)  
   - [Stop Services](#stop-services)  
6. [Security Notice](#security-notice)  
7. [Prerequisites](#prerequisites)  
8. [Contact](#contact)  

---

## Overview

This repository is a comprehensive guide to learning MLOps through hands-on practices, covering topics such as data pipeline, model training, and deployment using tools like Docker, DVC, and MLflow.

---

## Installation

### **1. Clone the Repository**

Clone the repository to your local machine:

```bash
git clone https://github.com/buithanhdam/mlops-crack.git
cd mlops-crack
```

### **2. Set Up Virtual Environment**

#### For Unix/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### For Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```

### **3. Install Dependencies**

Install project dependencies:

```bash
pip install -r requirements.txt
```

### **4. Environment Configuration**

Create a `.env` file from the provided template:

```bash
cp .env.example .env
```

Edit `.env` and set your environment variables:

```env
MYSQL_DATABASE=mlops-crack
MYSQL_USER=user
MYSQL_PASSWORD=1
MYSQL_ROOT_PASSWORD=1
MYSQL_HOST=mysql
MYSQL_PORT=3306

AWS_ACCESS_KEY_ID=<your-aws-access-key-id>
AWS_SECRET_ACCESS_KEY=<your-aws-secret-access-key>
```

### **5. Configure DVC with S3 Bucket**

1. Initialize DVC:
```bash
dvc init
```

2. Add S3 as the remote storage:
```bash
dvc remote add -d s3remote s3://your-bucket-name
```

3. Configure AWS credentials:
   - Create a `.aws/credentials` file:
```bash
mkdir .aws
touch .aws/credentials
```

   - Add your AWS credentials:
```ini
[default]
aws_access_key_id = <your-access-key>
aws_secret_access_key = <your-secret-key>
```

4. Create the `data/raw` directory for datasets:
```bash
mkdir -p data/raw
```

Place your raw datasets in the `data/raw` folder.

---

## Configuration

### **Config Structure**

```bash
configs/
├── config.yaml           # Main config
├── data/default.yaml     # Data settings
├── model/default.yaml    # Model parameters
└── training/default.yaml # Training parameters
```

### **Configuration Details**

- **Main Config**: General project settings, including paths and MLflow configurations.  
- **Data Config**: Controls dataset paths, column names, and split ratios.  
- **Model Config**: Specifies architecture and hyperparameters.  
- **Training Config**: Defines batch size, epochs, learning rate, etc.

---

## Testing

### **Testing Data Pipeline**

1. Update `configs/data/default.yaml` with your dataset file and label column.
2. Run the data pipeline:
```bash
python3 src/pipeline/data_pipeline.py
```

### **Testing Training Pipeline**

1. Update `configs/model/default.yaml` with the model of your choice (e.g., `random_forest`, `svm`).
2. Run the training pipeline:
```bash
python3 src/pipeline/training_pipeline.py
```

### **Prediction Pipeline**

Test the prediction process:
```bash
python3 src/pipeline/prediction_pipeline.py
```

---

## Run with Docker

### **Build and Start Services**

Build and start the services:
```bash
docker-compose up --build
```

Access services:
- **FastAPI**: `http://localhost:8000`  
- **MLflow**: `http://localhost:5000`  

### **Stop Services**

Stop all running containers:
```bash
docker-compose down
```

---

## Security Notice

- **Never commit credentials**: Use `.env` and `.aws` for sensitive information.
- Add `.env` and `.aws/` to `.gitignore`.

---

## Prerequisites

- Python 3.9+  
- Docker and Docker Compose  
- AWS account with S3 access  
- Basic understanding of ML concepts  

---

## Contact

For support, open an issue on the [GitHub repository](https://github.com/buithanhdam/mlops-crack/issues).