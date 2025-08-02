-- Event rankings table
CREATE TABLE tba.rankings (
    id SERIAL PRIMARY KEY,
    event_key TEXT NOT NULL REFERENCES tba.events(key) ON DELETE CASCADE,
    team_key TEXT NOT NULL REFERENCES tba.teams(key),
    rank INTEGER NOT NULL,
    matches_played INTEGER NOT NULL,
    qual_average INTEGER,
    wins INTEGER NOT NULL DEFAULT 0,
    losses INTEGER NOT NULL DEFAULT 0,
    ties INTEGER NOT NULL DEFAULT 0,
    dq INTEGER NOT NULL DEFAULT 0,  -- Number of disqualifications
    extra_stats DECIMAL[] DEFAULT '{}',  -- Array of additional statistics
    sort_orders DECIMAL[] DEFAULT '{}',  -- Year-specific sorting criteria
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(event_key, team_key),
    UNIQUE(event_key, rank)
);

-- Extra stats info (metadata for extra_stats array)
CREATE TABLE tba.ranking_extra_stats_info (
    id SERIAL PRIMARY KEY,
    event_key TEXT NOT NULL REFERENCES tba.events(key) ON DELETE CASCADE,
    name TEXT NOT NULL,
    precision_digits INTEGER DEFAULT 0,
    array_position INTEGER NOT NULL,  -- Position in the extra_stats array
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(event_key, array_position)
);

-- Sort order info (metadata for sort_orders array)
CREATE TABLE tba.ranking_sort_order_info (
    id SERIAL PRIMARY KEY,
    event_key TEXT NOT NULL REFERENCES tba.events(key) ON DELETE CASCADE,
    name TEXT NOT NULL,
    precision_digits INTEGER DEFAULT 0,
    array_position INTEGER NOT NULL,  -- Position in the sort_orders array
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(event_key, array_position)
);

-- Indexes for common queries
CREATE INDEX idx_rankings_event_key ON tba.rankings(event_key);
CREATE INDEX idx_rankings_team_key ON tba.rankings(team_key);
CREATE INDEX idx_rankings_rank ON tba.rankings(rank);
CREATE INDEX idx_rankings_wins_losses ON tba.rankings(wins, losses);
CREATE INDEX idx_rankings_matches_played ON tba.rankings(matches_played);

CREATE INDEX idx_ranking_extra_stats_info_event_key ON tba.ranking_extra_stats_info(event_key);
CREATE INDEX idx_ranking_sort_order_info_event_key ON tba.ranking_sort_order_info(event_key);

-- Comments
COMMENT ON TABLE tba.rankings IS 'Team rankings at FRC events';
COMMENT ON TABLE tba.ranking_extra_stats_info IS 'Metadata for extra statistics in rankings';
COMMENT ON TABLE tba.ranking_sort_order_info IS 'Metadata for sort order criteria in rankings';

COMMENT ON COLUMN tba.rankings.rank IS 'Team rank at the event (1 = first place)';
COMMENT ON COLUMN tba.rankings.qual_average IS 'Average match score during qualifications (year-specific)';
COMMENT ON COLUMN tba.rankings.dq IS 'Number of times team was disqualified';
COMMENT ON COLUMN tba.rankings.extra_stats IS 'Array of additional TBA-calculated statistics';
COMMENT ON COLUMN tba.rankings.sort_orders IS 'Array of year-specific ranking criteria values';
COMMENT ON COLUMN tba.ranking_extra_stats_info.precision_digits IS 'Number of decimal places for this statistic';
COMMENT ON COLUMN tba.ranking_extra_stats_info.array_position IS 'Index position in the extra_stats array';
