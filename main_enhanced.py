from fastapi import FastAPI, Query, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import sys
import os
import asyncio
from typing import List, Optional
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

sys.path.append(os.path.join(os.path.dirname(__file__), 'startup_opps_api'))

from startup_opps_api.models.opportunity import Opportunity
from startup_opps_api.services.run_scraper import scrape_opportunities
from startup_opps_api.services.ai_chat import AIChatService
from startup_opps_api.database.database import get_db, create_tables
from startup_opps_api.database.models import Opportunity as DBOpportunity, User, ChatSession

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AIpply API", 
    description="AI-powered opportunity finder for scholarships, fellowships, and accelerators",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (your existing frontend)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Add MIME type for CSS and JS files
from fastapi.responses import FileResponse
from fastapi import Response

# Initialize AI service (you'll need to set OPENAI_API_KEY environment variable)
ai_service = None
try:
    openai_key = os.getenv("MY OPEN AI API KEY")
    if openai_key:
        ai_service = AIChatService(openai_key)
except Exception as e:
    logger.warning(f"OpenAI service not available: {e}")

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()
    logger.info("Database tables created")

@app.get("/")
async def serve_frontend():
    """Serve the existing frontend"""
    return FileResponse("frontend/index.html")

@app.get("/style.css")
async def serve_css():
    """Serve CSS file"""
    return FileResponse("frontend/style.css", media_type="text/css")

@app.get("/script.js")
async def serve_js():
    """Serve JavaScript file"""
    return FileResponse("frontend/script.js", media_type="application/javascript")

@app.get("/img/{filename}")
async def serve_images(filename: str):
    """Serve image files"""
    return FileResponse(f"frontend/img/{filename}")

@app.get("/api/")
def read_root():
    return {"message": "Welcome to AIpply API! Visit /docs for API documentation."}

@app.get("/api/search", response_model=List[Opportunity])
async def search_opportunities(
    keyword: str = Query(..., description="Search term, e.g. 'climate tech'"),
    region: str = Query(None, description="Geographic region"),
    type: str = Query(None, description="Type: scholarship, fellowship, or accelerator"),
    background_tasks: BackgroundTasks = None
):
    """Search for opportunities with enhanced error handling"""
    try:
        logger.info(f"Searching for: {keyword}, type: {type}, region: {region}")
        
        # Run scraping in background
        opportunities = await asyncio.get_event_loop().run_in_executor(
            None, scrape_opportunities, keyword, region, type
        )
        
        # Log search for analytics
        if background_tasks:
            background_tasks.add_task(log_search, keyword, type, region, len(opportunities))
        
        return opportunities
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.post("/api/chat")
async def chat_with_ai(request: dict, db: Session = Depends(get_db)):
    """Chat endpoint with AI integration"""
    try:
        message = request.get("message", "")
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        if not ai_service:
            return {
                "response": "AI chat is not available. Please use the /api/search endpoint instead.",
                "opportunities": []
            }
        
        # Extract search parameters from user message
        search_params = ai_service.extract_search_parameters(message)
        
        # Search for opportunities
        opportunities = []
        if search_params.get("keyword"):
            opportunities = await asyncio.get_event_loop().run_in_executor(
                None, scrape_opportunities, 
                search_params["keyword"], 
                search_params.get("region"), 
                search_params.get("type")
            )
        
        # Generate AI response
        ai_response = await ai_service.process_user_message(message, opportunities)
        
        return {
            "response": ai_response,
            "opportunities": opportunities[:5]  # Limit to top 5
        }
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return {
            "response": "I'm sorry, I encountered an error. Please try again.",
            "opportunities": []
        }

@app.get("/api/opportunities", response_model=List[Opportunity])
async def get_opportunities(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    type: str = Query(None),
    db: Session = Depends(get_db)
):
    """Get opportunities from database"""
    query = db.query(DBOpportunity).filter(DBOpportunity.is_active == True)
    
    if type:
        query = query.filter(DBOpportunity.type == type)
    
    opportunities = query.offset(skip).limit(limit).all()
    
    return [
        Opportunity(
            title=opp.title,
            organization=opp.organization,
            type=opp.type,
            eligibility=opp.eligibility,
            deadline=opp.deadline.isoformat() if opp.deadline else None,
            url=opp.url
        )
        for opp in opportunities
    ]

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "2.0.0"}

async def log_search(keyword: str, type: str, region: str, count: int):
    """Log search for analytics"""
    logger.info(f"Search logged: {keyword}, {type}, {region}, found {count} opportunities")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
