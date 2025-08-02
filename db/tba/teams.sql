CREATE TABLE tba.teams (
    key TEXT PRIMARY KEY,  -- Format: frcXXXX
    team_number INTEGER NOT NULL UNIQUE,
    nickname TEXT,
    name TEXT,
    school_name TEXT,
    city TEXT,
    state_prov TEXT,
    country TEXT,
    address TEXT,
    postal_code TEXT,
    gmaps_place_id TEXT,
    gmaps_url TEXT,
    lat DECIMAL(10, 8),
    lng DECIMAL(11, 8),
    location_name TEXT,
    website TEXT,
    rookie_year INTEGER,
    motto TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for common queries
CREATE INDEX idx_teams_team_number ON tba.teams(team_number);
CREATE INDEX idx_teams_country_state ON tba.teams(country, state_prov);
CREATE INDEX idx_teams_rookie_year ON tba.teams(rookie_year);
CREATE INDEX idx_teams_city ON tba.teams(city);

-- Comments
COMMENT ON TABLE tba.teams IS 'FRC teams information from The Blue Alliance API';
COMMENT ON COLUMN tba.teams.key IS 'TBA team key with format frcXXXX';
COMMENT ON COLUMN tba.teams.team_number IS 'Official team number issued by FIRST';
COMMENT ON COLUMN tba.teams.nickname IS 'Team nickname provided by FIRST';
COMMENT ON COLUMN tba.teams.name IS 'Official long name registered with FIRST';
COMMENT ON COLUMN tba.teams.school_name IS 'Name of team school or affiliated group';
COMMENT ON COLUMN tba.teams.rookie_year IS 'First year the team officially competed';
