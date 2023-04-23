import unittest
import datetime
from .OcorrenciaDAO import OcorrenciaDAO, Ocorrencia
from src.model.connection.ConexaoProd import ConexaoProd
from src.app import app


class TestOcorrenciaDAO(unittest.TestCase):

    def setUp(self):
        # Instancia a DAO e cria uma conexão temporária com o banco de dados para os testes
        self.instanciaBD = ConexaoProd(app)
        self.dao = OcorrenciaDAO(self.instanciaBD)
        self.dao.getOcorrencias()

    def tearDown(self):
        # Fecha a conexão e exclui o banco de dados temporário
        self.dao.conexaoBD.fechar_conexao()

    def test_inserir_ocorrencia(self):
        # Testa se um produto pode ser inserido corretamente na tabela
        nome = 'pedroTestes'
        email_cidadao = 'pedro@gmail.com'
        descricao = "testando"
        ocorrencia = Ocorrencia(' pedroTestes', 'pedro@gmail.com', 'testando só', 'Aberto', 1, 2)
        id_inserido = self.dao.createOcorrencia(ocorrencia)
        ocorrencia.id = id_inserido
        cursor = self.instanciaBD.executa_query(
            'SELECT nome_cidadao, email_cidadao, descricao, status, id_local, id_setor, id FROM ocorrencia WHERE id=%s;',
            (id_inserido,)
        )
        resultados = cursor.fetchone()
        ocorrencias = []
        ocorrencias.append(
            Ocorrencia(resultados[0], resultados[1], resultados[2], resultados[3], resultados[4], resultados[5],
                       ))
        cursor.close()
        self.assertEqual(ocorrencia, ocorrencias[0])

    def test_atualizar_ocorrencia(self):
        # Testa se um produto pode ser atualizado corretamente na tabela
        now = datetime.datetime.now()
        sql_datetime = now.strftime('%Y-%m-%d %H:%M:%S%z')

        ocorrencia = Ocorrencia('VictorTestes', 'victor@gmail.com', 'testando só', 'Invalida', 1, 2)
        id_criado = self.dao.createOcorrencia(Ocorrencia)
        ocorrencia.id = id_criado
        ocorrencia.nome_cidadao = "Alterei"
        self.dao.updateOcorrencia(ocorrencia)
        cursor = self.instanciaBD.executa_query(
            'SELECT nome_cidadao, email_cidadao, descricao, status, id_local, id_setor, id FROM ocorrencia WHERE id=%s;',
            (id_criado,)
        )
        resultados = cursor.fetchone()
        ocorrencias = []
        ocorrencias.append(
            Ocorrencia(resultados[0], resultados[1], resultados[2], resultados[3], resultados[4], resultados[5],
                       ))
        cursor.close()
        self.assertEqual(ocorrencia, ocorrencias[0])


    def test_listar_ocorrencias(self):
        # Testa se a lista de produtos retornada pela DAO está correta
        now = datetime.datetime.now()
        sql_datetime = now.strftime('%Y-%m-%d %H:%M:%S%z')
        ocorrencia1 = Ocorrencia('VictorTestes', 'victor@gmail.com', 'testando só', 'Invalida', 1, 2)
        ocorrencia2 = Ocorrencia('pedroTestes', 'pedro@gmail.com', 'testando só', 'Aberto', 1, 2)
        id1 = self.dao.createOcorrencia(ocorrencia1)
        id2 = self.dao.createOcorrencia(ocorrencia2)
        ocorrencia1.id = id1
        ocorrencia2.id = id2
        cursor = self.instanciaBD.executa_query(
            'SELECT nome_cidadao, email_cidadao, descricao, status, id_local, id_setor, id FROM ocorrencia WHERE id >= %s ORDER BY id;',
            (id1, id2)
        )
        resultados = cursor.fetchall()
        ocorrencias = []  # lista contendo objetos de ocorrencias provindos da busca
        for ocorrencia in resultados:
            ocorrencias.append(
                Ocorrencia(ocorrencia[0], ocorrencia[1], ocorrencia[2], ocorrencia[3], ocorrencia[4], ocorrencia[5],
                           ))
        cursor.close()

        self.assertListEqual([ocorrencia1, ocorrencia2], ocorrencias)


if __name__ == '__main__':
    unittest.main()
