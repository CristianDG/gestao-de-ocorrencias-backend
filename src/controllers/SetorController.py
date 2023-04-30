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
    for problema in problemas:
        if type(problema) == str:
            setorDAO.create_problema(Problema(problema, id_setor))
            problemas_salvos.append(problema)

    setor.problemas = problemas_salvos

    return setor.dict()

def editar(id_setor, dados_setor):

    setor = setorDAO.get_setor_por_id(id_setor)
    if not setor:
        raise Exception(Erro.SETOR_INVALIDO)

    id_setor = setorDAO.update_setor(Setor(
        id=id_setor,
        nome=dados_setor.get('nome') or setor.nome,
        descricao=dados_setor.get('descricao') or setor.descricao,
        status=dados_setor.get('status') or setor.status))

    if not id_setor:
        # FIXME: Encontrar um erro melhor
        raise Exception(Erro.COMUM)


    # FIXME: e os problemas?

    return setorDAO.get_setor_por_id(id_setor).dict()



def listar():
    setores = []
    for setor in setorDAO.get_setores():
        setor.problemas = [problema.nome for problema in setorDAO.get_id_problemas(setor.id)]
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
