# app/routes/sec/utils.py
from fastapi import APIRouter, HTTPException
from app.services.sec_api import SECService

router = APIRouter(prefix="/utils")

@router.get("/form-types", summary="Get Available Form Types")
async def get_form_types():
    """
    Get a list of common SEC form types and their descriptions.

    Returns:
    - Dictionary of form types and descriptions
    """
    form_types = {
        "10-K": "Annual report",
        "10-Q": "Quarterly report",
        "8-K": "Current report (material events or corporate changes)",
        "S-1": "Registration statement for securities",
        "424B": "Prospectus filed pursuant to Rule 424(b)",
        "DEF 14A": "Definitive proxy statement",
        "13F": "Quarterly report filed by institutional managers",
        "4": "Statement of changes in beneficial ownership",
        "SC 13G": "Schedule 13G - Passive investors",
        "SC 13D": "Schedule 13D - Active investors"
    }

    return {"form_types": form_types}

@router.get("/cik/{ticker}", summary="Get CIK by Ticker")
async def get_cik_by_ticker(ticker: str):
    """
    Get the CIK (Central Index Key) for a company by its ticker symbol.

    Parameters:
    - ticker: The company's ticker symbol

    Returns:
    - CIK number with leading zeros
    """
    sec_service = SECService()

    try:
        cik = sec_service.get_cik_by_ticker(ticker)
        return {"ticker": ticker.upper(), "cik": cik}
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting CIK: {str(e)}")
