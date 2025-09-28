from fastapi import FastAPI, Query, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import sys
import os
import asyncio
from typing import List, Optional
import logging
import json

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

# Mock AI responses (works without OpenAI)
MOCK_RESPONSES = {
    "scholarship": [
        "I found some great scholarship opportunities for you! Here are some excellent options to consider.",
        "Based on your search, I've identified several scholarship programs that match your criteria.",
        "Great news! There are multiple scholarship opportunities available in your field of interest."
    ],
    "fellowship": [
        "I've discovered some fantastic fellowship programs that could be perfect for your career goals.",
        "There are several prestigious fellowship opportunities that align with your interests.",
        "I found some excellent fellowship programs that offer great professional development opportunities."
    ],
    "accelerator": [
        "I've identified some top-tier accelerator programs that could help grow your startup.",
        "There are several accelerator programs that match your startup's stage and industry.",
        "Great opportunities! I found some accelerators that could provide funding and mentorship."
    ]
}

def get_mock_opportunities(keyword, type="scholarship"):
    """Generate mock opportunities based on search criteria"""
    opportunities = []
    
    if type == "scholarship":
        opportunities = [
            Opportunity(
                title=f"{keyword.title()} Excellence Scholarship",
                organization="Prestigious University",
                type="scholarship",
                eligibility="Open to undergraduate and graduate students",
                deadline="2025-12-31",
                url="https://example.com/scholarship"
            ),
            Opportunity(
                title=f"Global {keyword.title()} Research Grant",
                organization="International Research Foundation",
                type="scholarship",
                eligibility="Graduate students and researchers",
                deadline="2025-11-30",
                url="https://example.com/research-grant"
            ),
            Opportunity(
                title=f"{keyword.title()} Innovation Award",
                organization="Tech Innovation Hub",
                type="scholarship",
                eligibility="Students with innovative projects",
                deadline="2025-10-15",
                url="https://example.com/innovation-award"
            )
        ]
    elif type == "fellowship":
        opportunities = [
            Opportunity(
                title=f"{keyword.title()} Leadership Fellowship",
                organization="Leadership Institute",
                type="fellowship",
                eligibility="Emerging leaders in the field",
                deadline="2025-12-15",
                url="https://example.com/leadership-fellowship"
            ),
            Opportunity(
                title=f"International {keyword.title()} Fellowship",
                organization="Global Development Network",
                type="fellowship",
                eligibility="Professionals with 3+ years experience",
                deadline="2025-11-20",
                url="https://example.com/international-fellowship"
            )
        ]
    elif type == "accelerator":
        opportunities = [
            Opportunity(
                title=f"{keyword.title()} Startup Accelerator",
                organization="Tech Accelerator Hub",
                type="accelerator",
                eligibility="Early-stage startups",
                deadline="2025-12-01",
                url="https://example.com/startup-accelerator"
            ),
            Opportunity(
                title=f"Global {keyword.title()} Incubator",
                organization="Innovation Incubator",
                type="accelerator",
                eligibility="Pre-seed to seed stage startups",
                deadline="2025-11-10",
                url="https://example.com/incubator"
            )
        ]
    
    return opportunities

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
    """Search for opportunities"""
    try:
        logger.info(f"Searching for: {keyword}, type: {type}, region: {region}")
        
        # Generate mock opportunities
        opportunities = get_mock_opportunities(keyword, type or "scholarship")
        
        return opportunities
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.post("/api/chat")
async def chat_with_ai(request: dict):
    """Chat endpoint with mock AI responses"""
    try:
        message = request.get("message", "")
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Extract type from message
        message_lower = message.lower()
        if "scholarship" in message_lower:
            opp_type = "scholarship"
        elif "fellowship" in message_lower:
            opp_type = "fellowship"
        elif "accelerator" in message_lower:
            opp_type = "accelerator"
        else:
            opp_type = "scholarship"  # default
        
        # Extract keyword from message
        keywords = message.split()
        keyword = "technology"  # default
        for word in keywords:
            if len(word) > 3 and word.lower() not in ["looking", "for", "scholarship", "fellowship", "accelerator", "programs", "opportunities"]:
                keyword = word
                break
        
        # Generate AI response
        import random
        responses = MOCK_RESPONSES.get(opp_type, MOCK_RESPONSES["scholarship"])
        ai_response = random.choice(responses)
        
        # Add personalized touch
        ai_response += f" Based on your interest in {keyword}, I've found some relevant {opp_type} opportunities for you."
        
        # Get mock opportunities
        opportunities = get_mock_opportunities(keyword, opp_type)
        
        return {
            "response": ai_response,
            "opportunities": opportunities[:3]  # Return top 3
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

