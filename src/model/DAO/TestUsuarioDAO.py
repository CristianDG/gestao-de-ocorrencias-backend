import unittest
from .UsuarioDAO import UsuarioDAO
from ..connection.ConexaoProd import ConexaoProd
from ..connection.ConexaoAuth import ConexaoAuth
from ...tipos import Usuario

class TestUsuarioDAO(unittest.TestCase):

    def setUp(self):
        # Instancia a DAO e cria uma conexão temporária com o banco de dados para os testes
        self.dao = UsuarioDAO(ConexaoAuth(), ConexaoProd())
        self.primeiro_id_criado = None
        self.ultimo_id_criado = None

    def tearDown(self):
        #exclui as linhas dos bancos
        primeiro_id = self.primeiro_id_criado
        ultimo_id = self.ultimo_id_criado
        if primeiro_id is not None and ultimo_id is not None:
            for id in range(primeiro_id, ultimo_id):
                self.dao.delete_user(id)

        self.dao.fechar_conexao()

    def test_inserir_usuario(self):
        usuario = Usuario(email='teste12356@gmail.com', nome='pedrotestes', sobrenome='testes', status='ativo',
                          admin=False, senha='ajsdbhasjdbasd')

        id_usuario = self.dao.create_usuario(usuario)
        usuario.id_prod=id_usuario

        self.primeiro_id_criado = id_usuario
        self.ultimo_id_criado = id_usuario

        self.assertIsNotNone(id_usuario)

    def test_atualizar_usuario(self):

        usuario = Usuario(email='maria123456@gmail.com', nome='mariatestes', sobrenome='testes', status='ativo',
                          admin=False, senha='ajsdbhasjdbasd')

        id_prod = self.dao.create_usuario(usuario)
        self.ultimo_id_criado = id_prod

        novo_email = "mariaMudotestes123456@gmail.com"
        usuario.email = novo_email
        usuario.id_prod = id_prod
        self.dao.update_user(usuario)

        usuario_atualizado = self.dao.get_user(id_prod)

        self.assertEqual(usuario_atualizado.email, novo_email)


if __name__ == '__main__':
    unittest.main()
