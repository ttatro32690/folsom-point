-- Create a user for our application
CREATE USER ai_agent_user WITH PASSWORD 'secure_password';

-- Create the database
CREATE DATABASE ai_agent_db;

-- Grant privileges to the user
GRANT ALL PRIVILEGES ON DATABASE ai_agent_db TO ai_agent_user;

-- Connect to the newly created database
\c ai_agent_db

-- Create initial tables (adjust these according to your needs)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE agents (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Add more tables as needed for your application

-- Grant privileges on all tables to the user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ai_agent_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO ai_agent_user;
