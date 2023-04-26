from dataclasses import dataclass, asdict
from typing import Optional, Union
import datetime

@dataclass
class Ocorrencia:
    descricao: str
    id_local: int
    id_setor: int
    status: Optional[str]
    email_cidadao: Optional[str]
    nome_cidadao: Optional[str]
    id: Optional[int]
    data_criacao: datetime.datetime = datetime.datetime.now()
    data_resolucao: Optional[datetime.datetime] = None

    dict = asdict


@dataclass
class Usuario:
    email: str
    id: Optional[int] = None
    admin: bool = False
    senha: Optional[str] = None
