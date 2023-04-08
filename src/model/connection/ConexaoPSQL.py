"""
Feitor por Victor C. 
Data: 08/04/2023

Classe utilizada para realizar a conexão com o banco postgres da aplicação

dependêcnias utilizadas:
psycopg2.binary
"""

import psycopg2
import ConexaoBD
from flask import current_app



class ConexaoPSQL(ConexaoBD):

    def conectar(self):
        if self.conexao is None:
            self.conexao = psycopg2.connect(
                host=current_app.config['PSQL_DB_HOST'],
                database=current_app.config['PSQL_DB_NAME'],
                user=current_app.config['PSQL_DB_USER'],
                password=current_app.config['PSQL_DB_PASSWORD']
            )
        return self.conexao

    def fechar_conexao(self):
        if self.conexao is not None:
            self.conexao.close()
            self.conexao = None

    def executa_query(self, query, params=None):
        with self.conexao.cursos() as cursor:
            cursor.execute(query, params)
            linhas = cursor.fetchall()
            return linhas