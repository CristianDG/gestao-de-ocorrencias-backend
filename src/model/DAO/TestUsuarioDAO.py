import unittest
from UsuarioDAO import UsuarioDAO
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
        self.dao.conexaoProd.executa_query(
            'DELETE FROM usuario WHERE id>=%s and id<=%s',
            (self.primeiro_id_criado, self.ultimo_id_criado, )
        )
        self.dao.conexaoAuth.executa_query(
            'DELETE FROM users WHERE id>=%s and id<=%s',
            (self.primeiro_id_criado, self.ultimo_id_criado, )
        )
        self.dao.conexaoProd.fechar_conexao()
        self.dao.conexaoAuth.fecha_conexao()

    def test_inserir_usuario(self):
        usuario = Usuario(email='pedrotestes@gmail.com', nome='pedrotestes', sobrenome='testes', status='ativo',
                          admin=False, senha='ajsdbhasjdbasd')

        id_usuario = self.dao.create_user(usuario)
        usuario.id_prod=id_usuario

        self.primeiro_id_criado = id_usuario

        self.assertIsNotNone(id_usuario)

    def test_atualizar_usuario(self):

        usuario = Usuario(email='mariatestes@gmail.com', nome='mariatestes', sobrenome='testes', status='ativo',
                          admin=False, senha='ajsdbhasjdbasd')

        id_prod = self.dao.create_user(usuario)

        novo_email = "mariaMudoutestes@gmail.com"
        usuario.email = novo_email
        self.dao.


