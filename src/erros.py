from enum import Enum

class ErroController(Enum):
    OCORRENCIA_INVALIDA = ('Ocorrencia não encontrada', 404)
    OCORRENCIA_NAO_CRIADA = ('A ocorrência não foi criada, tente novamente', 500)

    SETOR_INVALIDO = ('Setor não encontrado', 404)
    SETOR_NAO_CRIADO = ('O setor não foi criado, tente novamente', 500)

