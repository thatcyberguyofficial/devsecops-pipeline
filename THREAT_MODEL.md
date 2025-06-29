# Threat Model

This project analyzes SSH logs for brute force attempts. Below is a simple threat model for the application and pipeline.

## Assets
- SSH log files
- Flask API and web interface
- Docker container
- Jenkins pipeline

## Threats
- Brute force attacks against SSH (detected by the app)
- Malicious log uploads (attempting to exploit the analyzer)
- Unauthorized access to the API or pipeline
- Cross-Site Request Forgery (CSRF) attacks due to missing anti-CSRF tokens
- Cross-Site Scripting (XSS), clickjacking, and other attacks due to missing security headers (CSP, X-Frame-Options, Permissions-Policy, X-Content-Type-Options)
- Information disclosure via server version in HTTP headers
- Sensitive data exposure due to improper cache control

## Mitigations
- Input validation on logs
- No code execution on uploaded logs
- (Optional) Add authentication to API endpoints
- Use Docker to isolate the app
- Security testing in CI/CD pipeline (DAST)
- Implement anti-CSRF tokens in forms and validate them server-side
- Set security headers: Content-Security-Policy, X-Frame-Options, Permissions-Policy, X-Content-Type-Options, and others as appropriate
- Suppress or obfuscate server version information in HTTP response headers
- Set cache control headers (Cache-Control: no-store, no-cache, must-revalidate, private) for sensitive responses

## Assumptions
- The app is not exposed to the public internet without proper controls
- Only trusted users can access Jenkins and the API
