#!/usr/bin/env python3
import os
if os.getenv('DEBUG_CDG'):
    from psycopg2cffi import compat; compat.register()
from flask import Flask, jsonify, request, redirect, url_for, Blueprint
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
from functools import wraps
from hashlib import sha256
import jwt
from datetime import datetime as dt, timedelta
from tipos import Usuario, Ocorrencia, Setor
from erros import ErroController as Erro
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

    if hasattr(erro, 'args') and len(erro.args) > 0 and type(erro.args[0]) == Erro:
        return ({'error': erro.args[0].value[0]}, erro.args[0].value[1])

    if os.getenv('DEBUG'):
        raise erro

    return {'error': 'internal server error'}, 500


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

            token = decode(request.headers['Authorization'])
            id_usuario = None
            try:
                id_usuario = int(token['id'])
            except:
                return erro

            # TODO: controlar se o token é antigo
            ttl_token = timedelta(hours=3)

            data_token = dt.fromtimestamp(token['data'])
            agora = dt.now()

            if (agora - data_token) > ttl_token:
                return erro

            usuario = UsuarioController.procurar_por_id(id_usuario)
            if not usuario:
                return erro

            return fn(*args, **kwargs, usuario_solicitante=usuario)

        return inner
    return wrapper


@app.route("/")
@autenticar(gestor=True, admin=True)
def hello_world(usuario_solicitante):
    return 'admin' if usuario_solicitante.admin else 'gestor'

@app.get("/ocorrencias")
@autenticar(gestor=True)
def listar_ocorrencias(usuario_solicitante=None):
    # TODO: controlar qual é o setor
    return OcorrenciaController.listar(usuario_solicitante.setor)

@app.post("/ocorrencias")
def registrar_ocorrencia():
    ocorrencia_json = request.get_json()

    erro = verificar_existencia(['descricao', 'id_local', 'id_problema'], ocorrencia_json)
    if erro:
        return {'error': erro}, 403


    dados_ocorrencia = {
        'email_cidadao' : ocorrencia_json.get('email_cidadao'),
        'descricao' : ocorrencia_json['descricao'],
        'id_local' : ocorrencia_json['id_local'],
        'id_problema': ocorrencia_json['id_problema']
    }

    return OcorrenciaController.registrar(dados_ocorrencia), 201

@app.delete("/ocorrencias/<int:id_ocorrencia>")
@autenticar(gestor=True)
def invalidar_ocorrencia(id_ocorrencia, usuario_solicitante=None):

    res = OcorrenciaController.invalidar(id_ocorrencia)
    if not res:
        raise Exception(Erro.COMUM)

    return '', 204

@app.patch("/ocorrencias/<int:id_ocorrencia>")
@autenticar(gestor=True)
def validar_ocorrencia(id_ocorrencia, usuario_solicitante=None):

    res = OcorrenciaController.validar(id_ocorrencia)
    if not res:
        raise Exception(Erro.COMUM)

    return '', 204

@app.post("/ocorrencias/<int:id_ocorrencia>")
@autenticar(gestor=True)
def resolver_ocorrencia(id_ocorrencia, usuario_solicitante=None):

    res = OcorrenciaController.resolver(id_ocorrencia)
    if not res:
        raise Exception(Erro.COMUM)

    return '', 204

@app.patch("/ocorrencias/<int:id_ocorrencia>/<int:id_setor>")
@autenticar(gestor=True)
def encaminhar_ocorrencia(id_ocorrencia, id_setor, usuario_solicitante=None):

    # TODO: falta validar
    # - [ ] token jwt para gestor

    return OcorrenciaController.encaminhar(id_ocorrencia, id_setor)


@app.post('/login')
def login():
    usuario_json = request.get_json()

    erro = verificar_existencia(['email', 'senha'], usuario_json)
    if erro:
        return {'error': erro}, 403

    usuario = UsuarioController.procurar_por_login(usuario_json['email'], criptografar(usuario_json['senha']))
    if not usuario:
        return {'error': 'email ou senha incorretos'}, 400

    token = encode({'id': usuario.id, 'data': dt.now().timestamp()})

    return { 'token': token, 'adm': usuario.admin }, 200

