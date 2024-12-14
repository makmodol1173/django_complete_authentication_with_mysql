-- Create the database
CREATE DATABASE IF NOT EXISTS auth;

-- Use the database
USE auth;

-- Create the users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,        -- Auto-increment primary key for id
    name VARCHAR(255) NOT NULL,                -- Name cannot be null
    email VARCHAR(255) NOT NULL UNIQUE,        -- Email must be unique and cannot be null
    password VARCHAR(255) NOT NULL,            -- Password cannot be null
    role VARCHAR(50) NOT NULL,                  -- Role cannot be null
    profile_picture VARCHAR(100);

);
