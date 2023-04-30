from dataclasses import dataclass, asdict, field
from typing import Optional, Union
from enum import Enum
import datetime

def asdict_factory(data):
    def convert_value(obj):
        if isinstance(obj, Enum):
            return obj.value
        return obj
    return dict((k, convert_value(v)) for k, v in data)

class StatusOcorrencia(Enum):
    PENDENTE = 'pendente'
    VALIDA = 'valida'
    INVALIDA = 'invalida'
    SOLUCIONADA = 'solucionada'

@dataclass
class Ocorrencia:
    descricao: str
    id_setor: int
    id_problema: int
    status: StatusOcorrencia
    email_cidadao: Optional[str]
    data_criacao: datetime.datetime = datetime.datetime.now()
    id_local: Optional[int] = None
    id: Optional[int] = None
    local: Optional[str] = None
    data_resolucao: Optional[datetime.datetime] = None

    def dict(self):
        return asdict(self, dict_factory=asdict_factory)


@dataclass
class Usuario:
    email: str
    nome: str
    sobrenome: str
    status: str
    cargo: Optional[str] = None
    id_auth: Optional[int] = None
    id: Optional[int] = None
    admin: bool = False
    senha: Optional[str] = None
    setor: Optional[int] = None
    matricula: Optional[str] = None

    dict = asdict

@dataclass
class Setor:
    nome: str
    desc_responsabilidades: str
    status: str
    id: Optional[int] = None
    problemas: list[str] = field(default_factory=list)

    dict = asdict


@dataclass
class Problema:
    nome: str
    id_setor: Optional[int] = None
    id: Optional[int] = None

    dict = asdict

