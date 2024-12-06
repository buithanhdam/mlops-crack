# MLOps Crack
A comprehensive self-learning MLOps course repository with practical implementations and resources.

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
   - [Clone the Repository](#1-clone-the-repository)
   - [Set Up Virtual Environment](#2-set-up-virtual-environment)
   - [Install Dependencies](#3-install-dependencies)
   - [Configure DVC with S3 Bucket](#4-configure-dvc-with-s3-bucket)
3. [Configuration](#configuration)
   - [Config Structure](#config-structure)
   - [Configuration Details](#configuration-details)
4. [Testing](#testing)
   - [Testing Data Pipeline (Ingestion and Transformer)](#testing-data-pipeline-ingestion-and-transformer)
   - [Testing Training Pipeline (Build, Train, Evaluate)](#testing-training-pipeline-build-train-evaluate)
5. [Security Notice](#security-notice)
6. [Prerequisites](#prerequisites)
7. [Contact](#contact)

## Overview

This repository provides materials and code to learn MLOps practices and tools through hands-on experience. It covers essential topics such as data pipeline, model training, and deployment using industry-standard tools and frameworks.

## Installation

Follow these steps to set up the project:

### **1. Clone the Repository**

Clone the repository to your local machine:

```bash
git clone https://github.com/buithanhdam/mlops-crack.git
cd mlops-crack
```

### **2. Set Up Virtual Environment**

Set up a virtual environment to isolate dependencies for the project.

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

Once the virtual environment is active, install the required dependencies:

```bash
pip install -r requirements.txt
```

### **4. Configure DVC with S3 Bucket**

DVC (Data Version Control) is used for managing datasets and model versioning. To set it up with S3:

1. **Initialize DVC**:
```bash
dvc init -f
```

2. **Add S3 Remote Storage**:
```bash
dvc remote add -d <remote-name> <s3-bucket-link>
```

3. **Set up AWS Credentials**:
   - Create a directory for AWS credentials:
```bash
mkdir .aws
touch .aws/credentials
```

   - Add your AWS credentials to the `.aws/credentials` file:
```ini
[default]
aws_access_key_id = your-access-key
aws_secret_access_key = your-secret-key
```

4. **Create a data folder**:
   Create the necessary directories to store your data:
```bash
mkdir data
cd data
mkdir raw
```

   Then, place your data files in the `raw` directory.

## Configuration

The project uses **Hydra** for configuration management. Configuration files are organized in the `configs` directory.

### Config Structure

```bash
configs/
├── config.yaml           # Main configuration file
├── data/
│   └── default.yaml      # Data processing settings
├── model/
│   └── default.yaml      # Model configuration
└── training/
    └── default.yaml      # Training parameters
```

### Configuration Details

1. **Main Config** (`configs/config.yaml`):
   - Defines base paths, MLflow settings, and default configurations.

2. **Data Config** (`configs/data/default.yaml`):
   - Specifies paths and processing parameters for data.
   - Controls train/validation/test splits.
   - Defines data file and label column names.

3. **Model Config** (`configs/model/default.yaml`):
   - Contains settings for model architecture and hyperparameters.
   - Configures model-specific parameters (e.g., Random Forest).

4. **Training Config** (`configs/training/default.yaml`):
   - Defines training parameters such as batch size, epochs, and learning rate.
   - Includes early stopping configuration.

## Testing

### **Testing Data Pipeline (Ingestion and Transformer)**

To test the data pipeline:

1. Update the `configs/data/default.yaml` file:
   - Set the `data_file` to the name of your data file (e.g., `Iris.csv`).
   - Set the `label_col` to the column name of the target label (e.g., `Species`).
   
2. Run the data pipeline:
```bash
python3 src/pipeline/data_pipeline.py
```

### **Testing Training Pipeline (Build, Train, Evaluate)**

To test the training pipeline:

1. Update the `configs/model/default.yaml` file to include your model and parameters. You can choose from models such as:
   - `random_forest`
   - `svm`
   - `logistic_regression`
   - `knn`

2. Run the training pipeline:
```bash
python3 src/pipeline/training_pipeline.py
```

## Security Notice

- **AWS credentials**: Ensure your AWS credentials are secure. Never commit them to version control.
- Add `.aws/` to your `.gitignore` file to prevent AWS credentials from being tracked by Git.
- Use **environment variables** or **AWS IAM roles** for credentials in production environments.

## Prerequisites

Before starting, ensure you have the following installed:

- Python 3.9 or higher
- Git
- An AWS account with S3 access
- Basic understanding of machine learning concepts
- Hydra for configuration management

## Contact
For questions or support, please open an issue on the [GitHub repository](https://github.com/buithanhdam/mlops-crack/issues).
