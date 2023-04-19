from dataclasses import dataclass, asdict
from typing import Union
import datetime

@dataclass
class Ocorrencia:
    descricao: str
    id_local: int
    id_setor: int
    status: Union[str, None]
    email_cidadao: Union[str, None]
    nome_cidadao: Union[str, None]
    id: Union[int, None]
    data_criacao: datetime.datetime = datetime.datetime.now()
    data_resolucao: Union[datetime.datetime, None] = None

    dict = asdict


@dataclass
class Usuario:
    email: str
    senha: str
    id: Union[int, None]
