from tipos import Ocorrencia, StatusOcorrencia as Status
from erros import ErroController as Erro
from model.DAO.OcorrenciaDAO import OcorrenciaDAO
from model.DAO.SetorDAO import SetorDAO
from model.DAO.DashboardDAO import DashboardDAO
from model.connection.ConexaoProd import conexaoProd

ocorrenciaDAO = OcorrenciaDAO(conexaoProd)
setorDAO = SetorDAO(conexaoProd)
dashboardDAO = DashboardDAO(conexaoProd)


def listar(id_setor=None) -> list[Ocorrencia]:
    ocorrencias = (ocorrenciaDAO.get_ocorrencias_para_solucionar_por_setor(id_setor)
                   if id_setor else ocorrenciaDAO.get_ocorrencias_para_solucionar())
    return [ocorrencia.dict() for ocorrencia in ocorrencias]

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
    if not ocorrencia or ocorrencia.status in [Status.SOLUCIONADA, Status.VALIDA]:
        raise Exception(Erro.OCORRENCIA_INVALIDA)

    ocorrencia.status = Status.INVALIDA

    res = ocorrenciaDAO.update_ocorrencia(ocorrencia)
    if not res:
        raise Exception(Erro.COMUM)

    return True


def resolver(id_ocorrencia):
    ocorrencia = ocorrenciaDAO.get_ocorrencia_by_id(id_ocorrencia)
    if not ocorrencia or ocorrencia.status in [Status.INVALIDA, Status.PENDENTE]:
        raise Exception(Erro.OCORRENCIA_INVALIDA)

    ocorrencia.status = Status.SOLUCIONADA

    res = ocorrenciaDAO.update_ocorrencia(ocorrencia)
    if not res:
        raise Exception(Erro.COMUM)

    return True

def validar(id_ocorrencia):
    ocorrencia = ocorrenciaDAO.get_ocorrencia_by_id(id_ocorrencia)
    if not ocorrencia or ocorrencia.status in [Status.INVALIDA, Status.SOLUCIONADA]:
        raise Exception(Erro.OCORRENCIA_INVALIDA)

    ocorrencia.status = Status.VALIDA

    res = ocorrenciaDAO.update_ocorrencia(ocorrencia)
    if not res:
        raise Exception(Erro.COMUM)

    return True

def dados_dashboard():
    resolvidas_invalidas = dashboardDAO.get_ocorrencias_validas_invalidas()
    ocorrencias_resolvidas = resolvidas_invalidas['num_ocorrencias_resolvidas']
    ocorrencias_invalidas = resolvidas_invalidas['num_ocorrencias_invalidadas']
    return {
        "criadas_hoje": dashboardDAO.get_ocorrencias_criadas_hoje(),
        "resolvidas": ocorrencias_resolvidas,
        "invalidas": ocorrencias_invalidas,
        "cadastradas_nos_ultimos_12_meses": dashboardDAO.get_ocorrencias_cadastradas_12meses()
    }
