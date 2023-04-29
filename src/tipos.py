from dataclasses import dataclass, asdict
from typing import Optional, Union
import datetime


#NOTE: Fazer com que o banco retorne o local como str

@dataclass
class Ocorrencia:
    descricao: str
    id_setor: int
    id_problema: int
    status: Optional[str]
    email_cidadao: Optional[str]
    id_local: Optional[int] = None
    id: Optional[int] = None
    data_criacao: datetime.datetime = datetime.datetime.now()
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

@dataclass
class Setor:
    nome: str
    desc_responsabilidades: str
    status: str
    id: Optional[int] = None

    dict = asdict




