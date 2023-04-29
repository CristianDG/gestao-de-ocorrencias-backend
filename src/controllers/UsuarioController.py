from tipos import Usuario
from enum import Enum
from model.DAO.UsuarioDAO import UsuarioDAO
from model.connection.ConexaoAuth import ConexaoAuth
from model.connection.ConexaoProd import ConexaoProd

usuarioDAO = UsuarioDAO(ConexaoAuth(), ConexaoProd())

def criar():
    assert False, "Not Implemented"
    pass


def procurar_por_id(id_usuario):

    cargo = usuarioDAO.get_user_auth(id_usuario)

    if not id_usuario_auth:
        return False

    dados_usuario = usuarioDAO.get_user_prod(usuarioDAO.get_usuario_auth_map_prod(id_usuario))

    usuario = Usuario(**dados_usuario, cargo=cargo, admin= (cargo == 'administrador'))

    return usuario

def procurar_por_login(email, senha):
    if email == 'sla' and senha == '123':
        return Usuario(email=email, senha=senha, id=1)
    assert False, "Not Implemented"
    pass

def listar():
    assert False, "Not Implemented"
    pass
