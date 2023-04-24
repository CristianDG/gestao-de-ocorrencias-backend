import unittest
from .OcorrenciaDAO import OcorrenciaDAO
from ...tipos import Ocorrencia
from ..connection.ConexaoProd import ConexaoProd



class TestOcorrenciaDAO(unittest.TestCase):

    def setUp(self):
        # Instancia a DAO e cria uma conexão temporária com o banco de dados para os testes
        self.dao = OcorrenciaDAO(ConexaoProd())
        self.primeiro_id_criado = None
        self.ultimo_id_criado = None

    def tearDown(self):
        # Fecha a conexão e exclui o banco de dados temporário
        self.dao.conexaoBD.executa_query(
            'DELETE FROM ocorrencia WHERE id>=%s and id<=%s;',
            (self.primeiro_id_criado, self.ultimo_id_criado)
        )
        self.dao.conexaoBD.fechar_conexao()

    def test_inserir_ocorrencia(self):
        ocorrencia = Ocorrencia(email_cidadao="maria@gmail.com", nome_cidadao="Maria", descricao="teste",
                                status="aberto",
                                id_local=1, id_setor=1, id=None)

        id_ocorrencia = self.dao.create_ocorrencia(ocorrencia)
        self.primeiro_id_criado = id_ocorrencia
        self.ultimo_id_criado = id_ocorrencia

        self.assertIsNotNone(id_ocorrencia)

    def test_atualizar_ocorrencia(self):
        # Cria uma nova ocorrência
        ocorrencia = Ocorrencia(email_cidadao="joao@gmail.com", nome_cidadao="João", descricao="teste",
                                status="aberto",
                                id_local=1, id_setor=1, id=None)
        id_ocorrencia = self.dao.create_ocorrencia(ocorrencia)

        # Atualiza a descrição da ocorrência
        nova_descricao = "teste atualizado"
        ocorrencia.descricao = nova_descricao
        self.dao.update_ocorrencia(ocorrencia)
        self.ultimo_id_criado = id_ocorrencia
        # Obtém a ocorrência atualizada
        ocorrencia_atualizada = self.dao.getOcorrenciaById(id_ocorrencia)

        # Verifica se a descrição foi atualizada corretamente
        self.assertEqual(ocorrencia_atualizada.descricao, nova_descricao)


    '''def test_listar_ocorrencias(self):
        ocorrencia1 = Ocorrencia(email_cidadao="joao@gmail.com", nome_cidadao="João", descricao="teste",
                                 status="aberto",
                                 id_local=1, id_setor=1, id=None)
        id_ocorrencia1 = self.dao.createOcorrencia(ocorrencia1)
        ocorrencia1.id = id_ocorrencia1

        ocorrencia2 = Ocorrencia(email_cidadao="maria@gmail.com", nome_cidadao="Maria", descricao="teste",
                                 status="aberto",
                                 id_local=1, id_setor=1, id=None)
        id_ocorrencia2 = self.dao.createOcorrencia(ocorrencia2)
        ocorrencia2.id = id_ocorrencia2
        

        query = "SELECT id, email_cidadao, nome_cidadao, descricao, status, id_local, id_setor FROM ocorrencias ORDER BY id DESC LIMIT 2"
        with self.dao.conexaoBD.conectar() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

            ocorrencias = []
            for row in rows:
                ocorrencia = Ocorrencia(id=row[0], email_cidadao=row[1], nome_cidadao=row[2], descricao=row[3],
                                        status=row[4], id_local=row[5], id_setor=row[6])
                ocorrencia.id = row[0]
                ocorrencias.append(ocorrencia)

        self.assertEqual(len(ocorrencias), 2)
        self.assertEqual(ocorrencias[0].id, id_ocorrencia2)
        self.assertEqual(ocorrencias[1].id, id_ocorrencia1)'''


if __name__ == '__main__':
    unittest.main()
