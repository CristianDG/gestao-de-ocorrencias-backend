from tipos import Usuario
from enum import Enum
from model.DAO.UsuarioDAO import UsuarioDAO
from model.connection.ConexaoAuth import conexaoAuth

usuarioDAO = UsuarioDAO(conexaoAuth)

def criar():
    assert False, "Not Implemented"
    pass


def procurarPorId(id_usuario):
    if id_usuario == 1:
        return True
    assert False, "Not Implemented"
    pass

def procurarPorLogin(email, senha):
    if email == 'sla' and senha == '123':
        return Usuario(email=email, senha=senha, id=1)
    assert False, "Not Implemented"
    pass

def listar():
    assert False, "Not Implemented"
    pass
