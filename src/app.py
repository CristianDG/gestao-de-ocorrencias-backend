#!/usr/bin/env python3
<<<<<<< HEAD
from flask import Flask, request
from controllers import OcorrenciaController
=======
from psycopg2cffi import compat; compat.register()
from flask import Flask, jsonify
from dotenv import load_dotenv, find_dotenv
import os
import datetime
from model.connection.ConexaoProd import ConexaoProd
from model.connection.ConexaoAuth import ConexaoAuth
from model.DAO.OcorrenciaDAO import OcorrenciaDAO, Ocorrencia
from model.DAO.AuthDAO import AuthDAO
from model.DAO.UsuarioDAO import UsuarioDAO
>>>>>>> main

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


db_auth = ConexaoAuth(app)
usuarioDAO = UsuarioDAO(db_auth)



@app.route("/")
def hello_world():
    # TODO: Swagger ou Frontend?
    return "teste2"

@app.get("/ocorrencias")
def listar_ocorrencias():
    return OcorrenciaController.listar()

@app.post("/ocorrencias")
def registrar_ocorrencia():
    ocorrencia = request.get_json()

    if not ocorrencia['descricao']:
        return {'error': 'descrição inválida'}, 401

    # TODO: falta validar
    # - [ ] a existencia de todos os campos

    return OcorrenciaController.registrar(ocorrencia)

@app.patch("/ocorrencias/<int:id_ocorrencia>/<int:id_setor>")
def encaminhar_ocorrencia(id_ocorrencia, id_setor):

    # TODO: falta validar
    # - [ ] token jwt para gestor

    return OcorrenciaController.encaminhar(id_ocorrencia, id_setor)
