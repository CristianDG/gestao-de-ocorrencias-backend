#!/usr/bin/env python3
from flask import Flask, request
from controllers import OcorrenciaController

app = Flask(__name__)

@app.route("/")
def hello_world():
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
