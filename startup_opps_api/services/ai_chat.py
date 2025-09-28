"""
AI Chat service for conversational opportunity search
"""

import openai
import json
from typing import List, Dict, Any
from startup_opps_api.models.opportunity import Opportunity

class AIChatService:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.system_prompt = """
        You are AIpply, an AI assistant specialized in finding scholarships, fellowships, and accelerator programs.
        
        Your role:
        1. Help users find relevant opportunities based on their background, interests, and goals
        2. Provide personalized recommendations
        3. Explain opportunity requirements and deadlines
        4. Suggest application strategies
        
        Guidelines:
        - Be helpful, encouraging, and professional
        - Ask clarifying questions when needed
        - Provide specific, actionable advice
        - Always mention that opportunities should be verified on official websites
        - Focus on legitimate, well-known organizations and programs
        
        When presenting opportunities, format them clearly with:
        - Title and organization
        - Key requirements
        - Application deadline
        - Why it might be a good fit
        """
    
    async def process_user_message(self, message: str, opportunities: List[Opportunity] = None) -> str:
        """Process user message and generate AI response"""
        try:
            # Prepare context with opportunities if available
            context = ""
            if opportunities:
                context = f"\n\nHere are some relevant opportunities I found:\n"
                for i, opp in enumerate(opportunities[:5], 1):  # Limit to top 5
                    context += f"{i}. {opp.title} at {opp.organization}\n"
                    if opp.deadline:
                        context += f"   Deadline: {opp.deadline}\n"
                    if opp.url:
                        context += f"   URL: {opp.url}\n"
                    context += "\n"
            
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": message + context}
            ]
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"I apologize, but I'm having trouble processing your request right now. Please try again later. Error: {str(e)}"
    
    def extract_search_parameters(self, message: str) -> Dict[str, Any]:
        """Extract search parameters from user message using AI"""
        try:
            extraction_prompt = f"""
            Extract search parameters from this user message for finding opportunities:
            "{message}"
            
            Return a JSON object with these fields:
            - keyword: main search term (string)
            - type: "scholarship", "fellowship", "accelerator", or null (string or null)
            - region: geographic region if mentioned (string or null)
            - education_level: if mentioned (string or null)
            - field: academic/professional field if mentioned (string or null)
            
            Example: {{"keyword": "climate change", "type": "scholarship", "region": "Europe", "education_level": "graduate", "field": "environmental science"}}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": extraction_prompt}],
                max_tokens=200,
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content.strip())
            return result
            
        except Exception as e:
            # Fallback: simple keyword extraction
            return {"keyword": message, "type": None, "region": None}
    
    def generate_personalized_recommendations(self, user_profile: Dict[str, Any], opportunities: List[Opportunity]) -> str:
        """Generate personalized recommendations based on user profile and opportunities"""
        try:
            profile_text = f"""
            User Profile:
            - Background: {user_profile.get('background', 'Not specified')}
            - Interests: {user_profile.get('interests', 'Not specified')}
            - Education Level: {user_profile.get('education_level', 'Not specified')}
            - Field: {user_profile.get('field', 'Not specified')}
            - Region: {user_profile.get('region', 'Not specified')}
            """
            
            opps_text = "\n".join([
                f"- {opp.title} at {opp.organization} (Deadline: {opp.deadline or 'TBD'})"
                for opp in opportunities[:10]
            ])
            
            prompt = f"""
            {profile_text}
            
            Available Opportunities:
            {opps_text}
            
            Provide personalized recommendations for the top 3 most relevant opportunities.
            Explain why each opportunity is a good fit for this user.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return "I found some opportunities, but I'm having trouble generating personalized recommendations right now."
