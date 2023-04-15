#!/usr/bin/env python3
#from psycopg2cffi import compat; compat.register()
from flask import Flask, jsonify
from dotenv import load_dotenv, find_dotenv
import os
import datetime
from model.connection.ConexaoProd import ConexaoProd
from model.connection.ConexaoAuth import ConexaoAuth
from model.DAO.OcorrenciaDAO import OcorrenciaDAO, Ocorrencia
from model.DAO.AuthDAO import AuthDAO


app = Flask(__name__)

load_dotenv(find_dotenv(".env"))

#configuração das varáveis de ambiente de conexão com o banco DE PRODUÇÃO
app.config["PROD_DB_HOST"] = os.getenv("PROD_DB_HOST")
app.config["PROD_DB_NAME"] = os.getenv("PROD_DB_NAME")
app.config["PROD_DB_PASSWORD"] = os.getenv("PROD_DB_PASSWORD")
app.config["PROD_DB_PORT"] = os.getenv("PROD_DB_PORT")
app.config["PROD_DB_USER"] = os.getenv("PROD_DB_USER")
app.config["CLIENT_ENCODING"] = os.getenv("CLIENT_ENCODING")

    #configuração das varáveis de ambiente de conexão com o banco DE AUTENTICAÇÃO
app.config["AUTH_DB_HOST"] = os.getenv("AUTH_DB_HOST")
app.config["AUTH_DB_NAME"] = os.getenv("AUTH_DB_NAME")
app.config["AUTH_DB_PASSWORD"] = os.getenv("AUTH_DB_PASSWORD")
app.config["AUTH_DB_PORT"] = os.getenv("AUTH_DB_PORT")
app.config["AUTH_DB_USER"] = os.getenv("AUTH_DB_USER")


db = ConexaoAuth(app)
conexaoAUTH = AuthDAO(db)


now = datetime.datetime.now()
sql_datetime = now.strftime('%Y-%m-%d %H:%M:%S')#formato de data utilizado pelo BD



@app.route("/")
def hello_world():

    email = "asdkasnasdjk@gmail.com"
    senha = "askdjnaskdnkasd"
    conexaoAUTH.delete_user(1)
    id = conexaoAUTH.get_user(1)

    return f'{id}'
