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


class OcorrenciaDAO:

    def __init__(self, conexao):
        self.conexaoBD = conexao


    @staticmethod
    def formar_ocorrencia(ocorrencia):
        return Ocorrencia(**ocorrencia)

    def create_ocorrencia(self, ocorrencia):
        query_sql = "INSERT INTO ocorrencia (email_cidadao, descricao, status, " \
                    "id_local, id_setor, id_problema) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;"

        cursor = self.conexaoBD.executa_query(query_sql, (
            ocorrencia.email_cidadao, ocorrencia.descricao,
            ocorrencia.status, ocorrencia.id_local, ocorrencia.id_setor, ocorrencia.id_problema))

        id = cursor.fetchone()['id']
        cursor.close()
        return id


    #atualiza uma ocorrência
    def update_ocorrencia(self, ocorrencia):
        query_sql = "UPDATE ocorrencia SET id_problema = %s, email_cidadao = %s, descricao = %s, status = %s," \
                    " data_resolucao = %s, id_local = %s, id_setor = %s WHERE id = %s RETURNING id;"

        cursor = self.conexaoBD.executa_query(query_sql, (
            ocorrencia.id_problema, ocorrencia.email_cidadao, ocorrencia.descricao, ocorrencia.status,
            ocorrencia.data_resolucao, ocorrencia.id_local, ocorrencia.id_setor, ocorrencia.id, )
        )

        id_ocorrencia = cursor.fetchone()['id']

        cursor.close()
        return id_ocorrencia


    #retorna todas as ocorrências
    def get_ocorrencias(self):
        query_sql = "SELECT oc.email_cidadao, oc.descricao, oc.status, oc.data_criacao, oc.data_resolucao, oc.id_local, oc.id_setor, lo.nome as nome_local, oc.id " \
                    "FROM ocorrencia AS oc LEFT JOIN local as lo ON oc.id_local = lo.id"
        cursor = self.conexaoBD.executa_query(query_sql, None)
        resultados_query = cursor.fetchall()
        ocorrencias = []#lista contendo objetos de ocorrencias provindos da busca

        for ocorrencia in resultados_query:
            ocorrencias.append(self.formar_ocorrencia(ocorrencia))
        cursor.close()
        return ocorrencias

    def get_ocorrencia_by_id(self, id_ocorrencia):
        query_sql = "SELECT * FROM ocorrencia WHERE id = %s;"
        cursor = self.conexaoBD.executa_query(query_sql, (id_ocorrencia,))

        if cursor is None:
            return False

        ocorrencia = cursor.fetchone()

        if not ocorrencia:
            return False

        return self.formar_ocorrencia(ocorrencia)


    #retorna as ocorrências com base no id do setor
    def get_ocorrencias_por_id_setor(self, id_setor):
        query_sql = "SELECT email_cidadao, descricao, status, data_criacao, data_resolucao, id_local, id_setor, id_problema, id  " \
                    "FROM ocorrencia WHERE id_setor = %s"
        cursor = self.conexaoBD.executa_query(query_sql, id_setor)
        resultados = cursor.fetchall()
        ocorrencias = []  # lista contendo objetos de ocorrencias provindos da busca
        for ocorrencia in resultados:
            ocorrencias.append(self.formar_ocorrencia(ocorrencia))
        cursor.close()
        return ocorrencias

    def get_locais(self):
        cursor = self.conexaoBD.executa_query(
            'SELECT * FROM local',
            ()
        )
        if cursor is not None:
            resultado = cursor.fetchall()
            cursor.close()
            return resultado
        else:
            cursor.close()
            return None
