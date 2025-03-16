# app/routes/sec/filing.py
from fastapi import APIRouter, HTTPException, Query
from app.services.sec_api import SECService
from app.models import FilingMetadataResponse
from typing import List, Optional

router = APIRouter(prefix="/filing")

@router.get("/metadata/{ticker}", response_model=FilingMetadataResponse, summary="Get Filing Metadata")
async def get_filing_metadata(ticker: str):
    """
    Get SEC filing metadata for a company by its ticker symbol.

    This endpoint retrieves the filing metadata from the SEC's API
    for the specified company.

    Parameters:
    - ticker: The company's ticker symbol (e.g., AAPL for Apple)

    Returns:
    - Filing metadata information
    """
    sec_service = SECService()

    try:
        # Get filing metadata
        metadata = sec_service.get_filing_metadata(ticker)

        # Get company data from the metadata
        company_name = metadata.get('name', '')
        cik = metadata.get('cik', '')

        # Format the response
        response = FilingMetadataResponse(
            cik=cik,
            company_name=company_name,
            ticker=ticker.upper(),
            metadata=metadata
        )

        return response
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@router.get("/recent/{ticker}", summary="Get Recent Filings")
async def get_recent_filings(
    ticker: str,
    form_type: Optional[str] = Query(None, description="Filter by form type (e.g., 10-K, 10-Q)")
):
    """
    Get recent filings for a company.

    Parameters:
    - ticker: The company's ticker symbol
    - form_type: Optional filter for specific form types

    Returns:
    - List of recent filings
    """
    sec_service = SECService()

    try:
        # Get filing metadata
        metadata = sec_service.get_filing_metadata(ticker)

        # Extract recent filings
        recent_filings = metadata.get('filings', {}).get('recent', {})

        if not recent_filings:
            return {"ticker": ticker.upper(), "filings": []}

        # Organize the data into a list of filings
        filing_keys = list(recent_filings.keys())
        num_filings = len(recent_filings.get(filing_keys[0], []))

        filings = []
        for i in range(num_filings):
            filing = {key: recent_filings[key][i] if i < len(recent_filings[key]) else None
                      for key in filing_keys}
            filings.append(filing)

        # Filter by form type if specified
        if form_type:
            filings = [f for f in filings if f.get('form') == form_type]

        return {
            "ticker": ticker.upper(),
            "cik": metadata.get('cik', ''),
            "company_name": metadata.get('name', ''),
            "filings": filings
        }
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting recent filings: {str(e)}")
