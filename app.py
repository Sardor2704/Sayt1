import os
from flask import Flask, render_template, request
from duckduckgo_search import DDGS

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html', results=[], query="")

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    results = []
    if query:
        try:
            # Qidiruvni amalga oshirish
            with DDGS() as ddgs:
                results_gen = ddgs.text(query, max_results=15)
                for r in results_gen:
                    results.append({
                        'title': r['title'],
                        'link': r['href'],
                        'snippet': r.get('body', r.get('snippet', ''))
                    })
        except Exception as e:
            print(f"Xato yuz berdi: {e}")
            
    return render_template('index.html', results=results, query=query)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
