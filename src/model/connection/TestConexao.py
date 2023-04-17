import unittest
from .ConexaoProd import ConexaoProd
from flask import current_app


class TestPostgresConnection(unittest.TestCase):

    def setUp(self):
        app = current_app
        app.config["TESTING"] = True
        self.app = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        self.conexao = ConexaoProd(app)
        self.conexao.conectar()

    def tearDown(self):
        self.conexao.fechar_conexao()

    def test_query(self):
        query = "SELECT * FROM solve.ocorrencia LIMIT 1;"
        params = None
        rows = self.conexao.executa_query(query, params)
        self.assertEqual(len(rows), 1)


if __name__ == '__main__':
    unittest.main()
