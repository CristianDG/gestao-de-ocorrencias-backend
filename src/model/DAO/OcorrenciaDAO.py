"""
Feito por Victor C.
Data: 08/04/23

Esta classe representa a classe DAO referente a classe ocorrência

Modificado dia 11/04 por Victor C. Alterações feitas:

correção de bugs na criação das classes e alteração nos métodos para uma melhor interpretação

Modificado 14/04 por Victor C. Alterações:
Alteração da nomenclatura das funções para o padrão get, set, delete, etc.
"""

from tipos import Ocorrencia

#class Ocorrencia:
#    def __init__(self, nome_cidadao, email_cidadao, descricao, status, data_criacao, data_resolucao,
#                    id_local, id_setor):
#
#        self.email_cidadao = email_cidadao
#        self.nome_cidadao = nome_cidadao
#        self.descricao = descricao
#        self.status = status
#        self.data_criacao = data_criacao
#        self.data_resolucao = data_resolucao
#        self.id_local = id_local
#        self.id_setor = id_setor

class OcorrenciaDAO:

    def __init__(self, conexao):
        self.conexaoBD = conexao


    @staticmethod
    def formar_ocorrencia(ocorrencia):
        return Ocorrencia(
            id=ocorrencia[0],
            email_cidadao=ocorrencia[1],
            nome_cidadao=ocorrencia[2],
            descricao=ocorrencia[3],
            status=ocorrencia[4],
            data_criacao=ocorrencia[5],
            data_resolucao=ocorrencia[6],
            id_local=ocorrencia[7],
            id_setor=ocorrencia[8]
        )

    def create_ocorrencia(self, ocorrencia):
        query_sql = "INSERT INTO ocorrencia (email_cidadao, nome_cidadao, descricao, status, " \
                    "id_local, id_setor) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;"


        cursor = self.conexaoBD.executa_query(query_sql, (
            ocorrencia.email_cidadao, ocorrencia.nome_cidadao, ocorrencia.descricao,
            ocorrencia.status, ocorrencia.id_local, ocorrencia.id_setor))

        id = cursor.fetchone()[0]
        cursor.close()
        return id


    #atualiza uma ocorrência
    def update_ocorrencia(self, ocorrencia):
        query_sql = "UPDATE ocorrencia SET nome_cidadao = %s, email_cidadao = %s, descricao = %s, status = %s," \
                    " data_resolucao = %s, id_local = %s, id_setor = %s WHERE id = %s RETURNING id;"

        cursor = self.conexaoBD.executa_query(query_sql, (
            ocorrencia.email_cidadao, ocorrencia.nome_cidadao, ocorrencia.descricao, ocorrencia.status,
            ocorrencia.data_resolucao, ocorrencia.id_local, ocorrencia.id_setor,
            ocorrencia.id))

        id_ocorrencia = cursor.fetchone()[0]
        cursor.close()
        return id_ocorrencia

    #retorna todas as ocorrências
    def get_ocorrencias(self):
        query_sql = "SELECT nome_cidadao, email_cidadao, descricao, status, data_criacao, data_resolucao, id_local, id_setor, id " \
                    "FROM ocorrencia;"
        cursor = self.conexaoBD.executa_query(query_sql, None)
        resultados_query = cursor.fetchall()
        ocorrencias = []#lista contendo objetos de ocorrencias provindos da busca

        for ocorrencia in resultados_query:
            ocorrencias.append(self.formar_ocorrencia(ocorrencia))
        cursor.close()
        return ocorrencias

    def getOcorrenciaById(self, id_ocorrencia):
        query_sql = "SELECT * FROM ocorrencia WHERE id = %s;"
        cursor = self.conexaoBD.executa_query(query_sql, (id_ocorrencia,))

        if cursor is None:
            return False

        ocorrencia = cursor.fetchone()

        if not ocorrencia:
            return False

        return self.formar_ocorrencia(ocorrencia)


    #retorna as ocorrências com base no id do setor
    def get_ocorrencias_por_id_Setor(self, id_setor):
        query_sql = "SELECT nome_cidadao, email_cidadao, descricao, status, data_criacao, data_resolucao, id_local, id_setor, id  " \
                    "FROM ocorrencia WHERE id_setor = %s"
        cursor = self.conexaoBD.executa_query(query_sql, id_setor)
        resultados = cursor.fetchall()
        ocorrencias = []  # lista contendo objetos de ocorrencias provindos da busca
        for ocorrencia in resultados:
            ocorrencias.append(self.formar_ocorrencia(ocorrencia))
        cursor.close()
        return ocorrencias

    def get_ocorrencias_por_id(self, id):
        query_sql = "SELECT nome_cidadao, email_cidadao, descricao, status, data_criacao, data_resolucao, id_local, id_setor, id " \
                    "FROM ocorrencia WHERE id = %s"
        cursor = self.conexaoBD.executa_query(query_sql, id)
        resultados = cursor.fetchone()
        ocorrencias = []  # lista contendo objetos de ocorrencias provindos da busca
        for ocorrencia in resultados:
            ocorrencias.append(
                Ocorrencia(ocorrencia[0], ocorrencia[1], ocorrencia[2], ocorrencia[3], ocorrencia[4], ocorrencia[5], ocorrencia[6], ocorrencia[7], ocorrencia[8]))
        cursor.close()
        return ocorrencias





