-- ETags table for caching HTTP responses
CREATE TABLE etags (
    endpoint TEXT PRIMARY KEY,
    etag TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for common queries
CREATE INDEX idx_etags_endpoint ON etags(endpoint);
CREATE INDEX idx_etags_created_at ON etags(created_at);

-- Comments
COMMENT ON TABLE etags IS 'HTTP ETags for caching API responses';
COMMENT ON COLUMN etags.endpoint IS 'API endpoint or resource identifier';
COMMENT ON COLUMN etags.etag IS 'ETag value returned by the API for caching';
