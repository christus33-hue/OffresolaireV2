-- Schema definition for OffreSolaire project
-- Table of merchants (solar kit vendors)
CREATE TABLE IF NOT EXISTS merchants (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  website TEXT NOT NULL,
  affiliate_program TEXT,
  active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

-- Table of offers (individual solar kits)
CREATE TABLE IF NOT EXISTS offers (
  id SERIAL PRIMARY KEY,
  merchant_id INTEGER NOT NULL REFERENCES merchants(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  link TEXT NOT NULL,
  price DECIMAL(10, 2) NOT NULL,
  power_kwc DECIMAL(10, 3),
  battery_kwh DECIMAL(10, 3),
  created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

-- Table of price history (stores price snapshots for offers)
CREATE TABLE IF NOT EXISTS price_history (
  id SERIAL PRIMARY KEY,
  offer_id INTEGER NOT NULL REFERENCES offers(id) ON DELETE CASCADE,
  price DECIMAL(10, 2) NOT NULL,
  scraped_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

-- Table of newsletter subscribers
CREATE TABLE IF NOT EXISTS subscribers (
  id SERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  subscribed_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

-- Table of affiliate clicks
CREATE TABLE IF NOT EXISTS clicks (
  id SERIAL PRIMARY KEY,
  offer_id INTEGER NOT NULL REFERENCES offers(id) ON DELETE CASCADE,
  clicked_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
  session_id TEXT
);