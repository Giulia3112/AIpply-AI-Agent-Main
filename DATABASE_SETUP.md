# 🗄️ Database Setup Guide for AIpply API

This guide covers database setup for both development and production environments.

## 📊 Database Options

### Option 1: SQLite (Development)
- **Best for**: Local development, testing
- **Pros**: No setup required, file-based
- **Cons**: Not suitable for production, limited concurrency

### Option 2: PostgreSQL (Production)
- **Best for**: Production deployments
- **Pros**: Robust, scalable, ACID compliant
- **Cons**: Requires setup and maintenance

## 🚀 Quick Setup

### SQLite Setup (Default)
```bash
# No additional setup required
# Database file will be created automatically at: ./aipply.db
python main_enhanced.py
```

### PostgreSQL Setup

#### Using Docker (Recommended)
```bash
# Start PostgreSQL with Docker Compose
docker-compose up -d postgres

# Database will be available at:
# Host: localhost
# Port: 5432
# Database: aipply
# Username: aipply_user
# Password: aipply_password
```

#### Manual PostgreSQL Installation

**Ubuntu/Debian:**
```bash
# Install PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE aipply;
CREATE USER aipply_user WITH ENCRYPTED PASSWORD 'aipply_password';
GRANT ALL PRIVILEGES ON DATABASE aipply TO aipply_user;
\q
```

**macOS:**
```bash
# Install PostgreSQL
brew install postgresql
brew services start postgresql

# Create database and user
createdb aipply
psql aipply
CREATE USER aipply_user WITH ENCRYPTED PASSWORD 'aipply_password';
GRANT ALL PRIVILEGES ON DATABASE aipply TO aipply_user;
\q
```

**Windows:**
1. Download PostgreSQL from https://www.postgresql.org/download/windows/
2. Install with default settings
3. Use pgAdmin or psql to create database and user

## 🔧 Environment Configuration

### Update Environment Variables

Create or update your `.env` file:

```bash
# For SQLite (development)
DATABASE_URL=sqlite:///./aipply.db

# For PostgreSQL (production)
DATABASE_URL=postgresql://aipply_user:aipply_password@localhost:5432/aipply

# For Docker PostgreSQL
DATABASE_URL=postgresql://aipply_user:aipply_password@postgres:5432/aipply
```

### Cloud Database Options

#### Heroku Postgres
```bash
# Add Heroku Postgres addon
heroku addons:create heroku-postgresql:hobby-dev

# Get database URL
heroku config:get DATABASE_URL
```

#### Railway PostgreSQL
1. Add PostgreSQL service in Railway dashboard
2. Copy the generated DATABASE_URL
3. Set it as environment variable

#### DigitalOcean Managed Database
1. Create PostgreSQL cluster in DigitalOcean
2. Get connection details
3. Update DATABASE_URL environment variable

#### AWS RDS
```bash
# Create RDS PostgreSQL instance
# Update DATABASE_URL with RDS endpoint
DATABASE_URL=postgresql://username:password@your-rds-endpoint.amazonaws.com:5432/aipply
```

## 🔄 Database Migrations

### Automatic Schema Creation
The application automatically creates tables on startup:

```python
# This happens automatically in main_enhanced.py
create_tables()
```

### Manual Schema Management (Optional)

If you need more control over migrations:

```bash
# Install Alembic (already in requirements.txt)
pip install alembic

# Initialize migrations
alembic init migrations

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

## 📈 Database Optimization

### Indexes for Better Performance
```sql
-- Add these indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_opportunities_title ON opportunities(title);
CREATE INDEX IF NOT EXISTS idx_opportunities_type ON opportunities(type);
CREATE INDEX IF NOT EXISTS idx_opportunities_deadline ON opportunities(deadline);
CREATE INDEX IF NOT EXISTS idx_opportunities_created_at ON opportunities(created_at);

-- Full-text search index
CREATE INDEX IF NOT EXISTS idx_opportunities_search ON opportunities USING gin(to_tsvector('english', title || ' ' || description));
```

### Connection Pooling
```python
# Add to your database configuration
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
```

## 🔒 Security Best Practices

### Database Security
```bash
# Change default passwords
# Use strong passwords (12+ characters)
# Limit database access to application servers only
# Enable SSL connections in production
# Regular security updates
```

### Environment Variables Security
```bash
# Never commit database credentials to version control
# Use environment variables or secrets management
# Rotate credentials regularly
# Use least privilege principle
```

## 🧪 Testing Database Setup

### Test Connection
```bash
# Test SQLite
python -c "from startup_opps_api.database.database import get_db; print('SQLite connection OK')"

# Test PostgreSQL
python -c "from startup_opps_api.database.database import get_db; db = next(get_db()); print('PostgreSQL connection OK')"
```

### Test API Endpoints
```bash
# Test search endpoint
curl "http://localhost:8000/api/search?keyword=scholarship"

# Test health endpoint
curl "http://localhost:8000/api/health"
```

## 🔍 Monitoring and Maintenance

### Database Monitoring
```sql
-- Check database size
SELECT pg_size_pretty(pg_database_size('aipply'));

-- Check table sizes
SELECT schemaname,tablename,pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables WHERE schemaname = 'public' ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Check slow queries
SELECT query, mean_time, calls FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;
```

### Backup Strategy
```bash
# PostgreSQL backup
pg_dump -h localhost -U aipply_user aipply > backup_$(date +%Y%m%d).sql

# Restore backup
psql -h localhost -U aipply_user aipply < backup_20240101.sql

# Automated backups (cron job)
0 2 * * * pg_dump -h localhost -U aipply_user aipply > /backups/aipply_$(date +\%Y\%m\%d).sql
```

## 🆘 Troubleshooting

### Common Issues

**Connection Refused:**
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Check if port is listening
netstat -tulpn | grep 5432
```

**Authentication Failed:**
```bash
# Check pg_hba.conf
sudo nano /etc/postgresql/*/main/pg_hba.conf

# Restart PostgreSQL
sudo systemctl restart postgresql
```

**Database Doesn't Exist:**
```bash
# Create database
createdb aipply

# Or connect to postgres and create
psql -U postgres
CREATE DATABASE aipply;
```

**Permission Denied:**
```bash
# Grant permissions
psql -U postgres -d aipply
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO aipply_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO aipply_user;
```

## 📋 Production Checklist

- [ ] PostgreSQL installed and configured
- [ ] Strong passwords set
- [ ] SSL connections enabled
- [ ] Database backups configured
- [ ] Monitoring set up
- [ ] Connection pooling configured
- [ ] Indexes created for performance
- [ ] Security updates applied
- [ ] Access controls configured
- [ ] Health checks working

---

## 🚀 Quick Commands

```bash
# Start with SQLite (development)
python main_enhanced.py

# Start with Docker PostgreSQL
docker-compose up -d postgres

# Test database connection
curl http://localhost:8000/api/health

# Backup database
pg_dump -h localhost -U aipply_user aipply > backup.sql
```

Your database is now ready for AIpply API! 🎉
