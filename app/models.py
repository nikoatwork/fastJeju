# app/models.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Jeju Orange",
                "description": "Fresh orange from Jeju Island",
                "price": 5.99
            }
        }

class ItemResponse(BaseModel):
    items: List[Item]
    count: int

class CompanyInfo(BaseModel):
    cik: str
    ticker: str
    title: str

    class Config:
        schema_extra = {
            "example": {
                "cik": "0000320193",
                "ticker": "AAPL",
                "title": "Apple Inc."
            }
        }

class FilingMetadataRequest(BaseModel):
    ticker: str = Field(..., description="Company ticker symbol (e.g., AAPL, MSFT)")

class FilingMetadataResponse(BaseModel):
    cik: str
    company_name: str
    ticker: str
    metadata: Dict[str, Any]

    class Config:
        schema_extra = {
            "example": {
                "cik": "0000320193",
                "company_name": "Apple Inc.",
                "ticker": "AAPL",
                "metadata": {
                    "cik": "0000320193",
                    "name": "Apple Inc.",
                    "filings": {
                        "recent": {
                            "accessionNumber": ["0000320193-21-000001"],
                            "filingDate": ["2021-01-15"],
                            "form": ["10-K"]
                        }
                    }
                }
            }
        }
