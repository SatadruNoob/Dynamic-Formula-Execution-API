from pydantic import BaseModel, Field, validator, root_validator, Extra, ValidationError
from typing import List, Optional, Any, Dict
import re
from app.utils import parse_value  # Import from utils.py

class FormulaInput(BaseModel):
    varName: str
    varType: str  # Options: "number", "percentage", "boolean", "datetime", "currency"

class Formula(BaseModel):
    outputVar: str
    expression: str
    inputs: List[FormulaInput]

class DataRow(BaseModel):
    id: int
    product: Optional[str] = None  # Product name (e.g., "Laptop")
    unitPrice: Optional[str] = None  # Price in currency format (e.g., "1200 USD")
    quantity: Optional[float] = None  # Quantity of items sold
    discount: Optional[str] = None  # Discount in percentage format (e.g., "10%")

    # Validator to check if 'unitPrice' is in the correct currency format
    @validator('unitPrice', always=True)
    def check_unit_price(cls, v):
        if v is None:
            return v
        currency_match = re.match(r'^(\$|€)?(\d+(,\d{3})*(\.\d+)?)\s*(USD|EUR)?$', v)
        if not currency_match:
            raise ValueError('unitPrice must be in the format "1200 USD" or similar')
        return v

    # Validator to check if 'discount' is in the correct percentage format
    @validator('discount', always=True)
    def check_discount(cls, v):
        if v is None:
            return v
        if not re.match(r'^\d+(\.\d+)?%$', v):
            raise ValueError('discount must be in the format "10%" or similar')
        return v

    # Allow arbitrary fields in the data model
    class Config:
        extra = Extra.allow

    # Custom root validator for dynamic field parsing
    @root_validator(pre=True)
    def parse_dynamic_fields(cls, values):
        """
        Custom root validator for handling extra dynamic fields not defined in the model.
        Uses `parse_value` function to convert fields dynamically based on their type.
        """
        for field, value in values.items():
            if field not in cls.__fields__:
                try:
                    # Try parsing dynamic fields using the custom parse_value function
                    values[field] = parse_value(value)
                except ValueError:
                    raise ValidationError(f"Could not parse dynamic field '{field}' with value '{value}'")
        return values 

class FormulaPayload(BaseModel):
    data: List[DataRow]
    formulas: List[Formula]