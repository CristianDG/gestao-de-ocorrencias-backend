"""
Feitor por Victor C. 
Data: 08/04/2023
Classe utilizada para realizar a conexão com o banco postgres da aplicação
Modificado dia 11/04

Modifiquei o método de executar query para uma forma mais coerente para as querys com ou sem resultados utilizáveis
assim como o método de fechar a conexão. Foi necessário utilizar o conexão.close() para de fato encerrar a conexão com o banco


Modificado dia 13/04 por Victor C.
Alterei o nome da classe, uma vez que passaremos a utilizar apenas postgres como BD, não existe sentido em ter o nome PSQL na classe
deste modo, chamei ConexaoProd para deixar explicíto que é o banco da produção (regras de negócio)



dependências utilizadas:
psycopg2.binary
"""

import os
import psycopg2


class ConexaoProd:

    #o paramêtro app referencia ao objeto APP que diz respeito á instância do Flask referente ao projeto
    #ela carrega dados da aplicação, incluindo variáveis salvas internamente
    def __init__(self):
        self.conexao = None
        if self.conexao is None:
            self.init_app()

    #atribui as váriaveis de conexão relacionada a base de dados e estabelece a comunicação com a base de dados
    def init_app(self):

        self.conexao = psycopg2.connect(
            host=os.getenv("PROD_DB_HOST"),
            port=os.getenv("PROD_DB_PORT"),
            database=os.getenv("PROD_DB_NAME"),
            user=os.getenv("PROD_DB_USER"),
            password=os.getenv("PROD_DB_PASSWORD"),
            client_encoding=os.getenv("CLIENT_ENCODING")
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
        conexao = self.conectar()
        with conexao.cursor() as cursor:
            cursor.execute(query, params)
            if any(query.strip().lower().startswith(x) for x in ("insert", "update", "delete")): #caso seja um insert,update,delete por padrão ele retorna um valor apenas da quantidade de linhas afetadas, mas não é utilizável para nós
                self.fechar_conexao()
                return None
            else:#senão retorna as linhas adiquiridas na consulta
                resultado_consulta = cursor.fetchall()
                return resultado_consulta

conexaoProd = ConexaoProd()
