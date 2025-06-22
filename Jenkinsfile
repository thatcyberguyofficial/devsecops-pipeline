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
                // Run a ZAP scan and generate the zap-report.html file.
                bat 'docker run --rm -v %cd%:/zap/wrk:rw -t owasp/zap2docker-stable zap-baseline.py -t http://host.docker.internal:5000 -r zap-report.html'
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