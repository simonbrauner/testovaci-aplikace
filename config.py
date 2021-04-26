"""
Testovací aplikace
Šimon Brauner
26.4.2021

config.py

Creating and configuring application
and accessing database.
"""


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with open('secret_key.txt', 'r') as file:
    app.secret_key = file.read()

db = SQLAlchemy(app)
