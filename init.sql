-- Initialize PostgreSQL database for AIpply API

-- Create database if it doesn't exist
-- (This file is run when the PostgreSQL container starts)

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create indexes for better performance
-- (These will be created by SQLAlchemy migrations, but we can add custom ones here)

-- Set up logging
ALTER SYSTEM SET log_statement = 'all';
ALTER SYSTEM SET log_min_duration_statement = 1000;

-- Reload configuration
SELECT pg_reload_conf();
