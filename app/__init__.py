import os
import sqlite3
from flask import Flask, render_template

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY='...'
)
BASE_DIR = os.path.dirname(app.instance_path)





@app.route('/')
def index():
    return render_template('index.html')
