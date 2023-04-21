"""
Feito por Victor C.
Data: 08/04/23

Esta classe representa a classe DAO referente a classe ocorrência

Modificado dia 11/04 por Victor C. Alterações feitas:

correção de bugs na criação das classes e alteração nos métodos para uma melhor interpretação

Modificado 14/04 por Victor C. Alterações:
Alteração da nomenclatura das funções para o padrão get, set, delete, etc.
"""


class Ocorrencia:
    def __init__(self, nome_cidadao, email_cidadao, descricao, status, data_criacao, data_resolucao,
                    id_local, id_setor):

        self.email_cidadao = email_cidadao
        self.nome_cidadao = nome_cidadao
        self.descricao = descricao
        self.status = status
        self.data_criacao = data_criacao
        self.data_resolucao = data_resolucao
        self.id_local = id_local
        self.id_setor = id_setor

class OcorrenciaDAO:

    def __init__(self, conexao):
        self.conexaoBD = conexao

    def createAcorrencia(self, ocorrencia):
        query_sql = "INSERT INTO ocorrencia (email_cidadao, nome_cidadao, descricao, status, data_criacao, " \
                    "id_local, id_setor) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;"


        #linha de comando que gera o insert dentro do banco
        return self.conexaoBD.executa_query(query_sql, (
        ocorrencia.email_cidadao, ocorrencia.nome_cidadao, ocorrencia.descricao, ocorrencia.status,
        ocorrencia.data_criacao, ocorrencia.id_local, ocorrencia.id_setor))

    #atualiza uma ocorrência
    def setOcorrencia(self, ocorrencia):
        query_sql = "UPDATE ocorrencia SET nome_cidadao = %s, email_cidadao = %s, descricao = %s, status = %s, " \
                    "data_criacao = %s, data_resolucao = %s, id_local = %s, id_setor = %s WHERE id = %s RETURNING id;"

        return self.conexaoBD.executa_query(query_sql, (
            ocorrencia.email_cidadao, ocorrencia.nome_cidadao, ocorrencia.descricao, ocorrencia.status,
            ocorrencia.data_criacao, ocorrencia.data_resolucao, ocorrencia.id_local, ocorrencia.id_setor,
            ocorrencia.id))

    #retorna todas as ocorrências
    def getOcorrencias(self):
        query_sql = "SELECT * FROM ocorrencia;"
        resultados_query = self.conexaoBD.executa_query(query_sql, None)
        ocorrencias = []#lista contendo objetos de ocorrencias provindos da busca
        for ocorrencia in resultados_query:
            ocorrencias.append(
                Ocorrencia(ocorrencia[0], ocorrencia[1], ocorrencia[2], ocorrencia[3], ocorrencia[4], ocorrencia[5],ocorrencia[6], ocorrencia[7]))

        return ocorrencias


    #retorna as ocorrências com base no id do setor
    def getocorrenciaByIdSetor(self, id_setor):
        query_sql = "SELECT * FROM ocorrencia WHERE id_setor = %s"
        resultados_query = self.conexaoBD.executa_query(query_sql, (id_setor,))
        self.conexaoBD.fechar_conexao()
        ocorrencias = []#lista contendo objetos de ocorrencias provindos da busca
        for ocorrencia in resultados_query:
            ocorrencias.append(
                Ocorrencia(ocorrencia[0], ocorrencia[1], ocorrencia[2], ocorrencia[3], ocorrencia[4], ocorrencia[5], ocorrencia[6], ocorrencia[7]))

        return ocorrencias