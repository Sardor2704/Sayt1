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
                # DDGS orqali universal qidiruv
                with DDGS() as ddgs:
                    # 'wt-wt' - barcha regionlar va tillar bo'yicha qidiradi (Uz, Ru, En)
                    res_gen = ddgs.text(
                        query, 
                        region='wt-wt', 
                        safesearch='off', 
                        max_results=25
                    )
                    for r in res_gen:
                        results.append({
                            'title': r['title'],
                            'href': r['href'],
                            'body': r.get('body', '')
                        })
            except Exception as e:
                print(f"Xato: {e}")
    
    return render_template('index.html', results=results, query=query)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
