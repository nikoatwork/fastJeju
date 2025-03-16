# app/services/sec_api.py
import requests
import pandas as pd
from fastapi import HTTPException

class SECService:
    def __init__(self, user_agent="fastjeju@example.com"):
        self.headers = {'User-Agent': user_agent}
        self.company_tickers_url = "https://www.sec.gov/files/company_tickers.json"
        self.base_filing_url = "https://data.sec.gov/submissions/CIK{}.json"

    def get_company_tickers(self):
        """Get all company tickers from SEC"""
        try:
            response = requests.get(
                self.company_tickers_url,
                headers=self.headers
            )
            response.raise_for_status()  # Raise exception for HTTP errors

            # Convert to DataFrame
            company_data = pd.DataFrame.from_dict(response.json(), orient='index')

            # Add leading zeros to CIK
            company_data['cik_str'] = company_data['cik_str'].astype(str).str.zfill(10)

            return company_data
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=503, detail=f"Error fetching company data from SEC: {str(e)}")

    def get_cik_by_ticker(self, ticker):
        """Get CIK number by company ticker"""
        company_data = self.get_company_tickers()

        # Find the company by ticker (case insensitive)
        ticker = ticker.upper()
        matches = company_data[company_data['ticker'] == ticker]

        if matches.empty:
            raise HTTPException(status_code=404, detail=f"Company with ticker '{ticker}' not found")

        # Return the CIK with leading zeros
        return matches.iloc[0]['cik_str']

    def get_filing_metadata(self, ticker):
        """Get filing metadata for a company by ticker"""
        try:
            cik = self.get_cik_by_ticker(ticker)

            filing_url = self.base_filing_url.format(cik)
            response = requests.get(
                filing_url,
                headers=self.headers
            )
            response.raise_for_status()

            return response.json()
        except HTTPException:
            # Re-raise HTTP exceptions
            raise
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=503, detail=f"Error fetching filing metadata from SEC: {str(e)}")
