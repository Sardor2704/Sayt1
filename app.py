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
            with DDGS() as ddgs:
                # Oddiyroq va barqaror qidiruv usuli
                ddgs_gen = ddgs.text(query, region='wt-wt', safesearch='off', timelimit='y')
                for i, r in enumerate(ddgs_gen):
                    if i >= 15: break  # Top 15 natija
                    results.append({
                        'title': r['title'],
                        'link': r['href'],
                        'snippet': r['body']
                    })
        except Exception as e:
            print(f"Xato: {e}")
            
    return render_template('index.html', results=results, query=query)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
