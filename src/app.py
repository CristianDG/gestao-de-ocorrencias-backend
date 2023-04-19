#!/usr/bin/env python3
from psycopg2cffi import compat; compat.register()
from flask import Flask, jsonify, request, redirect, url_for, Blueprint
from dotenv import load_dotenv, find_dotenv
from functools import wraps
#from hashlib import sha256
import jwt
import os
import datetime
from controllers import OcorrenciaController, UsuarioController

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




def formatar_erro(erro):
    return ({'error': erro.args[0].value[0]}, erro.args[0].value[1])


def encode(dados):
    return jwt.encode(dados, os.getenv('JWT_SECRET'), algorithm='HS256')

def decode(dados):
    return jwt.decode(dados, os.getenv('JWT_SECRET'), algorithms=["HS256"])


def autenticar(cargos: list = []):
    cargos.append('gestor')
    def wrapper(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            erro = { 'error': 'não autorizado' }, 401

            if 'Authorization' not in request.headers:
                return erro

            # FIXME: acho que precisa de um controle pra não estourar
            id_usuario = int(decode(request.headers['Authorization'])['id'])

            if not UsuarioController.procurarPorId(id_usuario):
                return erro

            return fn(*args, **kwargs)

        return inner
    return wrapper


@app.route("/")
@autenticar()
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
        return {'error': 'descrição inválida'}, 400

    # TODO: falta validar
    # - [ ] a existencia de todos os campos

    return '', 201

@app.patch("/ocorrencias/<int:id_ocorrencia>/<int:id_setor>")
def encaminhar_ocorrencia(id_ocorrencia, id_setor):

    # TODO: falta validar
    # - [ ] token jwt para gestor

    try:
        return OcorrenciaController.encaminhar(id_ocorrencia, id_setor)
    except Exception as erro:
        return formatar_erro(erro)


@app.get('/login')
def login():
    usuario_json = request.get_json()

    if ('email' not in usuario_json or
        'senha' not in usuario_json or
        not UsuarioController.procurarPorLogin(usuario_json['email'], usuario_json['senha'])):

        return {'error': 'email ou senha incorretos'}, 400

    usuario = UsuarioController.procurarPorLogin(usuario_json['email'], usuario_json['senha'])
    token = encode({'id': usuario.id})

    return { 'token': token }, 200


@app.get('/usuarios')
def listar_usuarios():
    pass

@app.get('/usuarios/<id_usuario>')
def informacoes_usuario(id_usuario):
    pass

@app.post('/usuarios/<id_usuario>')
def registrar_usuario(id_usuario):
    pass

@app.post('/usuarios/<id_usuario>')
def modificar_usuario(id_usuario):
    pass
