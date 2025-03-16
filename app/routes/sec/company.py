# app/routes/sec/company.py
from fastapi import APIRouter, HTTPException
from app.services.sec_api import SECService
from app.models import CompanyInfo
from typing import List

router = APIRouter(prefix="/company")

@router.get("/{ticker}", response_model=CompanyInfo, summary="Get Company Info")
async def get_company_info(ticker: str):
    """
    Get basic company information by ticker symbol.

    Parameters:
    - ticker: The company's ticker symbol (e.g., AAPL for Apple)

    Returns:
    - Basic company information including CIK, ticker, and company name
    """
    sec_service = SECService()

    try:
        # Get company data
        cik = sec_service.get_cik_by_ticker(ticker)
        companies_df = sec_service.get_company_tickers()

        # Find company by CIK
        company_row = companies_df[companies_df['cik_str'] == cik].iloc[0]

        return CompanyInfo(
            cik=cik,
            ticker=company_row['ticker'],
            title=company_row['title']
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@router.get("/search/{query}", response_model=List[CompanyInfo], summary="Search Companies")
async def search_companies(query: str):
    """
    Search for companies by name or ticker.

    Parameters:
    - query: Search string to match against company names or tickers

    Returns:
    - List of matching companies
    """
    sec_service = SECService()

    try:
        # Get all companies
        companies_df = sec_service.get_company_tickers()

        # Convert query to lowercase for case-insensitive search
        query = query.lower()

        # Filter companies that match the query
        matches = companies_df[
            companies_df['ticker'].str.lower().str.contains(query) |
            companies_df['title'].str.lower().str.contains(query)
        ]

        # Limit to first 10 matches to avoid large responses
        matches = matches.head(10)

        if matches.empty:
            return []

        # Convert to list of CompanyInfo
        return [
            CompanyInfo(
                cik=row['cik_str'],
                ticker=row['ticker'],
                title=row['title']
            ) for _, row in matches.iterrows()
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching companies: {str(e)}")
