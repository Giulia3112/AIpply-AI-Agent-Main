"""
Database models for AIpply API
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Opportunity(Base):
    __tablename__ = "opportunities"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    organization = Column(String(200), nullable=False, index=True)
    type = Column(String(50), nullable=False, index=True)  # scholarship, fellowship, accelerator
    description = Column(Text)
    eligibility = Column(Text)
    deadline = Column(DateTime)
    url = Column(String(1000), nullable=False)
    source = Column(String(100), nullable=False)
    region = Column(String(100))
    amount = Column(String(100))  # For scholarships/fellowships
    duration = Column(String(100))  # For fellowships
    requirements = Column(JSON)  # Structured requirements
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user_searches = relationship("UserSearch", back_populates="opportunity")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(100))
    background = Column(Text)
    interests = Column(JSON)
    education_level = Column(String(50))
    field = Column(String(100))
    region = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    searches = relationship("UserSearch", back_populates="user")
    chat_sessions = relationship("ChatSession", back_populates="user")

class UserSearch(Base):
    __tablename__ = "user_searches"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"))
    search_query = Column(String(500))
    search_type = Column(String(50))
    clicked_at = Column(DateTime)
    applied_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="searches")
    opportunity = relationship("Opportunity", back_populates="user_searches")

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    session_id = Column(String(100), unique=True, index=True)
    messages = Column(JSON)  # Store chat history
    context = Column(JSON)  # Store user context and preferences
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="chat_sessions")

class ScrapingLog(Base):
    __tablename__ = "scraping_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(100), nullable=False)
    url = Column(String(1000), nullable=False)
    status = Column(String(20), nullable=False)  # success, error, partial
    opportunities_found = Column(Integer, default=0)
    error_message = Column(Text)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    duration_seconds = Column(Integer)
