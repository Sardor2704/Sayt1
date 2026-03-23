from flask import Flask, render_template, request
import requests

app = Flask(__name__, template_folder='../templates')

@app.route('/')
def index():
    query = request.args.get('query', '')
    results = []
    if query:
        url = "https://uz.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "utf8": 1
        }
        data = requests.get(url, params=params).json()
        for item in data.get('query', {}).get('search', []):
            results.append({
                'title': item['title'],
                'body': item['snippet']
            })
    return render_template('index.html', results=results, query=query)

# Vercel uchun juda muhim qator
app = app
