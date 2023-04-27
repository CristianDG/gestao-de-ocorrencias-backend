#!/usr/bin/env python3
#from psycopg2cffi import compat; compat.register()
from flask import Flask, jsonify, request, redirect, url_for, Blueprint
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
from functools import wraps
from hashlib import sha256
import jwt
import os
from datetime import datetime as dt, timedelta
from tipos import Usuario, Ocorrencia, Setor
from controllers import (
    OcorrenciaController,
    UsuarioController,
    SetorController,
    GestorController)


app = Flask(__name__)
CORS(app)

load_dotenv(find_dotenv(".env"))

if os.getenv('DEBUG'):
    print("#### DEBUG ATIVO ####")

@app.errorhandler(Exception)
def formatar_erro(erro):
    if os.getenv('DEBUG'):
        print(erro)
        return {'error': str(e)}, 500

    try:
        return ({'error': erro.args[0].value[0]}, erro.args[0].value[1])
    except Exception as e:
        if not os.getenv('DEBUG'):
            return {'error': 'internal server error'}, 500
        return {'error': str(e)}, 500


def verificar_existencia(campos: list[str], dic: dict) -> bool:
    res = True
    erro = None
    for campo in campos:
        res = (
            res and campo in dic
            and dic[campo] is not None
            and dic[campo] != '')

        if not res:
            erro = f'campo {campo} inválido ou não encontrado'
            break

    return erro

def encode(dados):
    return jwt.encode(dados, os.getenv('JWT_SECRET'), algorithm='HS256')

def decode(dados):
    return jwt.decode(dados, os.getenv('JWT_SECRET'), algorithms=["HS256"])

def criptografar(senha):
    return sha256(bytes(senha ,'utf8')).hexdigest()

def autenticar(gestor=False, admin=False):

    def wrapper(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            erro = { 'error': 'não autorizado' }, 401

            if 'Authorization' not in request.headers:
                return erro

            # FIXME: acho que precisa de um controle pra não estourar
            token = decode(request.headers['Authorization'])
            id_usuario = int(token['id'])

            # TODO: controlar se o token é antigo
            ttl_token = timedelta(hours=3)

            data_token = dt.fromtimestamp(token['data'])
            agora = dt.now()

            if (agora - data_token) > ttl_token:
                return erro

            # TODO: controlar se o usuário é gestor ou adm
            # FIXME: integrar com o banco de auth
            if not UsuarioController.procurarPorId(id_usuario):
                return erro

            # TODO: retornar o usuario que chamou o endpoint
            # FIXME: integrar com o banco de auth

            usuario = Usuario(email="sla@email.com", id=id_usuario)

            return fn(*args, **kwargs, usuario_solicitante=usuario)

        return inner
    return wrapper


@app.route("/")
@autenticar(gestor=True, admin=True)
def hello_world(usuario_solicitante):
    return 'admin' if usuario_solicitante.admin else 'gestor'

@app.get("/ocorrencias")
def listar_ocorrencias():
    # FIXME: como controlar qual é o setor?
    return OcorrenciaController.listar()

@app.post("/ocorrencias")
def registrar_ocorrencia():
    ocorrencia_json = request.get_json()

    erro = verificar_existencia(['descricao', 'id_local', 'id_setor'], ocorrencia_json)
    if erro:
        return {'error': erro}, 403



    dados_ocorrencia = {
        'email_cidadao' : ocorrencia_json.get('email_cidadao'),
        'nome_cidadao' : ocorrencia_json.get('nome_cidadao'),
        'descricao' : ocorrencia_json['descricao'],
        'id_local' : ocorrencia_json['id_local'],
        'id_setor' : ocorrencia_json['id_setor']
    }

    return OcorrenciaController.registrar(dados_ocorrencia), 201

@app.patch("/ocorrencias/<int:id_ocorrencia>/<int:id_setor>")
def encaminhar_ocorrencia(id_ocorrencia, id_setor):

    # TODO: falta validar
    # - [ ] token jwt para gestor

    return OcorrenciaController.encaminhar(id_ocorrencia, id_setor)


@app.post('/login')
def login():
    usuario_json = request.get_json()

    if ('email' not in usuario_json or
        'senha' not in usuario_json or
        not UsuarioController.procurarPorLogin(usuario_json['email'], usuario_json['senha'])):

        return {'error': 'email ou senha incorretos'}, 400

    usuario = UsuarioController.procurarPorLogin(usuario_json['email'], criptografar(usuario_json['senha']))
    token = encode({'id': usuario.id, 'data': dt.now().timestamp()})

    return { 'token': token }, 200


@app.get('/gestor')
def listar_gestores():
    pass

@app.get('/gestor/<int:id_gestor>')
def informacoes_gestor(id_gestor):
    pass

@app.post('/gestor')
def registrar_gestor():
    gestor_json = request.get_json()

    erro = verificar_existencia(
        ['email', 'senha', 'nome', 'sobrenome', 'status', 'id_setor'], gestor_json)

    if erro:
        return {'error': erro}, 403

    gestor_json['senha'] = criptografar(gestor_json['senha'])

    return GestorController.registrar(gestor_json), 201


@app.post('/gestor/<int:id_gestor>')
def modificar_gestor(id_gestor):
    pass



@app.get('/setor')
def listar_setores():
    return SetorController.listar(), 200

@app.post('/setor')
def registrar_setor():
    setor_json = request.get_json()

    if(not setor_json.get('descricao')
       or not setor_json.get('nome')):
        #TODO: Mudar
        return {'error': 'setor invalido'}, 400



    dados_setor = {
        'nome' : setor_json.get('nome'),
        'descricao' : setor_json.get('descricao'),
    }

    return SetorController.criar(dados_setor), 201

@app.patch('/setor/<int:id_setor>')
def alterar_setor(id_setor):
    setor_json = request.get_json()

    dados_setor = {
        'nome' : setor_json.get('nome'),
        'descricao' : setor_json.get('descricao'),
        'status': setor_json.get('status')
    }

    return SetorController.editar(id_setor, dados_setor), 200

@app.get('/setor/<int:id_setor>/problemas')
def listar_problemas_do_setor(id_setor):
    return SetorController.listar_problemas(id_setor), 200
