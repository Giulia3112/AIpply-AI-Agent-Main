from fastapi import FastAPI, Query, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import sys
import os
import asyncio
from typing import List, Optional
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), 'startup_opps_api'))

from startup_opps_api.models.opportunity import Opportunity

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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Initialize AI service
ai_service = None
try:
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        from startup_opps_api.services.ai_chat import AIChatService
        ai_service = AIChatService(openai_key)
        logger.info("AI service initialized successfully")
    else:
        logger.warning("No OpenAI API key found")
except Exception as e:
    logger.warning(f"OpenAI service not available: {e}")

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
    type: str = Query(None, description="Type: scholarship, fellowship, or accelerator")
):
    """Search for opportunities - simplified version"""
    try:
        logger.info(f"Searching for: {keyword}, type: {type}, region: {region}")
        
        # Return mock data for now
        mock_opportunities = [
            Opportunity(
                title=f"{keyword} Scholarship Program",
                organization="Example University",
                type=type or "scholarship",
                eligibility="Open to all students",
                deadline="2025-12-31",
                url="https://example.com/scholarship"
            ),
            Opportunity(
                title=f"{keyword} Fellowship Opportunity",
                organization="Research Institute",
                type=type or "fellowship",
                eligibility="Graduate students",
                deadline="2025-11-30",
                url="https://example.com/fellowship"
            )
        ]
        
        return mock_opportunities
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.post("/api/chat")
async def chat_with_ai(request: dict):
    """Chat endpoint with AI integration"""
    try:
        message = request.get("message", "")
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        if not ai_service:
            return {
                "response": "AI chat is not available. Please set OPENAI_API_KEY environment variable.",
                "opportunities": []
            }
        
        # Generate AI response
        ai_response = await ai_service.process_user_message(message, [])
        
        return {
            "response": ai_response,
            "opportunities": []
        }
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return {
            "response": "I'm sorry, I encountered an error. Please try again.",
            "opportunities": []
        }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "2.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
