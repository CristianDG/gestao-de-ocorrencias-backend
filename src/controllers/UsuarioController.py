from tipos import Usuario
from erros import ErroController as Erro
from model.DAO.UsuarioDAO import UsuarioDAO
from model.DAO.AuthDAO import AuthDAO
from model.connection.ConexaoAuth import conexaoAuth
from model.connection.ConexaoProd import conexaoProd

usuarioDAO = UsuarioDAO(conexaoAuth, conexaoProd)

def criar():
    assert False, "Not Implemented"
    pass


def procurar_por_id(id_usuario):

    usuario_auth = usuarioDAO.get_user_auth(id_usuario)

    if not usuario_auth:
        return False

    dados_usuario = usuarioDAO.get_user_prod(usuarioDAO.get_usuario_auth_map_prod(id_usuario))

    cargo = usuario_auth['cargo']
    usuario = Usuario(**dados_usuario, cargo=cargo, admin= (cargo == 'adm'))

    return usuario

def procurar_por_login(email, senha):

    id_usuario_auth = usuarioDAO.autentica_user(email, senha)

    if not id_usuario_auth:
        # NOTE: pode ser um erro melhor
        raise Exception(Erro.COMUM)

    cargo = usuarioDAO.get_user_auth(id_usuario_auth)['cargo']
    dados_usuario = usuarioDAO.get_user_prod(usuarioDAO.get_usuario_auth_map_prod(id_usuario_auth))

    if not dados_usuario:
        raise Exception(Erro.COMUM)

    usuario = Usuario(**dados_usuario, cargo=cargo, admin= (cargo == 'adm'))

    return usuario


def listar():
    assert False, "Not Implemented"
    pass


def mudar_senha(usuario,senha, nova_senha):
    usuario.id_auth = usuarioDAO.get_usuario_prod_map_auth(usuario.id)
    usuario.senha = nova_senha
    res = usuarioDAO.update_user_auth(usuario)
    if not res:
        raise Exception(Erro.COMUM)

    return True
