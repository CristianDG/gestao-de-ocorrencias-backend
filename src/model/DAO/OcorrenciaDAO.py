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
    def formarOcorrencia(ocorrencia):
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

    def createOcorrencia(self, ocorrencia):
        query_sql = "INSERT INTO solve.ocorrencia (email_cidadao, nome_cidadao, descricao, status, data_criacao, " \
                    "id_local, id_setor) VALUES (%s, %s, %s, %s, %s, %s, %s);"

        #linha de comando que gera o insert dentro do banco
        self.conexaoBD.executa_query(query_sql, (
            ocorrencia.email_cidadao, ocorrencia.nome_cidadao, ocorrencia.descricao, ocorrencia.status,
            ocorrencia.data_criacao, ocorrencia.id_local, ocorrencia.id_setor))

        return True



    #atualiza uma ocorrência
    def setOcorrencia(self, ocorrencia):
        query_sql = "UPDATE solve.ocorrencia SET nome_cidadao = %s, email_cidadao = %s, descricao = %s, status = %s, " \
                    "data_criacao = %s, data_resolucao = %s, id_local = %s, id_setor = %s WHERE id = %s;"

        self.conexaoBD.executa_query(query_sql, (
            ocorrencia.email_cidadao, ocorrencia.nome_cidadao, ocorrencia.descricao, ocorrencia.status,
            ocorrencia.data_criacao, ocorrencia.data_resolucao, ocorrencia.id_local, ocorrencia.id_setor,
            ocorrencia.id))

    #retorna todas as ocorrências
    def getOcorrencias(self):
        query_sql = "SELECT * FROM solve.ocorrencia;"
        resultados_query = self.conexaoBD.executa_query(query_sql, None)
        ocorrencias = []#lista contendo objetos de ocorrencias provindos da busca
        for ocorrencia in resultados_query:
            ocorrencias.append(self.formarOcorrencia(ocorrencia))

        return ocorrencias

    def getOcorrenciaById(self, id_ocorrencia):
        query_sql = "SELECT * FROM solve.ocorrencia WHERE id = %s;"
        resultados_query = self.conexaoBD.executa_query(query_sql, (id_ocorrencia,))
        if not resultados_query:
            return None

        ocorrencia = resultados_query[0]

        return self.formarOcorrencia(ocorrencia)


    #retorna as ocorrências com base no id do setor
    def getocorrenciaByIdSetor(self, id_setor):
        query_sql = "SELECT * FROM solve.ocorrencia WHERE id_setor = %s"
        resultados_query = self.conexaoBD.executa_query(query_sql, (id_setor,))
        self.conexaoBD.fechar_conexao()
        ocorrencias = []#lista contendo objetos de ocorrencias provindos da busca
        for ocorrencia in resultados_query:
            ocorrencias.append(self.formarOcorrencia(ocorrencia))

        return ocorrencias
