from pydantic import BaseModel
from typing import List, Optional


class JourneyGroup(BaseModel):
    title: str
    sort_order: int


class KeyJourney(BaseModel):
    ClassName: str
    LastEdited: str
    Title: str
    URLSlug: str
    Enabled: int
    SortOrder: int
    CurrentTime: int
    FreeFlowTime: int
    RegionID: int
    FreeFlowState: str


class Feature(BaseModel):
    type: str
    geometry: Optional[dict]
    properties: KeyJourney


class FeatureCollection(BaseModel):
    type: str
    features: List[Feature]
