from flask import Flask,render_template, request, redirect, jsonify
from dotenv import load_dotenv
import requests
import base64
import os


load_dotenv()

app = Flask(__name__)



@app.route('/')
def home():
    return render_template("index.html")

@app.route('/analyze', methods=['POST'])
def upload_file():

    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error':'no file'})
        file = request.files['file']

        if file.filename == ' ':
            return jsonify({'error': 'no file'})
        image_data = base64.b64encode(file.read()).decode('utf-8')

        api_key = os.getenv('ANTHROPIC_API_KEY') 

        headers = {
        "x-api-key" : api_key ,
        "anthropic-version" : "2023-06-01" ,
        "content-type" : "application/json" ,
        }

        body = {
        "model": "claude-haiku-4-5",
        "max_tokens" : 500,
        "messages": [
            {"role": "user", "content":"Hello, Claude"}
        ]
        }

        response = requests.post('https://api.anthropic.com/v1/messages', headers=headers, json=body)
        
        return jsonify(response.json())
        
        

if __name__ == '__main__':

    app.run(debug=True)