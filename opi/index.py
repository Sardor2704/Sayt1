import os
import requests
from flask import Flask, render_template, request

# Vercel-da templates papkasini topish uchun yo'l ko'rsatamiz
app = Flask(__name__, template_folder='../templates')

def search_wiki(query):
    results = []
    try:
        # Wikipedia API (O'zbek, Rus va Ingliz tillari uchun)
        url = "https://uz.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "utf8": 1
        }
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        
        for item in data.get('query', {}).get('search', []):
            results.append({
                'title': item['title'],
                'href': f"https://uz.wikipedia.org/wiki/{item['title'].replace(' ', '_')}",
                'body': item['snippet'].replace('<span class="searchmatch">', '').replace('</span>', '') + "..."
            })
    except Exception as e:
        print(f"Xato: {e}")
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    query = ""
    if request.method == 'POST':
        query = request.form.get('query', '')
        if query:
            results = search_wiki(query)
    return render_template('index.html', results=results, query=query)

# Vercel serverless function sifatida ishlashi uchun zarur
app = app
