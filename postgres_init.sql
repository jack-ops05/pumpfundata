CREATE USER reader WITH PASSWORD 'password';
CREATE USER writer WITH PASSWORD 'password';

GRANT CONNECT ON DATABASE pumpfundata TO reader;
GRANT CONNECT ON DATABASE pumpfundata TO writer;

\c pumpfundata;

GRANT USAGE ON SCHEMA public TO reader;
GRANT USAGE ON SCHEMA public TO writer;

CREATE TABLE IF NOT EXISTS events (
    signature TEXT PRIMARY KEY,
    mint TEXT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    txType TEXT NOT NULL,
    traderKey TEXT NOT NULL,
    curveKey TEXT NOT NULL,
    solAmount DECIMAL NOT NULL,
    tokenAmount DECIMAL NOT NULL,
    vSol DECIMAL NOT NULL,
    vTokens DECIMAL NOT NULL,
    marketCap DECIMAL NOT NULL
);

CREATE INDEX idx_timestamp ON events (timestamp);

GRANT SELECT ON events TO reader;
GRANT SELECT, INSERT, UPDATE, DELETE ON events TO writer;
