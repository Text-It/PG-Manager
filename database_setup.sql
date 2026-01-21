-- Database Setup / Reset Script
-- WARNING: This script will DELETE ALL DATA in the database.
-- Usage: psql -U postgres -d pg_manager -f database_setup.sql

-- 1. Clean up existing tables (Drop in reverse dependency order)
DROP TABLE IF EXISTS complaints CASCADE;
DROP TABLE IF EXISTS payments CASCADE;
DROP TABLE IF EXISTS tenants CASCADE;
DROP TABLE IF EXISTS rooms CASCADE;
DROP TABLE IF EXISTS properties CASCADE;
DROP TABLE IF EXISTS owners CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- 2. Clean up types
DROP TYPE IF EXISTS user_role;

-- 3. Create Enum Type
CREATE TYPE user_role AS ENUM ('OWNER', 'TENANT', 'ADMIN');

-- 4. Create Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role user_role NOT NULL DEFAULT 'TENANT',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. Create Owners Table
CREATE TABLE owners (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    full_name VARCHAR(100),
    phone_number VARCHAR(20),
    business_name VARCHAR(100),
    upi_id VARCHAR(50),
    qr_code_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_owners_user_id UNIQUE (user_id)
);

-- 6. Create Properties Table
CREATE TABLE properties (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id UUID REFERENCES owners(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL DEFAULT 'Main Building',
    address TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 7. Create Rooms Table
CREATE TABLE rooms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID REFERENCES properties(id) ON DELETE CASCADE,
    room_number VARCHAR(20) NOT NULL,
    floor_number INTEGER DEFAULT 0,
    capacity INTEGER DEFAULT 2,
    rent_amount INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_room_property UNIQUE (property_id, room_number)
);

-- 8. Create Tenants Table
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id UUID REFERENCES owners(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL, 
    
    -- Room Linkage
    room_id UUID REFERENCES rooms(id) ON DELETE SET NULL,
    
    -- Personal Details
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    room_number VARCHAR(20), -- Kept for historical/display redundancy if needed
    bed_number VARCHAR(10),
    
    -- Financials
    monthly_rent INTEGER NOT NULL,
    security_deposit INTEGER,
    lease_start DATE,
    lease_end DATE,
    
    -- Status
    onboarding_status VARCHAR(20) DEFAULT 'PENDING',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Unique Email per Owner
    CONSTRAINT uq_tenant_email_owner UNIQUE (owner_id, email)
);

-- 9. Create Payments Table
CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    amount INTEGER NOT NULL,
    payment_date DATE DEFAULT CURRENT_DATE,
    payment_month VARCHAR(7), -- 'YYYY-MM'
    status VARCHAR(20) DEFAULT 'COMPLETED',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 10. Create Complaints Table
CREATE TABLE complaints (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    owner_id UUID REFERENCES owners(id) ON DELETE CASCADE,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'PENDING',
    priority VARCHAR(10) DEFAULT 'MEDIUM',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 11. Create Indexes (Optimization)
CREATE INDEX idx_payments_month ON payments(payment_month);
CREATE INDEX idx_payments_tenant ON payments(tenant_id);
CREATE INDEX idx_complaints_owner ON complaints(owner_id);
CREATE INDEX idx_complaints_status ON complaints(status);
