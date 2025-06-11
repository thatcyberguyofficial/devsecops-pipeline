// This Jenkinsfile defines a pipeline for a DevSecOps workflow
// that clones a repository, builds a Docker image, runs a security test using ZAP,
// and deploys the application.
pipeline {
    agent any
    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/thatcyberguyofficial/devsecops-pipeline.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t flask-app .'
            }
        }
        stage('Security Test with ZAP') {
            steps {
                zap {
                    targetUrl 'http://localhost:5000'
                    failBuildAfterThreshold(5)
                }
                echo 'ZAP Security Scan Completed'
            }
        }
        stage('Deploy Application') {
            steps {
                sh 'docker run -d -p 5000:5000 flask-app'
                echo 'Application Deployed'
            }
        }
    }
}
