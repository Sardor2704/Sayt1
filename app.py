from flask import Flask, render_template, request
from duckduckgo_search import DDGS
import threading
import time

app = Flask(__name__)

def deep_search(query, file_type="all"):
    results = []
    operators = {
        "pdf": "filetype:pdf",
        "word": "(filetype:doc OR filetype:docx)",
        "excel": "(filetype:xls OR filetype:xlsx)",
        "video": "(filetype:mp4 OR filetype:mkv OR filetype:avi)",
        "all": ""
    }
    full_query = f"{query} {operators.get(file_type, '')}"
    try:
        with DDGS() as ddgs:
            search_results = [r for r in ddgs.text(full_query, safesearch='off', max_results=30)]
            for r in search_results:
                results.append({'title': r['title'], 'link': r['href'], 'snippet': r.get('body', '')})
    except:
        pass
    return results

@app.route('/')
def index():
    query = request.args.get('q')
    f_type = request.args.get('type', 'all')
    results = []
    if query:
        results = deep_search(query, f_type)
    return render_template('index.html', results=results, query=query)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
