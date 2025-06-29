# DevSecOps Pipeline Demo

This project demonstrates a simple DevSecOps pipeline using a Flask API, Docker, Jenkins, and integrated security testing (DAST).

## Features
- **Flask API**: Simple RESTful API (see `app.py`).
- **Dockerized**: Containerized application for easy deployment.
- **Jenkins Pipeline**: Automated CI/CD pipeline with security checks.
- **Security Testing**:
  - **DAST**: OWASP ZAP (dynamic analysis, see pipeline)

## Pipeline Overview
1. **Clone Repo**: Pulls the latest code from GitHub.
2. **Build Docker Image**: Builds the Flask app image.
3. **DAST with ZAP**: Scans running app for web vulnerabilities (report: `zap-report.html`).
4. **Deploy**: Runs the app in a Docker container.

## Getting Started

### Prerequisites
- Docker
- Jenkins (with Docker access)
- Python 3.x (for local development)

### Running Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

### Building & Running with Docker
```bash
docker build -t flask-app .
docker run -d -p 5000:5000 flask-app
```

### Jenkins Pipeline
- The `Jenkinsfile` defines all pipeline steps.
- Security reports are archived as build artifacts.

## Security Documentation
- See `THREAT_MODEL.md` for a simple threat model.
- API documentation is in `API.md` or inline in `app.py`.

## License
MIT
