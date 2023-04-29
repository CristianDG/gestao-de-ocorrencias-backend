from tipos import Ocorrencia, StatusOcorrencia as Status
from erros import ErroController as Erro
from model.DAO.OcorrenciaDAO import OcorrenciaDAO
from model.DAO.SetorDAO import SetorDAO
from model.connection.ConexaoProd import conexaoProd

ocorrenciaDAO = OcorrenciaDAO(conexaoProd)
setorDAO = SetorDAO(conexaoProd)


def listar():
    return ocorrenciaDAO.get_ocorrencias()

def encaminhar(id_ocorrencia: int, id_setor: int):
    ocorrencia = ocorrenciaDAO.get_ocorrencia_by_id(id_ocorrencia)
    if not ocorrencia:
        raise Exception(Erro.OCORRENCIA_INVALIDA)

    setor = setorDAO.get_setor_por_id(id_setor)
    if not setor:
        raise Exception(Erro.SETOR_INVALIDO)

    ocorrencia.id_setor = id_setor
    ocorrenciaDAO.update_ocorrencia(ocorrencia)

    return ocorrencia.dict()


def registrar(dados_ocorrencia: Ocorrencia) -> Ocorrencia:

    id_setor = setorDAO.get_id_setor(dados_ocorrencia['id_problema'])

    if not id_setor:
        raise Exception(Erro.OCORRENCIA_NAO_CRIADA)

    ocorrencia = Ocorrencia(**dados_ocorrencia, status=Status.PENDENTE, id=None, id_setor=id_setor)

    id = ocorrenciaDAO.create_ocorrencia(ocorrencia)
    if not id:
        raise Exception(Erro.OCORRENCIA_NAO_CRIADA)

    ocorrencia.id = id
    return ocorrencia.dict()

def listar_locais():
    return ocorrenciaDAO.get_locais()

def invalidar(id_ocorrencia):

    ocorrencia = ocorrenciaDAO.get_ocorrencia_by_id(id_ocorrencia)
    if not ocorrencia:
        raise Exception(Erro.OCORRENCIA_INVALIDA)

    ocorrencia.status = Status.INVALIDA

    res = ocorrenciaDAO.updateOcorrencia(ocorrencia)
    if not res:
        raise Exception(Erro.COMUM)

    return True


def solucionar(id_ocorrencia):
    pass
