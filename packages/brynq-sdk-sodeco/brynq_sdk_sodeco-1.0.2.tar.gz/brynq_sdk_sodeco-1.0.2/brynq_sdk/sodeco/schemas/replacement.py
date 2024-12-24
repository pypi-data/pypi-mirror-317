from pandera import DataFrameModel, Field, Column
from typing import Optional
from datetime import datetime

class ReplacementSchema(DataFrameModel):
    # Required fields
    WorkerNumber: int = Field(nullable=False, ge=1, le=9999999)
    Startdate: str = Field(nullable=False, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')
    
    # Optional fields
    Enddate: Optional[str] = Field(nullable=True, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')
    Percentage: Optional[float] = Field(nullable=True, ge=0.0, le=100.0)
