from typing import Any, Optional
from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class UrlType:
    solo: int = 1
    play_list: int = 2


@dataclass
class ResolutionType:
    low: str = '480'
    medium: str = '720'
    high: str = '1080'



class ApiResponseResource(BaseModel):
    status: bool
    message: Optional[str] = None
    data: Any


