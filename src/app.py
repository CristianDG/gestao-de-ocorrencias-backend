#!/usr/bin/env python3
from flask import Flask
from dotenv import load_dotenv, find_dotenv
from model.connection.ConexaoPSQL import ConexaoPSQL


app = Flask(__name__)

load_dotenv(find_dotenv())

print(app.config.values())

db = ConexaoPSQL(app)

query = "SELECT * FROM solve.ocorrencia;"
params = None
db.conectar()




@app.route("/")
def hello_world():
    return print(db.executa_query(query, params))
