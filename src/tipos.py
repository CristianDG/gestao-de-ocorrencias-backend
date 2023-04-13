from dataclasses import dataclass, KW_ONLY, asdict
from typing import Union
import datetime

@dataclass
class Ocorrencia:
    status: Union[str, None]
    descricao: str
    email_cidadao: Union[str, None]
    nome_cidadao: Union[str, None]
    data_criacao: datetime.datetime = datetime.datetime.now()
    data_resolucao: Union[datetime.datetime, None] = None
    _: KW_ONLY
    id_local: int
    id_setor: int

    dict = asdict
