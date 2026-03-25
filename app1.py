from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__, template_folder='templates', static_folder='static1')

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            result TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_history(url, result):
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute("INSERT INTO history (url, result) VALUES (?, ?)", (url, result))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute("SELECT url, result FROM history")
    data = c.fetchall()
    conn.close()
    return data

init_db()

# ---------- DATA ----------
data = {"total": 0, "safe": 0, "suspicious": 0, "dangerous": 0}

# ---------- ROUTES ----------
@app.route('/')
def home():
    history = get_history()
    return render_template('dashboard.html', data=data, history=history)

@app.route('/scan', methods=['POST'])
def scan():
    url = request.form.get('url')

    if "https" in url:
        result = "SAFE ✅"
        data["safe"] += 1
    else:
        result = "DANGEROUS ⚠️"
        data["dangerous"] += 1

    data["total"] += 1

    insert_history(url, result)
    history = get_history()

    return render_template('dashboard.html', data=data, result=result, url=url, history=history)

@app.route('/bulk', methods=['POST'])
def bulk():
    urls = request.form.get('urls').splitlines()

    for url in urls:
        if url.strip() == "":
            continue

        if "https" in url:
            result = "SAFE ✅"
            data["safe"] += 1
        else:
            result = "DANGEROUS ⚠️"
            data["dangerous"] += 1

        data["total"] += 1
        insert_history(url, result)

    history = get_history()

    return render_template('dashboard.html', data=data, history=history)

if __name__ == '__main__':
    app.run(debug=True)