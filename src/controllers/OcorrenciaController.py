from tipos import Ocorrencia
from erros import ErroController as Erro
from model.DAO.OcorrenciaDAO import OcorrenciaDAO
from model.DAO.SetorDAO import SetorDAO
from model.connection.ConexaoProd import ConexaoProd

ocorrenciaDAO = OcorrenciaDAO(ConexaoProd())
setorDAO = SetorDAO(ConexaoProd())


def listar():
    return ocorrenciaDAO.get_ocorrencias()

def encaminhar(id_ocorrencia: int, id_setor: int):
    ocorrencia = ocorrenciaDAO.get_ocorrencia_by_id(id_ocorrencia)
    if not ocorrencia:
        raise Exception(Erro.OCORRENCIA_INVALIDA)

    # TODO: falta controlar
    # - se existe o setor
    ocorrencia.id_setor = id_setor
    ocorrenciaDAO.update_ocorrencia(ocorrencia)
    return ocorrencia.dict()


def registrar(dados_ocorrencia: Ocorrencia) -> Ocorrencia:
    # TODO: falta controlar
    # - [ ] se existe o local
    # - [ ] se existe o setor


    id_setor = setorDAO.get_id_setor(dados_ocorrencia['id_problema'])

    if not id_setor:
        raise Exception(Erro.OCORRENCIA_NAO_CRIADA)

    ocorrencia = Ocorrencia(**dados_ocorrencia, status='Aberto', id=None, id_setor=id_setor)

    id = ocorrenciaDAO.create_ocorrencia(ocorrencia)
    if not id:
        raise Exception(Erro.OCORRENCIA_NAO_CRIADA)

    ocorrencia.id = id
    return ocorrencia.dict()
