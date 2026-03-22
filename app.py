import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates')

def search_wikipedia(query):
    """Wikipedia-dan ma'lumot qidirish (Bloklanmaydi)"""
    results = []
    try:
        url = f"https://uz.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "utf8": 1
        }
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        for item in data['query']['search'][:10]:
            results.append({
                'title': item['title'],
                'href': f"https://uz.wikipedia.org/wiki/{item['title'].replace(' ', '_')}",
                'body': item['snippet'].replace('<span class="searchmatch">', '').replace('</span>', '') + "..."
            })
    except:
        pass
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    query = ""
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            # Birinchi Wikipedia-dan qidiramiz (aniq natija beradi)
            results = search_wikipedia(query)
            
            # Agar Wikipedia-dan kam natija bo'lsa, Google/DuckDuckGo muqobilini qo'shamiz
            # (Hozircha Wikipedia eng ishonchlisi)
            
    return render_template('index.html', results=results, query=query)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
