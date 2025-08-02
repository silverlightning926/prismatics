-- Districts table
CREATE TABLE tba.districts (
    key TEXT PRIMARY KEY,  -- Format: yyyy + district abbreviation
    abbreviation TEXT NOT NULL,
    display_name TEXT NOT NULL,
    year INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Events table
CREATE TABLE tba.events (
    key TEXT PRIMARY KEY,  -- Format: yyyy[EVENT_CODE]
    name TEXT NOT NULL,
    event_code TEXT NOT NULL,
    event_type INTEGER NOT NULL,
    event_type_string TEXT NOT NULL,
    district_key TEXT REFERENCES tba.districts(key),
    city TEXT,
    state_prov TEXT,
    country TEXT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    year INTEGER NOT NULL,
    short_name TEXT,
    week INTEGER,
    address TEXT,
    postal_code TEXT,
    gmaps_place_id TEXT,
    gmaps_url TEXT,
    lat DECIMAL(10, 8),
    lng DECIMAL(11, 8),
    location_name TEXT,
    timezone TEXT,
    website TEXT,
    first_event_id TEXT,
    first_event_code TEXT,
    parent_event_key TEXT REFERENCES tba.events(key),
    division_keys TEXT[] DEFAULT '{}',  -- Array of division event keys
    playoff_type INTEGER,
    playoff_type_string TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Event webcasts table
CREATE TABLE tba.event_webcasts (
    id SERIAL PRIMARY KEY,
    event_key TEXT NOT NULL REFERENCES tba.events(key) ON DELETE CASCADE,
    type TEXT NOT NULL,  -- youtube, twitch, ustream, etc.
    channel TEXT NOT NULL,
    date DATE,
    file TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for common queries
CREATE INDEX idx_events_year ON tba.events(year);
CREATE INDEX idx_events_event_type ON tba.events(event_type);
CREATE INDEX idx_events_week ON tba.events(week);
CREATE INDEX idx_events_country_state ON tba.events(country, state_prov);
CREATE INDEX idx_events_start_date ON tba.events(start_date);
CREATE INDEX idx_events_district_key ON tba.events(district_key);
CREATE INDEX idx_events_parent_event_key ON tba.events(parent_event_key);

CREATE INDEX idx_districts_year ON tba.districts(year);
CREATE INDEX idx_districts_abbreviation ON tba.districts(abbreviation);

CREATE INDEX idx_event_webcasts_event_key ON tba.event_webcasts(event_key);
CREATE INDEX idx_event_webcasts_type ON tba.event_webcasts(type);
CREATE INDEX idx_events_division_keys ON tba.events USING GIN(division_keys);  -- GIN index for array queries

-- Comments
COMMENT ON TABLE tba.districts IS 'FRC districts information';
COMMENT ON TABLE tba.events IS 'FRC events information from The Blue Alliance API';
COMMENT ON TABLE tba.event_webcasts IS 'Webcast information for events';

COMMENT ON COLUMN tba.events.key IS 'TBA event key with format yyyy[EVENT_CODE]';
COMMENT ON COLUMN tba.events.event_type IS 'Event type: 0=Regional, 1=District, 2=District Championship, 3=Championship Division, 99=Offseason';
COMMENT ON COLUMN tba.events.week IS 'Week relative to first official season event, zero-indexed';
COMMENT ON COLUMN tba.events.division_keys IS 'Array of division event keys for championship events';
COMMENT ON COLUMN tba.events.playoff_type IS 'Playoff format type';
COMMENT ON COLUMN tba.event_webcasts.type IS 'Webcast provider: youtube, twitch, ustream, iframe, etc.';
