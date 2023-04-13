from tipos import Ocorrencia
from dataclasses import asdict

OCORRENCIAS: dict[int, Ocorrencia] = dict()
ID_OCORRENCIA = 0

def listar():
    # FIXME: usar assim até integrar com o banco
    return [{'id': id, **ocorrencia.dict()} for id, ocorrencia in OCORRENCIAS.items()]

def encaminhar(id_ocorrencia: int, id_setor: int):
    # FIXME: usar assim até integrar com o banco

    # TODO: falta controlar
    # - [ ] se existe a ocorrencia
    # - [ ] se existe o setor

    ocorrencia = OCORRENCIAS[id_ocorrencia]
    print(ocorrencia)
    ocorrencia.id_setor = id_setor
    return ocorrencia.dict()


def registrar(dados_ocorrencia: dict) -> Ocorrencia:
    # FIXME: usar assim até integrar com o banco
    global OCORRENCIAS, ID_OCORRENCIA

    # TODO: falta controlar
    # - [ ] se existe o local
    # - [ ] se existe o setor

    ocorrencia = Ocorrencia(**dados_ocorrencia, status='Aberto', data_resolucao=None)
    OCORRENCIAS[ID_OCORRENCIA] = ocorrencia
    ID_OCORRENCIA += 1


    return { **ocorrencia.dict(), 'id': ID_OCORRENCIA }
