"""
Feito por Victor C.
Data: 08/04/23

Esta classe representa a classe DAO referente a classe ocorrência

Modificado dia 11/04 por Victor C. Alterações feitas:

correção de bugs na criação das classes e alteração nos métodos para uma melhor interpretação

Modificado 14/04 por Victor C. Alterações:
Alteração da nomenclatura das funções para o padrão get, set, delete, etc.
"""

from tipos import Ocorrencia, StatusOcorrencia as Status


class OcorrenciaDAO:

    def __init__(self, conexao):
        self.conexaoBD = conexao


    @staticmethod
    def formar_ocorrencia(ocorrencia):
        ocorrencia['status'] = Status(ocorrencia['status'])
        return Ocorrencia(**ocorrencia)

    def create_ocorrencia(self, ocorrencia):
        query_sql = "INSERT INTO ocorrencia (email_cidadao, descricao, status, " \
                    "id_local, id_setor, id_problema) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;"

        cursor = self.conexaoBD.executa_query(query_sql, (
            ocorrencia.email_cidadao, ocorrencia.descricao,
            ocorrencia.status.value, ocorrencia.id_local, ocorrencia.id_setor, ocorrencia.id_problema))

        id = cursor.fetchone()['id']
        cursor.close()
        return id


    #atualiza uma ocorrência
    def update_ocorrencia(self, ocorrencia):
        query_sql = "UPDATE ocorrencia SET id_problema = %s, email_cidadao = %s, descricao = %s, status = %s," \
                    " data_resolucao = %s, id_local = %s, id_setor = %s WHERE id = %s RETURNING id;"

        cursor = self.conexaoBD.executa_query(query_sql, (
            ocorrencia.id_problema, ocorrencia.email_cidadao, ocorrencia.descricao, ocorrencia.status.value,
            ocorrencia.data_resolucao, ocorrencia.id_local, ocorrencia.id_setor, ocorrencia.id, )
        )

        id_ocorrencia = cursor.fetchone()['id']

        cursor.close()
        return id_ocorrencia

    def get_ocorrencias_para_solucionar_por_setor(self, id_setor):
        query_sql = "SELECT oc.email_cidadao, oc.descricao, oc.status, oc.data_criacao, oc.data_resolucao," \
                    "oc.id_local, oc.id_problema, oc.id_setor, lo.nome as local, oc.id " \
                    "FROM ocorrencia AS oc LEFT JOIN local as lo ON oc.id_local = lo.id " \
                    "WHERE oc.id_setor = %s and (oc.status = %s or oc.status = %s)"

        cursor = self.conexaoBD.executa_query(query_sql, (id_setor, Status.PENDENTE.value, Status.VALIDA.value))
        resultados_query = cursor.fetchall()
        ocorrencias = []#lista contendo objetos de ocorrencias provindos da busca

        for ocorrencia in resultados_query:
            ocorrencias.append(self.formar_ocorrencia(ocorrencia))
        cursor.close()
        return ocorrencias

    def get_ocorrencias_para_solucionar(self):
        query_sql = "SELECT oc.email_cidadao, oc.descricao, oc.status, oc.data_criacao, oc.data_resolucao," \
                    "oc.id_local, oc.id_problema, oc.id_setor, lo.nome as local, oc.id " \
                    "FROM ocorrencia AS oc LEFT JOIN local as lo ON oc.id_local = lo.id " \
                    "WHERE oc.status = %s or oc.status = %s"

        cursor = self.conexaoBD.executa_query(query_sql, (Status.PENDENTE.value, Status.VALIDA.value))
        resultados_query = cursor.fetchall()
        ocorrencias = []#lista contendo objetos de ocorrencias provindos da busca

        for ocorrencia in resultados_query:
            ocorrencias.append(self.formar_ocorrencia(ocorrencia))
        cursor.close()
        return ocorrencias

    #retorna todas as ocorrências
    def get_ocorrencias(self):
        query_sql = "SELECT oc.email_cidadao, oc.descricao, oc.status, oc.data_criacao, oc.data_resolucao," \
                    "oc.id_local, oc.id_problema, oc.id_setor, lo.nome as local, oc.id " \
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

        query_sql = "SELECT oc.email_cidadao, oc.descricao, oc.status, oc.data_criacao, oc.data_resolucao," \
                    "oc.id_local, oc.id_problema, oc.id_setor, lo.nome as local, oc.id " \
                    "FROM ocorrencia AS oc LEFT JOIN local as lo ON oc.id_local = lo.id" \
                    "WHERE id_setor = %s"

        cursor = self.conexaoBD.executa_query(query_sql, id_setor)
        resultados = cursor.fetchall()
        cursor.close()
        if not resultados:
            return False
        ocorrencias = []  # lista contendo objetos de ocorrencias provindos da busca
        for ocorrencia in resultados:
            ocorrencias.append(self.formar_ocorrencia(ocorrencia))


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
