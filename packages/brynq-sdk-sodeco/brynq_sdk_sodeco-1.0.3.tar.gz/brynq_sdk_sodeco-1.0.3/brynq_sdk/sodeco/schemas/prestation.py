from pandera import DataFrameModel, Field, Column
from typing import Optional, List
import pandas as pd

class CostSchema(DataFrameModel):
    """Schema for cost entries in prestations"""
    Code: int = Field(nullable=False, ge=1.0, le=8999.0)
    CostCentre: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 15})
    Shift: Optional[int] = Field(nullable=True, ge=1.0, le=99.0)
    Days: Optional[int] = Field(nullable=True, ge=0.0, le=99.0)
    Hours: Optional[float] = Field(nullable=True, ge=0.0, le=9999.0)
    Unity: Optional[float] = Field(nullable=True)
    Percentage: Optional[float] = Field(nullable=True)
    Amount: Optional[float] = Field(nullable=True)
    Supplement: Optional[float] = Field(nullable=True)

    class Config:
        strict = True
        coerce = True

class PrestationEntrySchema(DataFrameModel):
    """Schema for individual prestation entries"""
    Day: str = Field(nullable=False, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')
    Code: int = Field(nullable=False, ge=1.0, le=6999.0)
    CostCentre: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 15})
    Shift: Optional[int] = Field(nullable=True, ge=1.0, le=99.0)
    Hours: Optional[float] = Field(nullable=True, ge=0.0, le=9999.0)

    class Config:
        strict = True
        coerce = True

class PrestationSchema(DataFrameModel):
    """Schema for prestation entries"""
    # Required fields
    WorkerNumber: int = Field(nullable=False, ge=1.0, le=9999999.0)
    Month: int = Field(nullable=False, ge=1.0, le=12.0)
    Year: int = Field(nullable=False, ge=1900.0, le=2075.0)
    EndOfPeriod: str = Field(nullable=False, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')
    
    # Optional fields
    Annotation: Optional[str] = Field(nullable=True)
    Reset: Optional[str] = Field(nullable=True, isin=['N', 'Y'])
    Prestations: Optional[List[dict]] = Field(nullable=True)  # Will be validated separately using PrestationEntrySchema
    Costs: Optional[List[dict]] = Field(nullable=True)  # Will be validated separately using CostSchema

    class Config:
        strict = True
        coerce = True

    @classmethod
    def validate_prestations(cls, prestations: List[dict]) -> bool:
        """Validate a list of prestations against the PrestationEntrySchema"""
        if not prestations:
            return True
            
        try:
            df = pd.DataFrame(prestations)
            PrestationEntrySchema.validate(df)
            return True
        except Exception:
            return False

    @classmethod
    def validate_costs(cls, costs: List[dict]) -> bool:
        """Validate a list of costs against the CostSchema"""
        if not costs:
            return True
            
        try:
            df = pd.DataFrame(costs)
            CostSchema.validate(df)
            return True
        except Exception:
            return False

    @classmethod
    def validate_prestations(cls, data: dict) -> bool:
        """Validate prestation data including nested prestations and costs"""
        try:
            # Validate main prestation data
            df = pd.DataFrame([{k:v for k,v in data.items() if not isinstance(v, list)}])
            cls.validate(df)
            
            # Validate prestations if present
            prestations = data.get('Prestations', [])
            if prestations:
                df_prestations = pd.DataFrame(prestations)
                PrestationEntrySchema.validate(df_prestations)
                
            # Validate costs if present
            costs = data.get('Costs', [])
            if costs:
                df_costs = pd.DataFrame(costs)
                CostSchema.validate(df_costs)
                
            return True
        except Exception:
            return False

class PrestationCompletedSchema(DataFrameModel):
    """Schema for marking prestations as completed"""
    # Required fields
    Month: int = Field(nullable=False, ge=1.0, le=12.0)
    Year: int = Field(nullable=False, ge=1900.0, le=2075.0)
    
    # Optional fields
    Correction: Optional[str] = Field(nullable=True, isin=['N', 'Y'])

    class Config:
        strict = True
        coerce = True

    @classmethod
    def validate_completed(cls, data: dict) -> bool:
        """Validate completed prestation data"""
        try:
            df = pd.DataFrame([data])
            cls.validate(df)
            return True
        except Exception:
            return False

class DeletePrestationSchema(DataFrameModel):
    """Schema for deleting prestations"""
    WorkerNumber: int = Field(nullable=False, ge=1.0, le=9999999.0)
    Month: int = Field(nullable=False, ge=1.0, le=12.0)
    Year: int = Field(nullable=False, ge=1900.0, le=2075.0)

    class Config:
        strict = True
        coerce = True

    @classmethod
    def validate_delete(cls, data: dict) -> bool:
        """Validate delete prestation data"""
        try:
            df = pd.DataFrame([data])
            cls.validate(df)
            return True
        except Exception:
            return False
