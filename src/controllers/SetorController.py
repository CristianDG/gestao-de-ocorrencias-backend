from tipos import Setor
from erros import ErroController as Erro
from model.DAO.SetorDAO import SetorDAO
from model.connection.ConexaoProd import ConexaoProd

setorDAO = SetorDAO(ConexaoProd())


# FIXME: trocar para a classe Setor

def criar(dados_setor):

    # TODO: controlar

    setor = Setor(**dados_setor, status = 'Ativo')

    id_setor = setorDAO.create_setor(Setor(
        nome=setor.nome,
        descricao=setor.descricao,
        status=setor.status))

    if not id_setor:
        raise Exception(Erro.SETOR_NAO_CRIADO)

    setor.id = id_setor
    return setor.dict()

def editar(id_setor, dados_setor):

    setor = setorDAO.get_setor_por_id(id_setor)
    if not setor:
        raise Exception(Erro.SETOR_INVALIDO)

    # FIXME: Remover a linha abaixo
    id_setor = setorDAO.update_setor(Setor(
        id=id_setor,
        nome=dados_setor.get('nome') or setor.nome,
        descricao=dados_setor.get('descricao') or setor.descricao,
        status=dados_setor.get('status') or setor.status))

    if not id_setor:
        # FIXME: Encontrar um erro melhor
        assert False, "Not Implemented"

    # FIXME TROCAR PARA A CLASSE
    return setorDAO.get_setor_por_id(id_setor).dict()



def listar():
    setores = []
    for setor in setorDAO.get_setores():
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
