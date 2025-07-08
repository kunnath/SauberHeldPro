"""
Aufraumenbee - Vercel Deployment Handler
This file is optimized for Vercel serverless deployment using Flask.
"""

from flask import Flask, render_template_string
from datetime import datetime
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Aufraumenbee - Cleaning Service</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        header {
            background-color: #4CAF50;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        h1, h2 {
            color: #4CAF50;
        }
        .info-box {
            background-color: #e7f3fe;
            border-left: 6px solid #2196F3;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }
        .contact {
            background-color: #f5f5f5;
            padding: 20px;
            border-radius: 5px;
            margin-top: 30px;
        }
    </style>
</head>
<body>
    <header>
        <h1>🧹 Aufraumenbee Cleaning Services</h1>
    </header>
    
    <main>
        <h2>Welcome to Aufraumenbee Professional Cleaning Services</h2>
        <p>We provide top-quality cleaning services for homes and businesses.</p>
        
        <div class="info-box">
            <p>This is a lightweight version of our application optimized for Vercel deployment.</p>
            <p>Due to Vercel's 250MB function size limit, this is a reduced version of our application.</p>
            <p>For the full experience, please visit our main application or use the locally hosted version.</p>
        </div>
        
        <p>Current Time: {{ current_time }}</p>
        <p>Deployment Environment: {{ env }}</p>
        
        <div class="contact">
            <h2>Contact Us</h2>
            <p>For bookings and inquiries, please contact us at:</p>
            <p>📧 Email: contact@aufraumenbee.com</p>
            <p>📞 Phone: +1-234-567-8900</p>
        </div>
    </main>
</body>
</html>
"""

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    env = os.environ.get('VERCEL_ENV', 'Development')
    
    return render_template_string(
        HTML_TEMPLATE, 
        current_time=current_time,
        env=env
    )

if __name__ == "__main__":
    app.run(debug=True)
