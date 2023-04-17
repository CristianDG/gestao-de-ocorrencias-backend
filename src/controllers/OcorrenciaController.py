from tipos import Ocorrencia
from dataclasses import asdict
from enum import Enum
from model.DAO.OcorrenciaDAO import OcorrenciaDAO
from model.connection.ConexaoProd import conexaoProd

ocorrenciaDAO = OcorrenciaDAO(conexaoProd)

class Erro(Enum):
    OCORRENCIA_INVALIDA = ('Ocorrencia não encontrada', 404)
    SETOR_INVALIDO = ('Setor não encontrado', 404)

def listar():
    return ocorrenciaDAO.getOcorrencias()

def encaminhar(id_ocorrencia: int, id_setor: int):
    ocorrencia = ocorrenciaDAO.getOcorrenciaById(id_ocorrencia)
    if not ocorrencia:
        raise Exception(Erro.OCORRENCIA_INVALIDA)

    # TODO: falta controlar
    # - se existe o setor
    ocorrencia.id_setor = id_setor
    ocorrenciaDAO.setOcorrencia(ocorrencia)
    return ocorrencia.dict()


def registrar(dados_ocorrencia: dict) -> Ocorrencia:
    # TODO: falta controlar
    # - [ ] se existe o local
    # - [ ] se existe o setor

    ocorrencia = Ocorrencia(**dados_ocorrencia, status='Aberto', id=None)
    return ocorrenciaDAO.createOcorrencia(ocorrencia)
