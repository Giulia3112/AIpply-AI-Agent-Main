# ⚡ Quick Start - Deploy AIpply API in 10 Minutes

This is the fastest way to get your AIpply API running for users.

## 🎯 Choose Your Deployment Method

### Option 1: Heroku (Easiest - 5 minutes)

```bash
# 1. Install Heroku CLI from https://devcenter.heroku.com/articles/heroku-cli
heroku login

# 2. Create app and deploy
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set OPENAI_API_KEY=your_openai_key_here
git push heroku main

# 3. Open your app
heroku open
```

### Option 2: Railway (Modern - 3 minutes)

1. Go to [Railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "Deploy from GitHub"
4. Select your repository
5. Add PostgreSQL service
6. Set `OPENAI_API_KEY` environment variable
7. Deploy automatically!

### Option 3: Docker (Local Testing - 2 minutes)

```bash
# 1. Clone and setup
git clone <your-repo>
cd aipply-api
cp env.example .env

# 2. Edit .env file
nano .env
# Add your OPENAI_API_KEY

# 3. Run with Docker
docker-compose up -d

# 4. Test
curl http://localhost:8000/api/health
```

## 🔑 Required Setup

### 1. Get OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com)
2. Create account and get API key
3. Add to your environment variables

### 2. Environment Variables
```bash
# Required
OPENAI_API_KEY=your_key_here

# Optional (auto-configured)
DATABASE_URL=sqlite:///./aipply.db
ENVIRONMENT=production
```

## 🧪 Test Your Deployment

### Health Check
```bash
curl https://your-app-url.com/api/health
# Should return: {"status": "healthy", "version": "2.0.0"}
```

### Test AI Chat
```bash
curl -X POST "https://your-app-url.com/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Find me scholarship opportunities"}'
```

### Test Search
```bash
curl "https://your-app-url.com/api/search?keyword=scholarship"
```

## 🌐 Access Your App

- **Frontend**: https://your-app-url.com
- **API Docs**: https://your-app-url.com/docs
- **Health Check**: https://your-app-url.com/api/health

## 🚨 Troubleshooting

### Common Issues

**OpenAI API Error:**
- Check if API key is correct
- Verify you have credits in OpenAI account

**Database Error:**
- For Heroku: PostgreSQL addon should auto-configure
- For Railway: Add PostgreSQL service in dashboard

**App Won't Start:**
- Check logs: `heroku logs --tail`
- Verify all environment variables are set

### Get Help
- Check the full [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- Review [SECURITY_CONFIG.md](SECURITY_CONFIG.md) for production
- See [DATABASE_SETUP.md](DATABASE_SETUP.md) for database issues

## 🎉 You're Done!

Your AIpply API is now live and ready for users! 

**Next Steps:**
1. Share your app URL with users
2. Monitor usage and performance
3. Set up proper domain and SSL (see full guides)
4. Configure monitoring and backups

**Happy Deploying! 🚀**
