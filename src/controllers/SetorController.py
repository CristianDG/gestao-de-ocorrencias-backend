from tipos import Setor
from erros import ErroController as Erro
from model.DAO.SetorDAO import SetorDAO
from model.connection.ConexaoProd import ConexaoProd

setorDAO = SetorDAO(ConexaoProd())

def formarSetor(setor):
    return Setor(id=setor[0], nome=setor[1], descricao=setor[2], status=setor[3])

# FIXME: trocar para a classe Setor

def criar(dados_setor):

    # TODO: controlar

    setor = Setor(**dados_setor, status = 'Ativo')

    id_setor = setorDAO.create_setor(
        nome=setor.nome,
        descricao=setor.descricao,
        status=setor.status)

    if not id_setor:
        raise Exception(Erro.SETOR_NAO_CRIADO)

    setor.id = id_setor
    return setor.dict()

def editar(id_setor, dados_setor):

    setor = formarSetor(setorDAO.get_setor_by_id(id_setor))
    if not setor:
        raise Exception(Erro.SETOR_INVALIDO)

    # FIXME: Remover a linha abaixo
    id_setor = setorDAO.update_setor(
        id=id_setor,
        nome=dados_setor.get('nome') or setor.nome,
        descricao=dados_setor.get('descricao') or setor.descricao,
        status=dados_setor.get('status') or setor.status)

    if not id_setor:
        # FIXME: Encontrar um erro melhor
        assert False, "Not Implemented"

    # FIXME TROCAR PARA A CLASSE
    return formarSetor(setorDAO.get_setor_by_id(id_setor)).dict()



def listar():
    setores = []
    for setor in setorDAO.get_setores():
        setores.append(formarSetor(setor))
    return setores
