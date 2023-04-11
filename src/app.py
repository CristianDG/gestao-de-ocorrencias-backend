#!/usr/bin/env python3
from flask import Flask, jsonify
from dotenv import load_dotenv, find_dotenv
import os
import datetime
from model.connection.ConexaoPSQL import ConexaoPSQL
from model.DAO.OcorrenciaDAO import OcorrenciaDAO, Ocorrencia


app = Flask(__name__)

load_dotenv(find_dotenv(".env"))

#configuração das varáveis de ambiente de conexão com o banco
app.config["PSQL_DB_HOST"] = os.getenv("PSQL_DB_HOST")
app.config["PSQL_DB_NAME"] = os.getenv("PSQL_DB_NAME")
app.config["PSQL_DB_PASSWORD"] = os.getenv("PSQL_DB_PASSWORD")
app.config["PSQL_DB_PORT"] = os.getenv("PSQL_DB_PORT")
app.config["PSQL_DB_USER"] = os.getenv("PSQL_DB_USER")
app.config["CLIENT_ENCODING"] = os.getenv("CLIENT_ENCODING")


db = ConexaoPSQL(app)
ocorrenciaDAO = OcorrenciaDAO(db)



now = datetime.datetime.now()
sql_datetime = now.strftime('%Y-%m-%d %H:%M:%S')#formato de data utilizado pelo BD



@app.route("/")
def hello_world():

    ocorrencia = Ocorrencia("'teste'", "'teste'", "'teste'", "'Ativo'", sql_datetime, None, 1, 1)
    ocorrencias = ocorrenciaDAO.criar_ocorrencia(ocorrencia)
    ocorrencias_dict = None
    #Converte a lista de ocorrências em um dicionário
    if ocorrencias == None:
        ocorrencias_dict = {"id":0, "value": None}
    else:
        ocorrencias_dict = [ocorrencia.__dict__ for ocorrencia in ocorrencias if ocorrencias is not None]
    #Retorna a lista de dicionários em forma de um json
    return jsonify(ocorrencias_dict)
