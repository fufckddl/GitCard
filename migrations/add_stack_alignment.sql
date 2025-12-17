-- Migration: Add stack_alignment column to profile_cards table
-- Date: 2024
-- Description: Adds stack_alignment column to support left/center/right alignment of stack badges

-- Check if column exists before adding (MySQL doesn't support IF NOT EXISTS for ALTER TABLE)
-- Run this manually if needed, or use a migration tool

-- Add stack_alignment column
-- Note: If column already exists, this will fail. Check first with:
-- SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS 
-- WHERE TABLE_SCHEMA = 'gitcard' AND TABLE_NAME = 'profile_cards' AND COLUMN_NAME = 'stack_alignment';

ALTER TABLE profile_cards 
ADD COLUMN stack_alignment VARCHAR(10) NOT NULL DEFAULT 'center' 
AFTER show_github_stats;

-- Update existing records to have 'center' as default alignment (if needed)
UPDATE profile_cards 
SET stack_alignment = 'center' 
WHERE stack_alignment IS NULL OR stack_alignment = '';
