-- =====================================================
-- ScanTrac Database Schema
-- Run: mysql -u root -p < database.sql
-- =====================================================

CREATE DATABASE IF NOT EXISTS scantrac_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE scantrac_db;

-- Users
CREATE TABLE IF NOT EXISTS users (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(120) NOT NULL,
    email       VARCHAR(120) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    plan        ENUM('free','pro','business') DEFAULT 'free',
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Products
CREATE TABLE IF NOT EXISTS products (
    id                   INT AUTO_INCREMENT PRIMARY KEY,
    user_id              INT NOT NULL,
    name                 VARCHAR(200) NOT NULL,
    category             VARCHAR(100),
    description          TEXT,
    custom_fields_schema TEXT COMMENT 'JSON array of {label, key, type}',
    created_at           DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at           DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Batches
CREATE TABLE IF NOT EXISTS batches (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    product_id      INT NOT NULL,
    batch_code      VARCHAR(50) NOT NULL UNIQUE,
    qr_token        VARCHAR(64) NOT NULL UNIQUE,
    qr_image_path   VARCHAR(255),
    field_data      TEXT COMMENT 'JSON key-value of custom field values',
    production_date DATE,
    expiry_date     DATE,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    INDEX idx_product (product_id),
    INDEX idx_token (qr_token)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Scan Logs
CREATE TABLE IF NOT EXISTS scan_logs (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    batch_id   INT NOT NULL,
    ip_address VARCHAR(45),
    user_agent VARCHAR(255),
    city       VARCHAR(100),
    scanned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (batch_id) REFERENCES batches(id) ON DELETE CASCADE,
    INDEX idx_batch (batch_id),
    INDEX idx_scanned_at (scanned_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
