import os
from flask import Flask, render_template, request
from duckduckgo_search import DDGS

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    query = ""
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            try:
                # Qidiruv parametrlarini maksimal darajada soddalashtiramiz
                with DDGS() as ddgs:
                    # 'wt-wt' dunyo bo'ylab, 'max_results' sonini kamaytirib ko'ramiz (tezlik uchun)
                    ddgs_gen = ddgs.text(query, region='wt-wt', safesearch='off')
                    for i, r in enumerate(ddgs_gen):
                        results.append({
                            'title': r['title'],
                            'href': r['href'],
                            'body': r['body']
                        })
                        if i >= 15: break # 15 ta natija yetarli
            except Exception as e:
                print(f"Xatolik yuz berdi: {e}")
                # Agar DuckDuckGo bloklasa, bu xato loglarda ko'rinadi
    
    return render_template('index.html', results=results, query=query)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
