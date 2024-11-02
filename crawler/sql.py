from psycopg import sql

init_sql = sql.SQL(
    """
-- enable the PostGIS extension (if not already enabled)
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create the stores table (if it does not already exist)
CREATE TABLE IF NOT EXISTS stores (
    store_id VARCHAR(6) PRIMARY KEY,
    store_name VARCHAR(50) NOT NULL,
    address VARCHAR(100) NOT NULL,
    coordinates GEOGRAPHY(Point) NOT NULL,

    -- only have 7-11 and FamilyMart
    brand VARCHAR(10) NOT NULL CHECK (brand IN ('7-11', 'FamilyMart'))
);
"""
)

upsert_stores = sql.SQL(
    """
INSERT INTO stores (store_id, store_name, address, coordinates, brand)
VALUES (%(store_id)s, %(store_name)s, %(address)s, ST_SetSRID(ST_MakePoint(%(longitude)s, %(latitude)s), 4326), %(brand)s)
ON CONFLICT (store_id) DO UPDATE
SET store_name = EXCLUDED.store_name, address = EXCLUDED.address, coordinates = EXCLUDED.coordinates, brand = EXCLUDED.brand;
"""
)
