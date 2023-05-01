from tipos import Setor, Problema
from erros import ErroController as Erro
from model.DAO.SetorDAO import SetorDAO
from model.connection.ConexaoProd import conexaoProd

setorDAO = SetorDAO(conexaoProd)


def criar(dados_setor, problemas):

    # TODO: controlar

    setor = Setor(**dados_setor, status = 'Ativo')

    id_setor = setorDAO.create_setor(setor)

    if not id_setor:
        raise Exception(Erro.SETOR_NAO_CRIADO)

    setor.id = id_setor


    problemas_salvos = []
    for i in range(4):
        problema = ''
        if i < len(problemas):
            problema = problemas[i]
        if type(problema) == str:
            id_problema = setorDAO.create_problema(Problema(problema, id_setor))
            problemas_salvos.append(Problema(problema, id_setor, id= id_problema))

    setor.problemas = problemas_salvos

    return setor.dict()

def editar(id_setor, dados_setor, dados_problemas=[]):

    setor = setorDAO.get_setor_por_id(id_setor)
    if not setor:
        raise Exception(Erro.SETOR_INVALIDO)

    id_setor = setorDAO.update_setor(Setor(
        id=id_setor,
        nome=dados_setor.get('nome') or setor.nome,
        desc_responsabilidades=dados_setor.get('desc_responsabilidades') or setor.desc_responsabilidades,
        status=dados_setor.get('status') or setor.status))

    if not id_setor:
        # TODO: Encontrar um erro melhor
        raise Exception(Erro.COMUM)

    setor_retorno = setorDAO.get_setor_por_id(id_setor)

    while dados_problemas:
        problema = Problema(**dados_problemas.pop(), id_setor=id_setor)
        setorDAO.update_problema(problema)

    setor_retorno.problemas = setorDAO.get_id_problemas(id_setor)


    return setor_retorno.dict()

def inativar(id_setor):
    setor = setorDAO.get_setor_por_id(id_setor)
    if not setor:
        raise Exception(Erro.SETOR_INVALIDO)

    setor.status = "Inativo"
    setorDAO.update_setor(setor)
    return True


def listar():
    setores = []
    for setor in setorDAO.get_setores():
        setor.problemas = setorDAO.get_id_problemas(setor.id)
        setores.append(setor)

    return setores

def listar_problemas_do_setor(id_setor):
    setor = setorDAO.get_setor_por_id(id_setor)
    if not setor:
        raise Erro.SETOR_INVALIDO
    pass

def listar_problemas():
    problemas = setorDAO.get_problemas()

    if not problemas:
        return Erro.COMUM

    return problemas
