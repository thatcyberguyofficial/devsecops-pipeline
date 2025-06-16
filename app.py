from flask import Flask, request, render_template_string, url_for
from collections import Counter
import re

app = Flask(__name__, static_url_path='/static')

# HTML template for the upload form
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Log File Brute Force Analyzer</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <h2>Log File Brute Force Analyzer</h2>
    <form method="post" enctype="multipart/form-data">
        <p>Upload .txt file:</p>
        <input type="file" name="file" accept=".txt">
        <p>Or paste log content:</p>
        <textarea name="log_content" rows="10" cols="50"></textarea>
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

@app.route('/', methods=['GET', 'POST'])
def home():
    results = None
    if request.method == 'POST':
        if 'file' in request.files and request.files['file'].filename:
            # Handle file upload
            file = request.files['file']
            if not file.filename.endswith('.txt'):
                return "Only .txt files are allowed!"
            log_content = file.read().decode('utf-8')
        elif request.form.get('log_content'):
            # Handle pasted content
            log_content = request.form.get('log_content')
        else:
            return "No content provided!"
            
        results = analyze_logs(log_content)
    
    return render_template_string(HTML_TEMPLATE, results=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
