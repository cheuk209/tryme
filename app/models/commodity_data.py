from pydantic import BaseModel, Field, validator
from enum import Enum
from datetime import datetime
from typing import List, Optional, Union

class Interval(str, Enum):
    monthly = "monthly"
    weekly = "weekly"
    daily = "daily"

class CommodityData(BaseModel):
    date: str
    value: str = Field(..., description='Must be a float or the string "."')

    @validator('value') # covering the edge case of empty value "." in old data
    def check_value(cls, v):
        if v == ".":
            return v
        try:
            float(v)
            return v
        except ValueError:
            raise ValueError('value must be a float or the string "."')

class Commodity(BaseModel):
    name: str
    interval: Interval
    unit: str
    data: list[CommodityData]
