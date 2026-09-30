from flask import Flask, render_template, request, redirect
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DB = 'inventory.db'

def init_db():
    if not os.path.exists(DB):
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute('''CREATE TABLE devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            type TEXT,
            serial TEXT,
            purchase_date TEXT
        )''')
        c.execute('''CREATE TABLE software (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            licence_key TEXT,
            expiry_date TEXT
        )''')
        conn.commit()
        conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT * FROM devices')
    devices = c.fetchall()
    c.execute('SELECT * FROM software')
    software = c.fetchall()
    conn.close()
    return render_template('index.html', devices=devices, software=software)

@app.route('/add_device', methods=['POST'])
def add_device():
    name = request.form['name']
    type_ = request.form['type']
    serial = request.form['serial']
    purchase_date = request.form['purchase_date']
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('INSERT INTO devices (name,type,serial,purchase_date) VALUES (?,?,?,?)',
              (name,type_,serial,purchase_date))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
