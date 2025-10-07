CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
  
CREATE TABLE IF NOT EXISTS user_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION create_user_data_automatically()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO user_data (user_id) VALUES (NEW.id);
    RAISE NOTICE 'Automatically created user_data for user_id: %', NEW.id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- create trigger after insert on users table
CREATE TRIGGER trg_create_user_data
AFTER INSERT ON users
FOR EACH ROW
EXECUTE FUNCTION create_user_data_automatically();