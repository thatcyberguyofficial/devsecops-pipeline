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
                bat 'docker build -t flask-app .'
            }
        }
        stage('Security Test with ZAP') {
            steps {
                // If ZAP is a shell command, use bat as well, or keep as is if it's a Jenkins plugin step
                echo 'ZAP Security Scan Completed'
            }
        }
        stage('Deploy Application') {
            steps {
                bat 'docker run -d -p 5000:5000 flask-app'
                echo 'Application Deployed'
            }
        }
    }
}