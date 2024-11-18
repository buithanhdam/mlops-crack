// Jenkinsfile
pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'mlops-app'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh '''
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh 'python -m pytest tests/'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
            }
        }
        
        stage('Run Container Tests') {
            steps {
                sh "docker run ${DOCKER_IMAGE}:${DOCKER_TAG} python -m pytest tests/"
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                echo 'Deploying...'
                // Add deployment steps here
                // For example: push to registry, deploy to k8s, etc.
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}