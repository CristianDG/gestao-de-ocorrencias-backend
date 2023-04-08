#!/usr/bin/env python3
from flask import Flask
from dotenv import load_dotenv, find_dotenv
import os
from model.connection.ConexaoPSQL import ConexaoPSQL
from model.DAO.OcorrenciaDAO import OcorrenciaDAO


app = Flask(__name__)

load_dotenv(find_dotenv(".env"))

#configuração das varáveis de ambiente de conexão com o banco
app.config["PSQL_DB_HOST"] = os.getenv("PSQL_DB_HOST")
app.config["PSQL_DB_NAME"] = os.getenv("PSQL_DB_NAME")
app.config["PSQL_DB_PASSWORD"] = os.getenv("PSQL_DB_PASSWORD")
app.config["PSQL_DB_PORT"] = os.getenv("PSQL_DB_PORT")
app.config["PSQL_DB_USER"] = os.getenv("PSQL_DB_USER")


db = ConexaoPSQL(app)
ocorrenciaDAO = OcorrenciaDAO(db)




@app.route("/")
def hello_world():
    busca = ocorrenciaDAO.buscar_todas_ocorrencias()
    # Retorna o resultado da consulta como uma string
    return f"{busca}"
