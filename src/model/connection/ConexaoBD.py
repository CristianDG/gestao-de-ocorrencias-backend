"""
Feitor por Victor C. 
Data: 08/04/2023

Classe mãe utilizada para as conexões dos bancos
"""
from abc import abstractmethod


class ConexaoBD:

    def __init__(self):
        self.conexao = None
    

    @abstractmethod
    def conectar(self):
        pass

    @abstractmethod
    def cesconectar(self):
        pass

    @abstractmethod
    def executar(self, query):
        pass