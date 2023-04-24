import unittest

from .SetorDAO import SetorDAO
from ...tipos import Setor
from ..connection.ConexaoProd import ConexaoProd
class TestSetorDAO(unittest.TestCase):

    def setUp(self):
        # Instancia a DAO e cria uma conexão temporária com o banco de dados para os testes
        self.dao = SetorDAO(ConexaoProd())
        self.primeiro_id_criado = None
        self.ultimo_id_criado = None

    def tearDown(self):
        # Fecha a conexão e exclui o banco de dados temporário
        self.dao.conexaoProd.executa_query(
            'DELETE FROM setor WHERE id>=%s and id<=%s;',
            (self.primeiro_id_criado, self.ultimo_id_criado)
        )
        self.dao.fechar_conexao()


    def test_inserir_setor(self):
        setor = Setor(nome='Setor de testes automatizados', descricao='lida com a criação de testes automatizados', status='Ativo')

        id_setor = self.dao.create_setor(setor)
        setor.id = id_setor
        self.primeiro_id_criado = id_setor

        self.assertIsNotNone(id_setor)


    def test_atualizar_setor(self):
        setor = Setor(nome='Setor de testes automatizados', descricao='lida com a criação de testes automatizados', status='Ativo')

        id_setor = self.dao.create_setor(setor)
        setor.id = id_setor

        nova_desc = 'Lida com criação e manutenção de teste automatizados, e teste de código'
        setor.descricao = nova_desc
        self.dao.update_setor(setor)
        self.ultimo_id_criado = id_setor

        setor_att = self.dao.get_setor_por_id(id_setor)

        self.assertEqual(setor_att.descricao, nova_desc)



if __name__ == '--main--':
    unittest.main()