from tipos import Usuario
from erros import ErroController as Erro
from enum import Enum
from model.DAO.UsuarioDAO import UsuarioDAO
from model.DAO.GestorDAO import GestorDAO
from model.connection.ConexaoAuth import conexaoAuth
from model.connection.ConexaoProd import conexaoProd


usuarioDAO = UsuarioDAO(conexaoAuth, conexaoProd)
gestorDAO = GestorDAO(conexaoProd, usuarioDAO)

def registrar(dados_gestor):

    gestor = Usuario(
        email=dados_gestor['email'],
        # NOTE: dados_gestor['senha'] já está criptografado
        senha=dados_gestor['senha'],
        nome=dados_gestor['nome'],
        sobrenome=dados_gestor['sobrenome'],
        status="Ativo",
        cargo="Gestor",
        admin=False,
        setor=dados_gestor['id_setor']
    )

    id = gestorDAO.create_gestor(gestor)

    if not id:
        raise Exception(Erro.USUARIO_EXISTENTE)

    gestor.id = id
    gestor.senha = None

    return gestor.dict()


def listar():
    return gestorDAO.get_gestores()

def mudar_setor(id_gestor, id_setor):
    assert False, "Not Implemented"
    pass
