#!/usr/bin/env python3
from flask import Flask
from dotenv import load_dotenv, find_dotenv
from model.connection.ConexaoPSQL import ConexaoPSQL
import os

app = Flask(__name__)

load_dotenv(find_dotenv(".env"))

app.config["PSQL_DB_HOST"] = os.getenv("PSQL_DB_HOST")
app.config["PSQL_DB_NAME"] = os.getenv("PSQL_DB_NAME")
app.config["PSQL_DB_PASSWORD"] = os.getenv("PSQL_DB_PASSWORD")
app.config["PSQL_DB_PORT"] = os.getenv("PSQL_DB_PORT")
app.config["PSQL_DB_USER"] = os.getenv("PSQL_DB_USER")

print(app.config.values())

db = ConexaoPSQL(app)


@app.route("/")
def hello_world():
    # Executa uma consulta SQL simples para testar a conexão com o banco de dados
    result = db.executa_query("SELECT * FROM solve.ocorrencia", None)

    # Retorna o resultado da consulta como uma string
    return str(result)
