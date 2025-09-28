# 🎓 AIpply - AI-Powered Opportunity Finder

AIpply is an intelligent platform that helps users find scholarships, fellowships, and accelerator programs through conversational AI and web scraping.

## ✨ Features

- **🤖 AI Chat Interface**: Conversational search for opportunities
- **🔍 Smart Web Scraping**: Scrapes 30+ trusted opportunity sources
- **📊 Database Storage**: SQLite/PostgreSQL for data persistence
- **🎨 Modern UI**: Beautiful chat interface with opportunity cards
- **⚡ Fast API**: FastAPI with async support
- **🐳 Docker Ready**: Easy deployment with Docker

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- OpenAI API key (for AI chat functionality)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd aipply-api
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env and add your OpenAI API key
   ```

4. **Run the application**
   ```bash
   # For development (preserves your frontend)
   python main.py
   
   # For enhanced version with AI chat
   python main_enhanced.py
   ```

5. **Access the application**
   - Frontend: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/api/health

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Using Docker directly

```bash
# Build image
docker build -t aipply-api .

# Run container
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key_here aipply-api
```

## 📊 Opportunity Sources

### Scholarships
- [Partiu Intercambio](https://partiuintercambio.org/bolsas-de-estudo/)
- [WeMakeScholars](https://www.wemakescholars.com/scholarship)
- [Fulbright Brazil](https://fulbright.org.br/bolsas-para-brasileiros/)
- [Fulbright US](https://fulbright.org.br/awards-for-us-citizens/)

### Fellowships
- [ProFellow](https://www.profellow.com/open-calls/)
- [Opportunities for Youth](https://opportunitiesforyouth.org/)
- [Audacious Project](https://www.audaciousproject.org/apply)
- [Start Fellowship](https://www.startglobal.org/start-fellowship)
- [Westerwelle Foundation](https://westerwelle-foundation.com/programs/young-founders-program/)
- [Watson Impact Fellowships](https://watson.is/impact-fellowships/)
- [Kauffman Fellows](https://www.kauffmanfellows.org/)
- [ChangeMakerXchange](https://changemakerxchange.org/ai/)

### Accelerators
- [YouNoodle](https://platform.younoodle.com/competition/apply)
- [OpportunityDesk](https://opportunitydesk.org/)
- [F6S Programs](https://www.f6s.com/programs)
- [SEBRAE Startups](https://programas.sebraestartups.com.br/programas)
- [Station F](https://stationf.co/programs)
- [Emerge Americas](https://emergeamericas.com/programs/)
- [Startup World Cup](https://www.startupworldcup.io/)
- [Global Startup Awards](https://www.globalstartupawards.com/)
- [Web Summit](https://websummit.com/startups/)
- [TechCrunch Disrupt](https://techcrunch.com/events/tc-disrupt-2025/)
- [BRICS Women Startups](https://bricswomen.com/pt/brics-womensstartups-contest/)
- [NextStep Accelerator](https://nextstepaccelerator.com/investment/)
- [Decelera Ventures](https://www.decelera.ventures/)
- [Ventiur](https://ventiur.net/)
- [776 Foundation](https://www.776.org/)
- [500 Global](https://flagship.aplica.500.co/)
- [Techstars](https://www.techstars.com/accelerators)

## 🔧 API Endpoints

### Main Endpoints
- `GET /` - Serve frontend interface
- `GET /api/` - API welcome message
- `GET /api/health` - Health check

### Search Endpoints
- `GET /api/search` - Search opportunities
  - Parameters: `keyword`, `region`, `type`
- `POST /api/chat` - AI chat interface
  - Body: `{"message": "your message"}`
- `GET /api/opportunities` - Get stored opportunities

## 🛠️ Development

### Project Structure
```
aipply-api/
├── main.py                 # Original API (preserves frontend)
├── main_enhanced.py        # Enhanced API with AI chat
├── startup_opps_api/
│   ├── models/            # Pydantic models
│   ├── services/          # Business logic
│   ├── scraper/           # Web scraping
│   └── database/          # Database models
├── frontend/              # Your existing frontend
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
└── README.md
```

### Adding New Sources

1. Edit `startup_opps_api/scraper/opportunity_sources.py`
2. Add new source configuration with selectors
3. Test with the scraper

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for chat | Required |
| `DATABASE_URL` | Database connection string | `sqlite:///./aipply.db` |
| `ENVIRONMENT` | Environment (development/production) | `development` |

## 🚀 Production Deployment

### Using Cloud Providers

1. **Heroku**
   ```bash
   # Add Heroku Postgres addon
   heroku addons:create heroku-postgresql:hobby-dev
   
   # Set environment variables
   heroku config:set OPENAI_API_KEY=your_key
   
   # Deploy
   git push heroku main
   ```

2. **Railway**
   ```bash
   # Connect GitHub repo
   # Set environment variables in dashboard
   # Deploy automatically
   ```

3. **DigitalOcean App Platform**
   ```bash
   # Create app from GitHub
   # Set environment variables
   # Deploy
   ```

### Using VPS

1. **Install Docker**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   ```

2. **Deploy with Docker Compose**
   ```bash
   git clone <your-repo>
   cd aipply-api
   docker-compose up -d
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For support, please open an issue on GitHub or contact the development team.

---

**Made with ❤️ for opportunity seekers worldwide**
