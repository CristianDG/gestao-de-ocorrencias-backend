'''
Criado por Victor C. 14/04
Classe referente á conexão com o banco de dados postgres utilizado para autênticação da aplicação


'''

import psycopg2
import os


class ConexaoAuth:

    def __init__(self):
        self.conexao = None
        if self.conexao is None:
            self.init_app()

    def init_app(self):
        self.conexao = psycopg2.connect(
            host=os.getenv("AUTH_DB_HOST"),
            port=os.getenv("AUTH_DB_PORT"),
            database=os.getenv("AUTH_DB_NAME"),
            user=os.getenv("AUTH_DB_USER"),
            password=os.getenv("AUTH_DB_PASSWORD"),
            client_encoding=os.getenv("CLIENT_ENCODING")
        )
        self.conexao.autocommit = True

    def conectar(self):
        if self.conexao is None:
            raise ValueError("A conexão não foi iniciada com uma instância do app")
        return self.conexao


    def fecha_conexao(self):
        self.conexao.close()


    def executa_query(self, query, params=None):
        conexao = self.conectar()
        cursor = conexao.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor.execute(query, params)
        return cursor


conexaoAuth = ConexaoAuth()
