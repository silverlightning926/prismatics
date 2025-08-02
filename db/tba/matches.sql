-- Main matches table
CREATE TABLE tba.matches (
    key TEXT PRIMARY KEY,  -- Format: yyyy[EVENT_CODE]_[COMP_LEVEL]m[MATCH_NUMBER]
    event_key TEXT NOT NULL REFERENCES tba.events(key) ON DELETE CASCADE,
    comp_level TEXT NOT NULL,  -- qm, ef, qf, sf, f
    set_number INTEGER NOT NULL,
    match_number INTEGER NOT NULL,
    time_scheduled BIGINT,  -- UNIX timestamp
    actual_time BIGINT,     -- UNIX timestamp
    predicted_time BIGINT,  -- UNIX timestamp
    post_result_time BIGINT, -- UNIX timestamp
    winning_alliance TEXT,   -- red, blue, or empty string
    score_breakdown JSONB,   -- Year-specific score breakdown data
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_comp_level CHECK (comp_level IN ('qm', 'ef', 'qf', 'sf', 'f')),
    CONSTRAINT chk_winning_alliance CHECK (winning_alliance IN ('red', 'blue', ''))
);

-- Match alliances (red and blue for each match)
CREATE TABLE tba.match_alliances (
    id SERIAL PRIMARY KEY,
    match_key TEXT NOT NULL REFERENCES tba.matches(key) ON DELETE CASCADE,
    alliance_color TEXT NOT NULL,  -- red or blue
    score INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_alliance_color CHECK (alliance_color IN ('red', 'blue')),
    UNIQUE(match_key, alliance_color)
);

-- Teams in each match alliance
CREATE TABLE tba.match_alliance_teams (
    id SERIAL PRIMARY KEY,
    match_alliance_id INTEGER NOT NULL REFERENCES tba.match_alliances(id) ON DELETE CASCADE,
    team_key TEXT NOT NULL REFERENCES tba.teams(key),
    is_surrogate BOOLEAN DEFAULT FALSE,
    is_dq BOOLEAN DEFAULT FALSE,
    position INTEGER,  -- 1, 2, 3 for the three robots
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_position CHECK (position IN (1, 2, 3))
);

-- Match videos
CREATE TABLE tba.match_videos (
    id SERIAL PRIMARY KEY,
    match_key TEXT NOT NULL REFERENCES tba.matches(key) ON DELETE CASCADE,
    type TEXT NOT NULL,  -- youtube, tba, etc.
    video_key TEXT NOT NULL,  -- Video identifier
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for common queries
CREATE INDEX idx_matches_event_key ON tba.matches(event_key);
CREATE INDEX idx_matches_comp_level ON tba.matches(comp_level);
CREATE INDEX idx_matches_match_number ON tba.matches(match_number);
CREATE INDEX idx_matches_time_scheduled ON tba.matches(time_scheduled);
CREATE INDEX idx_matches_winning_alliance ON tba.matches(winning_alliance);

CREATE INDEX idx_match_alliances_match_key ON tba.match_alliances(match_key);
CREATE INDEX idx_match_alliances_alliance_color ON tba.match_alliances(alliance_color);

CREATE INDEX idx_match_alliance_teams_match_alliance_id ON tba.match_alliance_teams(match_alliance_id);
CREATE INDEX idx_match_alliance_teams_team_key ON tba.match_alliance_teams(team_key);
CREATE INDEX idx_match_alliance_teams_is_surrogate ON tba.match_alliance_teams(is_surrogate);
CREATE INDEX idx_match_alliance_teams_is_dq ON tba.match_alliance_teams(is_dq);

CREATE INDEX idx_match_videos_match_key ON tba.match_videos(match_key);
CREATE INDEX idx_match_videos_type ON tba.match_videos(type);

-- Comments
COMMENT ON TABLE tba.matches IS 'FRC match information from The Blue Alliance API';
COMMENT ON TABLE tba.match_alliances IS 'Red and blue alliances for each match';
COMMENT ON TABLE tba.match_alliance_teams IS 'Teams participating in each match alliance';
COMMENT ON TABLE tba.match_videos IS 'Video recordings associated with matches';

COMMENT ON COLUMN tba.matches.key IS 'TBA match key with format yyyy[EVENT_CODE]_[COMP_LEVEL]m[MATCH_NUMBER]';
COMMENT ON COLUMN tba.matches.comp_level IS 'Competition level: qm=Qualifications, ef=Elimination Finals, qf=Quarterfinals, sf=Semifinals, f=Finals';
COMMENT ON COLUMN tba.matches.score_breakdown IS 'Year-specific detailed scoring information stored as JSON';
COMMENT ON COLUMN tba.match_alliance_teams.is_surrogate IS 'Whether this team is playing as a surrogate';
COMMENT ON COLUMN tba.match_alliance_teams.is_dq IS 'Whether this team was disqualified';
COMMENT ON COLUMN tba.match_alliance_teams.position IS 'Robot position (1, 2, or 3) within the alliance';
