'''
Criado por Victor C. 14/04
Classe referente á conexão com o banco de dados postgres utilizado para autênticação da aplicação


'''

import psycopg2



class ConexaoAuth:

    def __init__(self, app=None):
        self.localapp = app
        self.conexao = None
        self.init_app(self.localapp)

    def init_app(self, app):
        self.conexao = psycopg2.connect(
            host=app.config["AUTH_DB_HOST"],
            port=app.config["AUTH_DB_PORT"],
            database=app.config["AUTH_DB_NAME"],
            user=app.config["AUTH_DB_USER"],
            password=app.config["AUTH_DB_PASSWORD"],
            client_encoding=app.config["CLIENT_ENCODING"]
        )

    def conectar(self):
        if self.conexao is None:
            raise ValueError("A conexão não foi iniciada com uma instância do app")
        self.conexao.__enter__() #usado para melhorar a performance do With de executa_query. Encerrando a sessão após termino da operação
        return self.conexao


    def fecha_conexao(self):
        self.conexao.close()



    def executa_query(self, query, params):
        with self.localapp.app_context():
            conexao = self.conectar()
            with conexao.cursor() as cursor:
                cursor.execute(query, params)
                return cursor





