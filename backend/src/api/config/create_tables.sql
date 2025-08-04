-- Create extension for UUID if not exists
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =========================
-- Table: users
-- =========================
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- =========================
-- Table: uploaded_pdfs
-- =========================
CREATE TABLE uploaded_pdfs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    content BYTEA NOT NULL,               -- PDF file content stored as binary
    file_size INTEGER,
    uploaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    user_id UUID NOT NULL,
    CONSTRAINT fk_uploaded_pdfs_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
