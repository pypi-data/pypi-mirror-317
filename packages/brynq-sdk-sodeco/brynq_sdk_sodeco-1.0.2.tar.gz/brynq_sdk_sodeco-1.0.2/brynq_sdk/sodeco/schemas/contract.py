from pandera import DataFrameModel, Field, Column
from typing import Optional
from datetime import datetime

class CareerBreakDefinition(DataFrameModel):
    Reason: str = Field(nullable=False, str_length={'min_value': 0, 'max_value': 50})
    StartDate: str = Field(nullable=False, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')
    EndDate: Optional[str] = Field(nullable=True, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')

class CertainWorkDefinition(DataFrameModel):
    StartDate: str = Field(nullable=False, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')
    EndDate: str = Field(nullable=False, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')

class StudentDefinition(DataFrameModel):
    StartDate: str = Field(nullable=False, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')
    EndDate: str = Field(nullable=False, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')

class ContractSchema(DataFrameModel):
    # Required fields
    Startdate: str = Field(nullable=False, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')
    EmploymentStatus: str = Field(nullable=False, isin=['Employee', 'Interim', 'Student'])
    WorkingTime: str = Field(nullable=False, isin=['Fulltime', 'Parttime'])
    WeekhoursWorker: float = Field(nullable=False, ge=0.0, le=168.0)
    WeekhoursEmployer: float = Field(nullable=False, ge=0.0, le=168.0)
    
    # Optional fields
    Enddate: Optional[str] = Field(nullable=True, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')
    ContractType: Optional[str] = Field(nullable=True, isin=['Determined', 'Undetermined', 'Replacement', 'Student'])
    Function: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 50})
    ScheduleCode: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 20})
    ShiftCode: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 20})
    WorkplaceCode: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 20})
    DepartmentCode: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 20})
    JobClassificationCode: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 20})
    SalaryScaleCode: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 20})
    SalaryScaleStep: Optional[int] = Field(nullable=True, ge=0)
    Comments: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 255})
    CareerBreak: Optional[CareerBreakDefinition] = Field(nullable=True)
    CertainWork: Optional[CertainWorkDefinition] = Field(nullable=True)
    Student: Optional[StudentDefinition] = Field(nullable=True)
    CostCenters: Optional[str] = Field(nullable=True)  # Will be converted to/from list
    BenefitCodes: Optional[str] = Field(nullable=True)  # Will be converted to/from list
