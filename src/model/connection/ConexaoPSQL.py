"""
Feitor por Victor C. 
Data: 08/04/2023

Classe utilizada para realizar a conexão com o banco postgres da aplicação

dependêcnias utilizadas:
psycopg2.binary
os
flask current_app
"""

import psycopg2


class ConexaoPSQL:
    
    def __init__(self, app=None):
        self.localapp = app
        self.conexao = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.conexao = psycopg2.connect(
            host=app.config["PSQL_DB_HOST"],
            port=app.config["PSQL_DB_PORT"],
            database=app.config["PSQL_DB_NAME"],
            user=app.config["PSQL_DB_USER"],
            password=app.config["PSQL_DB_PASSWORD"]
        )

    def conectar(self):
        if self.conexao is None:
            raise ValueError("A conexão não foi iniciada com uma instância do app")
        self.conexao.__enter__()
        return self.conexao

    def fechar_conexao(self):
        if self.conexao is not None:
            self.conexao.__exit__(None, None, None)
            self.conexao = None

    def executa_query(self, query, params=None):
        with self.localapp.app_context():
            conexao = self.conectar()
            with conexao.cursor() as cursor:
                cursor.execute(query, params)
                resultado_consulta = cursor.fetchall
                conexao.commit()
                return resultado_consulta