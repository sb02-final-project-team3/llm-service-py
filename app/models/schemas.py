from pydantic import BaseModel
from typing import List, Dict, Optional

class VisionAttributeOut(BaseModel):
    definitionName: str
    value: Optional[str] = None

class VisionOut(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None  # "TOP|BOTTOM|..."
    attributes: List[VisionAttributeOut] = []

class VisionRequest(BaseModel):
    imageUrl: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    definitionNames: List[str] = []
    optionsByDef: Dict[str, List[str]] = {}
    locale: str = "ko-KR"