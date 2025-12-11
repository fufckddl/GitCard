-- GitCard Database Schema
-- MySQL Database Schema for GitCard Application

-- Create database (run this manually if needed)
-- CREATE DATABASE IF NOT EXISTS gitcard CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- USE gitcard;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    github_id INT UNIQUE NOT NULL,
    github_login VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    email VARCHAR(255),
    avatar_url VARCHAR(500),
    html_url VARCHAR(500),
    github_access_token VARCHAR(500),
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    last_login_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    INDEX idx_github_id (github_id),
    INDEX idx_github_login (github_login)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Profile cards table
CREATE TABLE IF NOT EXISTS profile_cards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    card_title VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    tagline VARCHAR(500),
    primary_color VARCHAR(7) NOT NULL DEFAULT '#667eea',
    gradient VARCHAR(500) NOT NULL,
    show_stacks BOOLEAN NOT NULL DEFAULT TRUE,
    show_contact BOOLEAN NOT NULL DEFAULT TRUE,
    show_github_stats BOOLEAN NOT NULL DEFAULT TRUE,
    stacks JSON NOT NULL DEFAULT (JSON_ARRAY()),
    contacts JSON NOT NULL DEFAULT (JSON_ARRAY()),
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    INDEX idx_user_id (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

