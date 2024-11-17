from psycopg import sql

init_sql = sql.SQL(
    """
-- Enable the PostGIS extension (if not already enabled)
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create store services enum type
CREATE TYPE services AS ENUM (
    'lcoffee',       -- 咖啡複合店
    'rpotato',       -- 烤馬鈴薯
    'hd',            -- 哈逗堡
    'smart',         -- 智能咖啡機
    'tea',           -- 福爾摩沙茶館
    'sweetpotato',   -- 夯番薯
    'photo',         -- 相片立可得
    'cs',            -- ChargeSPOT
    'goro',          -- gogoro電池交換站
    'ice',           -- Fami!ce(有販售店)
    'icecream',      -- Fami!ce(單口味店)
    'twoice',        -- Fami!ce(雙口味店)
    'famiice',       -- Fami!ce(特殊造型店)
    'card',          -- Picard (法國優質冷凍食品)
    'super',         -- 全家FamiSuper選品超市店
    'tanhou',        -- 天和鮮物
    'rest',          -- 休憩區
    'toilet',        -- 廁所
    'veg',           -- 生鮮蔬菜
    'laundry',       -- Fami自助洗衣
    'dessert',       -- SOHOT炎選-現烤點心
    'costco',        -- 好市多專區
    'hada',          -- 哈根達斯冰箱
    'tripk',         -- 鼎王麻辣蛋
    'fresh',         -- 蒸新鮮
    'eco',           -- 塑環真®循環杯
    'grill',         -- SOHOT炎選-炸烤物
    'cooknow',       -- 馬尚煮
    'hogan',         -- 哈肯舖
    'bear',          -- 小熊菓子
    'musl',          -- 穆斯林友善商品店舖
    'npork',         -- 無豬肉熱食友善店
    'unknow'         -- 未知
);

C

-- Create the stores table (if it does not already exist)
CREATE TABLE IF NOT EXISTS stores (
    store_id VARCHAR(6) NOT NULL,
    store_name VARCHAR(50) NOT NULL,
    address VARCHAR(100) NOT NULL,
    coordinates GEOGRAPHY(Point) NOT NULL,
    services services[] NOT NULL,  

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
