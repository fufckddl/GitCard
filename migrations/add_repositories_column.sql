-- Migration: Add repositories column to profile_cards table
-- Date: 2024
-- Description: Adds repositories column to store selected GitHub repositories (max 8)

-- Check if column exists before adding
-- Run this query first to check:
-- SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS 
-- WHERE TABLE_SCHEMA = 'gitcard' AND TABLE_NAME = 'profile_cards' AND COLUMN_NAME = 'repositories';

-- Add repositories column
-- Note: If column already exists, this will fail. Check first with the query above.

ALTER TABLE profile_cards 
ADD COLUMN repositories JSON NOT NULL DEFAULT (JSON_ARRAY()) 
AFTER contacts;

-- Update existing records to have empty array as default (if needed)
UPDATE profile_cards 
SET repositories = JSON_ARRAY() 
WHERE repositories IS NULL;
