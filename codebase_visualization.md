# AIpply Codebase Visualization

## Architecture Overview

```mermaid
graph TB
    subgraph "Frontend (Web Interface)"
        A[index.html<br/>Chat Interface] --> B[script.js<br/>Chat Logic]
        A --> C[style.css<br/>Styling]
        A --> D[Images<br/>logo1.png, fundo.jpeg]
    end
    
    subgraph "Backend API"
        E[main.py<br/>FastAPI Server] --> F[models/opportunity.py<br/>Data Model]
        E --> G[services/run_scraper.py<br/>Scraping Service]
    end
    
    subgraph "Scraping Module"
        G --> H[scraper/scrapy_spider.py<br/>Web Scraper]
        H --> I[scraper/parser.py<br/>Data Parser]
    end
    
    subgraph "External Services"
        J[Firebase Functions<br/>AI Processing]
        K[Web Sources<br/>Opportunity Websites]
    end
    
    A -.->|HTTP Requests| E
    B -.->|Firebase SDK| J
    G -.->|Web Scraping| K
    
    style A fill:#e1f5fe
    style E fill:#f3e5f5
    style J fill:#fff3e0
    style K fill:#e8f5e8
```

## Component Details

### 1. Frontend Components
- **index.html**: Main chat interface with input field and message display
- **script.js**: Handles user interactions, message sending, and Firebase integration
- **style.css**: Modern glassmorphism design with background image
- **Images**: Logo and background assets

### 2. Backend API
- **main.py**: FastAPI server with `/search` endpoint
- **models/opportunity.py**: Pydantic model for opportunity data structure
- **services/run_scraper.py**: Orchestrates web scraping process

### 3. Data Flow
1. User types message in frontend
2. JavaScript sends to Firebase Functions for AI processing
3. AI response triggers backend API call
4. Backend uses Scrapy to scrape opportunity websites
5. Results returned and displayed in chat interface

## Technology Stack
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Python, FastAPI, Pydantic
- **Scraping**: Scrapy, Twisted
- **Cloud**: Firebase Functions
- **Styling**: Glassmorphism design with backdrop blur effects

## File Structure
```
AIpply-API-main/
├── frontend/                 # Web interface
│   ├── index.html           # Main HTML page
│   ├── script.js            # Chat functionality
│   ├── style.css            # Styling
│   └── img/                 # Assets
├── main.py                  # FastAPI server entry point
├── requirements.txt         # Python dependencies
└── startup-opps-api/        # Core API module
    ├── main.py             # (Empty - likely moved to root)
    ├── models/
    │   └── opportunity.py   # Data models
    ├── services/
    │   └── run_scraper.py   # Scraping orchestration
    └── scraper/
        ├── scrapy_spider.py # Web scraper
        └── parser.py        # Data parsing
```

## Key Features
- **Real-time Chat Interface**: Modern chat UI with message timestamps
- **AI-Powered Matching**: Uses Firebase Functions for intelligent opportunity matching
- **Web Scraping**: Automatically gathers startup opportunities from various sources
- **Responsive Design**: Glassmorphism UI with backdrop blur effects
- **RESTful API**: FastAPI-based backend with structured endpoints
