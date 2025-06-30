from flask import Flask, request, render_template_string, url_for, jsonify, make_response
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import TextAreaField, FileField
from wtforms.validators import Optional
from collections import Counter
import re
import os

app = Flask(__name__, static_url_path='/static')
app.secret_key = os.environ.get('flask-secret-key', 'change_this_secret_key')#add fallback for local testing.
csrf = CSRFProtect(app)

# HTML template for the upload form
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Log File Brute Force Analyzer</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <h2>Log File Brute Force Analyzer2</h2>
    <form method="post" enctype="multipart/form-data">
        {{ form.csrf_token }}
        <p>Upload .txt file:</p>
        {{ form.file() }}
        <p>Or paste log content:</p>
        {{ form.log_content(rows=10, cols=50) }}
        <input type="submit" value="Analyze">
    </form>
    {% if results %}
    <div class="results">
        <h3>Analysis Results:</h3>
        <pre>{{ results }}</pre>
    </div>
    {% endif %}
</body>
</html>
'''

class LogForm(FlaskForm):
    file = FileField('file', validators=[Optional()])
    log_content = TextAreaField('log_content', validators=[Optional()])

def analyze_logs(log_content):
    """
    Analyze log content for potential brute force attacks
    Basic detection: Counts failed login attempts per IP
    Returns: Analysis results as string
    """
    # Simple regex to match IP addresses (basic pattern)
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    
    # Find all IPs in the log content
    ips = re.findall(ip_pattern, log_content)
    
    # Count occurrences of each IP
    ip_counts = Counter(ips)
    
    # Check for potential brute force attempts (threshold: 5 attempts)
    suspicious_ips = {ip: count for ip, count in ip_counts.items() if count >= 5}
    
    if not suspicious_ips:
        return "No suspicious activity detected."
    
    result = "Potential brute force attempts detected:\n"
    for ip, count in suspicious_ips.items():
        result += f"IP: {ip} - {count} attempts\n"
    return result

@app.after_request
def set_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'self' 'unsafe-inline';"
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, private'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    # Remove or obfuscate server version info
    response.headers['Server'] = 'SecureServer'
    return response

@app.route('/', methods=['GET', 'POST'])
def home():
    form = LogForm()
    results = None
    if form.validate_on_submit():
        if form.file.data and form.file.data.filename:
            # Handle file upload
            file = form.file.data
            if not file.filename.endswith('.txt'):
                return "Only .txt files are allowed!"
            log_content = file.read().decode('utf-8')
        elif form.log_content.data:
            # Handle pasted content
            log_content = form.log_content.data
        else:
            return "No content provided!"
            
        results = analyze_logs(log_content)
    return render_template_string(HTML_TEMPLATE, form=form, results=results)

@app.route('/api/analyze', methods=['POST'])
@csrf.exempt  # Exempt API from CSRF for programmatic access
def api_analyze():
    """
    REST API endpoint to analyze log content for brute force attempts.
    Expects JSON: {"logs": "<log text>"}
    Returns: JSON with suspicious IPs and attempt counts.
    """
    data = request.get_json()
    if not data or 'logs' not in data:
        return jsonify({"error": "Missing 'logs' in request body."}), 400
    log_content = data['logs']
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    ips = re.findall(ip_pattern, log_content)
    ip_counts = Counter(ips)
    suspicious_ips = {ip: count for ip, count in ip_counts.items() if count >= 5}
    return jsonify({"suspicious_ips": suspicious_ips, "total_ips": len(ip_counts)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
