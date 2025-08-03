from fastapi import FastAPI, Request
from pydantic import BaseModel 
from typing import List, Optional, Dict 
import requests 
from bs4 import BeautifulSoup import uvicorn

app = FastAPI()
class ScrapeRequest(BaseModel): platform: str  # e.g., "linkedin", "twitter", "github" keywords: List[str] location: Optional[str] = None filters: Optional[Dict[str, str]] = None

def dummy_scraper(platform: str, keywords: List[str], location: Optional[str] = None): # Normally this would do real scraping, but for now we return dummy data print(f"Scraping {platform} with keywords: {keywords} and location: {location}") return [ { "name": "Ahmed Yasser", "profile_url": "https://linkedin.com/in/ahmed", "bio": "AI Expert | Speaker", "followers": 2500, "matched_keywords": [kw for kw in keywords if kw.lower() in "AI Expert".lower()], "posted_at": "2025-07-20" }, { "name": "Sara Adel", "profile_url": "https://linkedin.com/in/sara", "bio": "Data Science Enthusiast", "followers": 800, "matched_keywords": [kw for kw in keywords if kw.lower() in "Data Science Enthusiast".lower()], "posted_at": "2025-07-18" } ]

@app.post("/scrape") async def scrape(request: ScrapeRequest): scraped_data = dummy_scraper(request.platform, request.keywords, request.location)


filtered_data = []
for entry in scraped_data:
    if request.filters:
        passed = True
        for key, condition in request.filters.items():
            if key == "followers":
                number = int(condition[1:])
                operator = condition[0]
                if operator == '>' and entry[key] <= number:
                    passed = False
            if key == "post_date":
                if condition == "last_week" and entry["posted_at"] < "2025-07-22":
                    passed = False
        if passed:
            filtered_data.append(entry)
    else:
        filtered_data.append(entry)

return filtered_data



if name == "main": 
uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

