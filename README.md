# MLOps Crack

A comprehensive self-learning MLOps course repository with practical implementations and resources.

## Overview

This repository contains materials and code for learning MLOps practices and tools through hands-on experience.

## Installation

Follow these steps to set up the project:

### **1. Clone the Repository**

```bash
git clone https://github.com/buithanhdam/mlops-crack.git
cd mlops-crack
```

### **2. Set Up Virtual Environment**

Choose the appropriate command based on your operating system:

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

```bash
pip install -r requirements.txt
```

### **4. Configure DVC with S3 Bucket**

#### Initialize DVC:
```bash
dvc init -f
dvc remote add -d <remote-name> <s3-bucket-link>
```

#### Set up AWS Credentials:
1. Create AWS credentials directory:
```bash
mkdir .aws
touch .aws/credentials
```

2. Add your AWS credentials to `.aws/credentials`:
```ini
[default]
aws_access_key_id = your-access-key
aws_secret_access_key = your-secret-key
```

#### Create a data folder in same path of root project `./mlops-crack/data` and put your data file here
## Security Notice

- Keep your AWS credentials secure and never commit them to version control
- Add `.aws/` to your `.gitignore` file
- Use environment variables or AWS IAM roles in production environments

## Prerequisites

- Python 3.9 or higher
- Git
- AWS account with S3 access
- Basic understanding of ML concepts

## Contact

For questions or support, please open an issue in the repository.