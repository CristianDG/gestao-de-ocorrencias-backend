"""
Feitor por Victor C. 
Data: 08/04/2023
Classe utilizada para realizar a conexão com o banco postgres da aplicação
Modificado dia 11/04

Modifiquei o método de executar query para uma forma mais coerente para as querys com ou sem resultados utilizáveis
assim como o método de fechar a conexão. Foi necessário utilizar o conexão.close() para de fato encerrar a conexão com o banco



dependências utilizadas:
psycopg2.binary
"""

import psycopg2


class ConexaoPSQL:

    #o paramêtro app referencia ao objeto APP que diz respeito á instância do Flask referente ao projeto
    #ela carrega dados da aplicação, incluindo variáveis salvas internamente
    def __init__(self, app=None):
        self.localapp = app
        self.conexao = None
        if app is not None:
            self.init_app(app)

    #atribui as váriaveis de conexão relacionada a base de dados e estabelece a comunicação com a base de dados
    def init_app(self, app):
        self.conexao = psycopg2.connect(
            host=app.config["PSQL_DB_HOST"],
            port=app.config["PSQL_DB_PORT"],
            database=app.config["PSQL_DB_NAME"],
            user=app.config["PSQL_DB_USER"],
            password=app.config["PSQL_DB_PASSWORD"],
            client_encoding=app.config["CLIENT_ENCODING"]
        )


    #método auxiliar para dar início ao uso da conexão com o banco de dados
    def conectar(self):
        if self.conexao is None:
            raise ValueError("A conexão não foi iniciada com uma instância do app")
        self.conexao.__enter__() #usado para melhorar a performance do With de executa_query. Encerrando a sessão após termino da operação
        return self.conexao

    def fechar_conexao(self):
        if self.conexao is not None:
            self.conexao.__exit__(None, None, None)
            self.conexao.close()
            self.conexao = None


    '''executa a query e da o seu retorno. Caso não haja retorno não interfere na função
     
     Por padrão o método .execute do pacote psycopg evita SQL injections.
     Contanto que os paraâmetros sejam passados fora da query, não existem riscos.
     '''
    #A função executa query
    def executa_query(self, query, params):
        resultado_consulta = None
        conexao = None
        num_linhas_retorno = 0
        with self.localapp.app_context():
            conexao = self.conectar()
            with conexao.cursor() as cursor:
                cursor.execute(query, params)
                if any(query.strip().lower().startswith(x) for x in ("insert", "update", "delete")): #caso seja um insert,update,delete por padrão ele retorna um valor apenas da quantidade de linhas afetadas, mas não é utilizável para nós
                    self.fechar_conexao()
                    return None
                else:#senão retorna as linhas adiquiridas na consulta
                    resultado_consulta = cursor.fetchall()
                    return resultado_consulta