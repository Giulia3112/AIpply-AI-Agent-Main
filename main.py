from fastapi import FastAPI, Query
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'startup-opps-api'))

from startup_opps_api.models.opportunity import Opportunity
from startup_opps_api.services.run_scraper import scrape_opportunities

app = FastAPI(title="AIpply API", description="AI-powered startup opportunity finder")

@app.get("/")
def read_root():
    return {"message": "Welcome to AIpply API! Visit /docs for API documentation."}

@app.get("/search", response_model=list[Opportunity])
def search_opportunities(
    keyword: str = Query(..., description="e.g. climate tech"),
    region: str = Query(None),
    type: str = Query(None)  # accelerator, grant, etc.
):
    return scrape_opportunities(keyword, region, type)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
