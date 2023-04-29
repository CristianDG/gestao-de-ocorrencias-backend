from tipos import Usuario
from enum import Enum
from model.DAO.UsuarioDAO import UsuarioDAO
from model.DAO.GestorDAO import GestorDAO
from model.connection.ConexaoAuth import conexaoAuth
from model.connection.ConexaoProd import conexaoProd


usuarioDAO = UsuarioDAO(conexaoAuth, conexaoProd)
gestorDAO = GestorDAO(conexaoProd, usuarioDAO)

def registrar(dados_gestor):
    # FIXME FIXME FIXME FIXME

    gestor = Usuario(
        email=dados_gestor['email'],
        # NOTE: dados_gestor['senha'] já está criptografado
        senha=dados_gestor['senha'],
        nome=dados_gestor['nome'],
        sobrenome=dados_gestor['sobrenome'],
        status=dados_gestor['status'],
        cargo="Gestor",
        admin=False,
        setor=dados_gestor['id_setor']

    )

    id = gestorDAO.create_gestor(gestor)

    # TODO: Controle de erros

    gestor.id = id

    gestor.senha = None
    return gestor.dict()


def listar():
    assert False, "Not Implemented"
    pass

def mudar_setor():
    assert False, "Not Implemented"
    pass

def encaminhar_ocorrencia():
    assert False, "Not Implemented"
    pass
