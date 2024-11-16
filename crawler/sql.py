from psycopg import sql

init_sql = sql.SQL(
    """
-- Enable the PostGIS extension (if not already enabled)
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create the stores table (if it does not already exist)
CREATE TABLE IF NOT EXISTS stores (
    store_id VARCHAR(6) NOT NULL,
    store_name VARCHAR(50) NOT NULL,
    address VARCHAR(100) NOT NULL,
    coordinates GEOGRAPHY(Point) NOT NULL,
    family_mart_services VARCHAR(255) NULL,

    -- only have 7-11 and FamilyMart
    brand VARCHAR(10) NOT NULL CHECK (brand IN ('7-11', 'FamilyMart')),
    PRIMARY KEY (store_id, brand)
);

-- Create a GIST index on the coordinates
CREATE INDEX IF NOT EXISTS idx_stores_coordinates ON stores USING GIST (coordinates);

-- Enable the vector extension (if not already enabled)
CREATE EXTENSION IF NOT EXISTS vector;

-- Create the stores_embeddings table (if it does not already exist)
CREATE TABLE IF NOT EXISTS stores_embeddings (
    store_id VARCHAR(6) NOT NULL,
    brand VARCHAR(10) NOT NULL CHECK (brand IN ('7-11', 'FamilyMart')),
    embedding VECTOR(1536) NOT NULL,
    raw_embedding TEXT NOT NULL,
    FOREIGN KEY (store_id, brand) REFERENCES stores(store_id, brand) ON DELETE CASCADE,
    PRIMARY KEY (store_id, brand)
);
"""
)

upsert_stores = sql.SQL(
    """
INSERT INTO stores
    (store_id, store_name, address, coordinates, brand)
VALUES
    (%(store_id)s, %(store_name)s, %(address)s, ST_SetSRID(ST_MakePoint(%(longitude)s, %(latitude)s), 4326), %(brand)s)
ON CONFLICT
    (store_id, brand) DO UPDATE
SET
    store_name = EXCLUDED.store_name,
    address = EXCLUDED.address,
    coordinates = EXCLUDED.coordinates
;
"""
)

upsert_stores_embeddings = sql.SQL(
    """
INSERT INTO stores_embeddings
    (store_id, brand, embedding, raw_embedding)
VALUES
    (%(store_id)s, %(brand)s, %(embedding)s, %(raw_embedding)s)
ON CONFLICT
    (store_id, brand)
DO UPDATE
SET
    store_id = EXCLUDED.store_id,
    brand = EXCLUDED.brand,
    embedding = EXCLUDED.embedding,
    raw_embedding = EXCLUDED.raw_embedding
;
"""
)
