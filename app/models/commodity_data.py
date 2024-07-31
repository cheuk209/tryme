from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
from typing import List, Optional

class Interval(str, Enum):
    monthly = "monthly"
    weekly = "weekly"
    daily = "daily"

class CommodityData(BaseModel):
    date: str
    value: float

class Commodity(BaseModel):
    name: str
    interval: Interval
    unit: str
    data: list[CommodityData]
