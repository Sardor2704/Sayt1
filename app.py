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
                # Blokirovkani chetlab o'tish uchun maxsus sozlamalar
                with DDGS(timeout=20) as ddgs:
                    # 'wt-wt' barcha tillar uchun
                    res_gen = ddgs.text(
                        query, 
                        region='wt-wt', 
                        safesearch='off', 
                        max_results=15
                    )
                    if res_gen:
                        results = [r for r in res_gen]
            except Exception as e:
                print(f"Qidiruvda xatolik: {e}")
                # Xatolik bo'lsa, foydalanuvchiga bo'sh ro'yxat qaytadi
    
    return render_template('index.html', results=results, query=query)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
