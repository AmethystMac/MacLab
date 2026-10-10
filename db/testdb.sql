
DROP TABLE IF EXISTS users CASCADE;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), 
    name VARCHAR(40) NOT NULL,
    age INT NOT NULL,
    sex VARCHAR(6)
);