@app.patch('/mudar-senha')
@autenticar(gestor=True, admin=True)
def mudar_senha(usuario_solicitante=None):
    senhas_json = request.get_json()
    erro = verificar_existencia(['senha', 'nova_senha'], senhas_json)
    if erro:
        return {'error': erro}, 403

    senha = criptografar(senhas_json['senha'])
    nova_senha = criptografar(senhas_json['nova_senha'])
    res = UsuarioController.mudar_senha(usuario_solicitante, senha, nova_senha)

    if not res:
        raise Exception(Erro.COMUM)

    return '', 200


@app.get('/gestor')
@autenticar(admin=True)
def listar_gestores(usuario_solicitante=None):
    return GestorController.listar()

@app.get('/gestor/<int:id_gestor>')
@autenticar(admin=True)
def informacoes_gestor(id_gestor, usuario_solicitante=None):
    return {'status': 'Work In Progress'}

@app.post('/gestor')
@autenticar(admin=True)
def registrar_gestor(usuario_solicitante=None):
    gestor_json = request.get_json()

    erro = verificar_existencia(
        ['email', 'senha', 'nome', 'sobrenome', 'id_setor'], gestor_json)

    if erro:
        return {'error': erro}, 403

    gestor_json['senha'] = criptografar(gestor_json['senha'])

    return GestorController.registrar(gestor_json), 201


@app.post('/gestor/<int:id_gestor>')
@autenticar(admin=True)
def modificar_gestor(id_gestor, usuario_solicitante=None):
    gestor_json = request.get_json()

    return {'status': 'Work In Progress'}


@app.get('/setor')
@autenticar(gestor=True)
def listar_setores():
    return SetorController.listar(), 200

@app.post('/setor')
@autenticar(admin=True)
def registrar_setor(usuario_solicitante=None):
    setor_json = request.get_json()

    erro = verificar_existencia(['nome', 'desc_responsabilidades', 'problemas'], setor_json)
    if erro:
        return {'error': erro}, 403

    if not type(setor_json['problemas']) == list:
        raise Exception(Erro.COMUM)

    dados_setor = {
        'nome' : setor_json.get('nome'),
        'desc_responsabilidades' : setor_json.get('desc_responsabilidades'),
    }

    return SetorController.criar(dados_setor, setor_json['problemas']), 201

@app.patch('/setor/<int:id_setor>')
@autenticar(admin=True)
def alterar_setor(id_setor, usuario_solicitante=None):
    setor_json = request.get_json()


    dados_setor = {
        'nome' : setor_json.get('nome'),
        'desc_responsabilidades' : setor_json.get('desc_responsabilidades'),
        'status': setor_json.get('status')
    }

    return SetorController.editar(id_setor, dados_setor, setor_json.get('problemas', [])), 200

@app.get('/setor/<int:id_setor>/problemas')
@autenticar(admin=True)
def listar_problemas_do_setor(id_setor, usuario_solicitante=None):
    return SetorController.listar_problemas_do_setor(id_setor), 200


@app.get('/problemas')
def listar_problemas():
    return SetorController.listar_problemas(), 200

@app.get('/locais')
def listar_locais():
    return OcorrenciaController.listar_locais(), 200

@app.patch('/inativar/<int:id_setor>')
@autenticar(admin=True)
def inativar_setor(id_setor, usuario_solicitante=None):
    res = SetorController.inativar(id_setor)
    if not res:
        raise Exception(Erro.COMUM)

    return '', 200

@app.get('/dashboard')
@autenticar(gestor=True, admin=True)
def dados_dashboard(usuario_solicitante=None):
    return OcorrenciaController.dados_dashboard(), 200


@app.patch('/mudar-setor/<int:id_gestor>/<int:id_setor>')
@autenticar(admin=True)
def mudar_setor(id_gestor, id_setor, usuario_solicitante=None):
    res =  GestorController.mudar_setor(id_gestor, id_setor), 200
    if not res:
        raise Exception(Erro.COMUM)
    return '', 200
