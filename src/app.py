#!/usr/bin/env python3
#from psycopg2cffi import compat; compat.register()
from flask import Flask, jsonify
from dotenv import load_dotenv, find_dotenv
import os
import datetime
from src.model.connection.ConexaoProd import ConexaoProd
from src.model.connection.ConexaoAuth import ConexaoAuth
from src.model.DAO.OcorrenciaDAO import OcorrenciaDAO, Ocorrencia
from src.model.DAO.AuthDAO import AuthDAO
from src.model.DAO.UsuarioDAO import UsuarioDAO

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


db_auth = ConexaoProd(app)
ocorrenciaDAO = OcorrenciaDAO(db_auth)


now = datetime.datetime.now()
sql_datetime = now.strftime('%Y-%m-%d %H:%M:%S')#formato de data utilizado pelo BD



@app.route("/")
def hello_world():

     return (ocorrenciaDAO.getOcorrencias())
