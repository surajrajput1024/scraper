from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel
import json
from scraper_service import ScraperService  
from storage_service import StorageService  
from typing import List, Optional

# Sample Authentication Dependency
def authenticate(token: str = Query(..., description="Auth token")):
    """
    Authentication dependency to check if the provided token is valid.
    """
    if token != "static-token-123":
        raise HTTPException(status_code=401, detail="Unauthorized")

class ScrapeRequest(BaseModel):
    max_pages: int = 1  
    proxy: Optional[str] = None  # proxy for scraping requests (now ignored)

app = FastAPI()

scraper_service = ScraperService()


@app.post("/scrape")
async def scrape_products(request: ScrapeRequest, token: str = Depends(authenticate)):
    """
    Endpoint to scrape product data from a website, based on the number of pages.
    """
    try:
        scraped_data = scraper_service.scrape("https://dentalstall.com/shop/", request.max_pages)
        
        if not scraped_data:
            raise HTTPException(status_code=500, detail="No product data found or failed to scrape.")
        
        storage_service = StorageService()
        file_name = storage_service.save_to_json(scraped_data)
        
        return {"status": "success", "file": file_name, "scraped_data": scraped_data}
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
