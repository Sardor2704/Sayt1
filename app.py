import os
from flask import Flask, render_template, request
from duckduckgo_search import DDGS

# Render va Flask uchun papka manzillarini to'g'ri ko'rsatamiz
app = Flask(__name__, template_folder='templates')

def deep_search(query, file_type="all"):
    results = []
    # Qidiruv operatorlari (PDF, Word, Excel, Video uchun)
    operators = {
        "pdf": "filetype:pdf",
        "word": "(filetype:doc OR filetype:docx)",
        "excel": "(filetype:xls OR filetype:xlsx)",
        "video": "(filetype:mp4 OR filetype:mkv OR filetype:avi)",
        "all": ""
    }
    
    full_query = f"{query} {operators.get(file_type, '')}"
    try:
        # DuckDuckGo orqali qidiruvni amalga oshiramiz
        with DDGS() as ddgs:
            search_results = [r for r in ddgs.text(full_query, safesearch='off', max_results=30)]
            for r in search_results:
                results.append({
                    'title': r['title'], 
                    'link': r['href'], 
                    'snippet': r.get('body', '')
                })
    except Exception as e:
        print(f"Xato yuz berdi: {e}")
        pass
    return results

# Asosiy sahifa yuklanganda
@app.route('/')
def index():
    return render_template('index.html', results=[], query="")

# Qidiruv tugmasi bosilganda (POST so'rovi)
@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    f_type = request.form.get('type', 'all')
    results = []
    if query:
        results = deep_search(query, f_type)
    # Natijalarni index.html ga qaytaramiz
    return render_template('index.html', results=results, query=query)

if __name__ == "__main__":
    # Render serveri talab qiladigan port sozlamasi
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
