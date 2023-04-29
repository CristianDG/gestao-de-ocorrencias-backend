from dataclasses import dataclass, asdict
from typing import Optional, Union
from enum import Enum
import datetime


class StatusOcorrencia(Enum):
    PENDENTE = 'pendente'
    ATIVA = 'ativa'
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

    dict = asdict


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

    dict = asdict


