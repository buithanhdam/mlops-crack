# setup.py
from setuptools import find_packages, setup

setup(
    name="mlops-template",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
        "mlflow>=2.0.0",
        "dvc[s3]",  # Add appropriate remote storage
        "hydra-core",  # For configuration management
        "python-dotenv",
        "typer",  # For CLI
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "black",
            "flake8",
            "isort",
            "pre-commit",
        ],
    },
    python_requires=">=3.9",
)