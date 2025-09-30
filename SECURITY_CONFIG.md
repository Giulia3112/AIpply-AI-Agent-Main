# 🔒 Security Configuration Guide for AIpply API

This guide covers essential security configurations for production deployment.

## 🛡️ Essential Security Measures

### 1. Environment Variables Security

#### Create Secure Environment File
```bash
# Create .env file with secure values
cp env.example .env

# Generate secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Update .env with secure values
SECRET_KEY=your_generated_secret_key_here
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=postgresql://username:password@localhost:5432/aipply
ENVIRONMENT=production
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

#### Never Commit Secrets
```bash
# Add to .gitignore
echo ".env" >> .gitignore
echo "*.key" >> .gitignore
echo "*.pem" >> .gitignore
```

### 2. API Security Configuration

#### Update CORS Settings
```python
# In main_enhanced.py, update CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "").split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

#### Add Rate Limiting
```python
# Add rate limiting middleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Apply rate limiting to endpoints
@app.post("/api/chat")
@limiter.limit("5/minute")
async def chat(request: Request, message: ChatMessage, db: Session = Depends(get_db)):
    # Your chat logic here
```

### 3. SSL/HTTPS Configuration

#### Let's Encrypt SSL Setup
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

#### Nginx SSL Configuration
```nginx
# In nginx.conf
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # SSL Security
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
}
```

### 4. Database Security

#### PostgreSQL Security
```bash
# Update pg_hba.conf for secure authentication
sudo nano /etc/postgresql/*/main/pg_hba.conf

# Use scram-sha-256 for password encryption
local   all             all                                     scram-sha-256
host    all             all             127.0.0.1/32            scram-sha-256
host    all             all             ::1/128                 scram-sha-256

# Restart PostgreSQL
sudo systemctl restart postgresql
```

#### Database User Permissions
```sql
-- Create limited database user
CREATE USER aipply_app WITH ENCRYPTED PASSWORD 'strong_password_here';

-- Grant only necessary permissions
GRANT CONNECT ON DATABASE aipply TO aipply_app;
GRANT USAGE ON SCHEMA public TO aipply_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO aipply_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO aipply_app;

-- Revoke unnecessary permissions
REVOKE CREATE ON SCHEMA public FROM aipply_app;
```

### 5. Server Security

#### Firewall Configuration
```bash
# Install and configure UFW
sudo ufw enable

# Allow SSH
sudo ufw allow ssh

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow application port (if not using reverse proxy)
sudo ufw allow 8000/tcp

# Check status
sudo ufw status
```

#### Fail2Ban Setup
```bash
# Install fail2ban
sudo apt install fail2ban

# Configure fail2ban
sudo nano /etc/fail2ban/jail.local

# Add configuration
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3

# Start fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

#### System Updates
```bash
# Regular security updates
sudo apt update && sudo apt upgrade -y

# Enable automatic security updates
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 6. Application Security

#### Input Validation
```python
# Add input validation to API endpoints
from pydantic import BaseModel, validator
import re

class ChatMessage(BaseModel):
    message: str
    
    @validator('message')
    def validate_message(cls, v):
        if len(v) > 1000:
            raise ValueError('Message too long')
        if not re.match(r'^[a-zA-Z0-9\s.,!?-]+$', v):
            raise ValueError('Invalid characters in message')
        return v.strip()
```

#### Error Handling
```python
# Secure error handling
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log error securely
    logger.error(f"Unhandled exception: {str(exc)}")
    
    # Return generic error message
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
```

#### Request Logging
```python
# Add request logging middleware
import time
from fastapi import Request

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    
    response = await call_next(request)
    
    # Log response
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} - {process_time:.4f}s")
    
    return response
```

### 7. Monitoring and Alerting

#### Security Monitoring
```bash
# Monitor failed login attempts
sudo tail -f /var/log/auth.log | grep "Failed password"

# Monitor application logs
tail -f /var/log/aipply/app.log | grep ERROR

# Monitor database connections
sudo tail -f /var/log/postgresql/postgresql-*.log
```

#### Set Up Alerts
```bash
# Create monitoring script
cat > /usr/local/bin/security-monitor.sh << 'EOF'
#!/bin/bash

# Check for failed logins
FAILED_LOGINS=$(grep "Failed password" /var/log/auth.log | wc -l)
if [ $FAILED_LOGINS -gt 10 ]; then
    echo "High number of failed login attempts: $FAILED_LOGINS" | mail -s "Security Alert" admin@yourdomain.com
fi

# Check disk space
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "High disk usage: $DISK_USAGE%" | mail -s "Disk Alert" admin@yourdomain.com
fi

# Check if application is running
if ! curl -f http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "Application health check failed" | mail -s "App Alert" admin@yourdomain.com
fi
EOF

chmod +x /usr/local/bin/security-monitor.sh

# Add to crontab
crontab -e
# Add: */15 * * * * /usr/local/bin/security-monitor.sh
```

## 🔍 Security Testing

### Vulnerability Scanning
```bash
# Install security scanning tools
pip install bandit safety

# Scan Python code for vulnerabilities
bandit -r . -f json -o security-report.json

# Check dependencies for vulnerabilities
safety check
```

### Penetration Testing
```bash
# Test API endpoints
curl -X POST "https://yourdomain.com/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "<script>alert(1)</script>"}'

# Test rate limiting
for i in {1..10}; do
  curl "https://yourdomain.com/api/search?keyword=test"
done
```

## 📋 Security Checklist

### Pre-Deployment
- [ ] Strong passwords set for all accounts
- [ ] Environment variables secured
- [ ] SSL certificate installed
- [ ] Firewall configured
- [ ] Database permissions limited
- [ ] Rate limiting implemented
- [ ] Input validation added
- [ ] Error handling secured
- [ ] Logging configured
- [ ] Monitoring set up

### Post-Deployment
- [ ] Security headers configured
- [ ] HTTPS redirect working
- [ ] Rate limiting functional
- [ ] Database access secured
- [ ] Log monitoring active
- [ ] Backup strategy implemented
- [ ] Incident response plan ready
- [ ] Regular security updates scheduled

### Ongoing Security
- [ ] Regular security audits
- [ ] Dependency updates
- [ ] Log analysis
- [ ] Vulnerability scanning
- [ ] Penetration testing
- [ ] Security training
- [ ] Incident response drills

## 🆘 Security Incident Response

### Immediate Actions
1. **Isolate** affected systems
2. **Assess** the scope of the incident
3. **Contain** the threat
4. **Document** everything
5. **Notify** relevant parties

### Recovery Steps
1. **Clean** affected systems
2. **Patch** vulnerabilities
3. **Restore** from clean backups
4. **Monitor** for recurrence
5. **Update** security measures

## 📞 Emergency Contacts

```bash
# Create emergency contact list
cat > /etc/emergency-contacts.txt << 'EOF'
Security Team: security@yourdomain.com
System Admin: admin@yourdomain.com
Database Admin: dba@yourdomain.com
Hosting Provider: support@yourhostingprovider.com
EOF
```

---

## 🚀 Quick Security Setup

```bash
# 1. Secure environment
cp env.example .env
# Edit .env with secure values

# 2. Configure firewall
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 3. Install SSL certificate
sudo certbot --nginx -d yourdomain.com

# 4. Set up monitoring
sudo apt install fail2ban
sudo systemctl enable fail2ban

# 5. Test security
curl -I https://yourdomain.com
```

Your AIpply API is now secure and ready for production! 🔒
