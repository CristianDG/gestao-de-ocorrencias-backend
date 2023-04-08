"""
Feito por Victor C.
Data: 08/04/23

Esta classe representa a classe DAO referente a classe ocorrência
"""


class Ocorrencia:
    def __int__(self, email_cidadao, nome_cidadao, descricao, status, data_criacao, data_resolucao,
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

    def __int__(self, conexao):
        self.conexaoBD = conexao

    def criar_ocorrencia(self, ocorrencia):
        query_sql = "INSERT INTO solve.ocorrencia (email_cidadao, nome_cidadao, descricao, status, data_criacao, " \
                    "id_local, id_setor) VALUES (%s, %s, %s, %s, %s, %s, %s);"


        #linha de comando que gera o insert dentro do banco
        self.conexaoBD.executa_query(query_sql, (ocorrencia.email_cidadao, ocorrencia.nome_cidadao, ocorrencia.descricao, ocorrencia.status, ocorrencia.data_criacao, ocorrencia.data_resolucao, ocorrencia.id_local, ocorrencia.id_setor))

    def atualizar_ocorrencia(self, ocorrencia):
        query_sql = "UPDATE solve.ocorrencia SET email_cidadao = %s, nome_cidadao = %s, descricao = %s, status = %s, " \
                    "data_criacao = %s, data_resolucao = %s, id_local = %s, id_setor = %s WHERE id = %s;"

        self.conexaoBD.executa_query(query_sql, (
        ocorrencia.email_cidadao, ocorrencia.nome_cidadao, ocorrencia.descricao, ocorrencia.status,
        ocorrencia.data_criacao, ocorrencia.data_resolucao, ocorrencia.id_local, ocorrencia.id_setor, ocorrencia.id))

    def buscar_todas_ocorrencias(self):
        query_sql = "SELECT * FROM solve.ocorrencia;"
        resultados = self.conexaoBD.executa_query(query_sql, None)
        ocorrencias = []
        for resultado in resultados:
            ocorrencias.append(
                Ocorrencia(resultado[0], resultado[1], resultado[2], resultado[3], resultado[4], resultado[5],
                           resultado[6], resultado[7]))
        return ocorrencias

    def buscar_ocorrencias_por_id_setor(self, id_setor):
        sql = "SELECT * FROM ocorrencia WHERE id_setor = %s"
        resultado = self.conexaoBD.executa_query(sql, (id_setor,))
        return Ocorrencia(resultado[0], resultado[1], resultado[2], resultado[3], resultado[4], resultado[5], resultado[6],
                          resultado[7])