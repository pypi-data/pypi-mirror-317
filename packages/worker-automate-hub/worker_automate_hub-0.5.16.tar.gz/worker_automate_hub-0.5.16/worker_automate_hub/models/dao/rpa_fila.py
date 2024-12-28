from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class RpaFila(BaseModel):
    uuidFila: Optional[str] = Field(None, alias="uuidFila")
    uuidRobo: Optional[str] = Field(None, alias="uuidRobo")
    uuidProcesso: str = Field(..., alias="uuidProcesso")
    prioridade: int = Field(..., alias="prioridade")
    configEntrada: Optional[dict] = Field(None, alias="configEntrada")
    dtLeituraFila: Optional[datetime] = Field(None, alias="dtLeituraFila")
    lock: Optional[bool] = Field(None, alias="lock")
    mutarNotificacao: Optional[int] = Field(None, alias="mutarNotificacao")

    class Config:
        populate_by_name = True
