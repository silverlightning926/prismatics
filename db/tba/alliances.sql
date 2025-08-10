-- Playoff alliances table
CREATE TABLE tba.alliances (
    id SERIAL PRIMARY KEY,
    event_key TEXT NOT NULL REFERENCES tba.events(key) ON DELETE CASCADE,
    name TEXT,  -- Alliance 1, Alliance 2, etc.
    status_level TEXT,  -- f, sf, qf, etc.
    status_status TEXT,  -- won, eliminated
    status_playoff_type INTEGER,
    status_double_elim_round TEXT,
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    ties INTEGER DEFAULT 0,
    current_level_wins INTEGER DEFAULT 0,
    current_level_losses INTEGER DEFAULT 0,
    current_level_ties INTEGER DEFAULT 0,
    playoff_average DECIMAL(10, 2),
    backup_in TEXT REFERENCES tba.teams(key),  -- Team that was called in as backup
    backup_out TEXT REFERENCES tba.teams(key), -- Team that was replaced
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Alliance picks (teams selected for the alliance)
CREATE TABLE tba.alliance_picks (
    id SERIAL PRIMARY KEY,
    alliance_id INTEGER NOT NULL REFERENCES tba.alliances(id) ON DELETE CASCADE,
    team_key TEXT NOT NULL REFERENCES tba.teams(key),
    pick_order INTEGER NOT NULL,  -- 1 = captain, 2 = first pick, etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(alliance_id, pick_order),
    UNIQUE(alliance_id, team_key)
);

-- Alliance declines (teams that declined to be picked)
CREATE TABLE tba.alliance_declines (
    id SERIAL PRIMARY KEY,
    alliance_id INTEGER NOT NULL REFERENCES tba.alliances(id) ON DELETE CASCADE,
    team_key TEXT NOT NULL REFERENCES tba.teams(key),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(alliance_id, team_key)
);

-- Indexes for common queries
CREATE INDEX idx_alliances_event_key ON tba.alliances(event_key);
CREATE INDEX idx_alliances_status_status ON tba.alliances(status_status);
CREATE INDEX idx_alliances_status_level ON tba.alliances(status_level);

CREATE INDEX idx_alliance_picks_alliance_id ON tba.alliance_picks(alliance_id);
CREATE INDEX idx_alliance_picks_team_key ON tba.alliance_picks(team_key);
CREATE INDEX idx_alliance_picks_pick_order ON tba.alliance_picks(pick_order);

CREATE INDEX idx_alliance_declines_alliance_id ON tba.alliance_declines(alliance_id);
CREATE INDEX idx_alliance_declines_team_key ON tba.alliance_declines(team_key);

-- Comments
COMMENT ON TABLE tba.alliances IS 'Playoff alliance information for events';
COMMENT ON TABLE tba.alliance_picks IS 'Teams picked for each alliance';
COMMENT ON TABLE tba.alliance_declines IS 'Teams that declined alliance invitations';

COMMENT ON COLUMN tba.alliances.name IS 'Alliance name like Alliance 1, Alliance 2, etc.';
COMMENT ON COLUMN tba.alliances.status_level IS 'Current competition level (f=Finals, sf=Semifinals, etc.)';
COMMENT ON COLUMN tba.alliances.status_status IS 'Current status: won, eliminated';
COMMENT ON COLUMN tba.alliances.status_double_elim_round IS 'Round in double elimination format';
COMMENT ON COLUMN tba.alliances.backup_in IS 'Team key that was called in as backup';
COMMENT ON COLUMN tba.alliances.backup_out IS 'Team key that was replaced by backup';
COMMENT ON COLUMN tba.alliance_picks.pick_order IS 'Order picked: 1=captain, 2=first pick, 3=second pick, 4=third pick (backup)';
