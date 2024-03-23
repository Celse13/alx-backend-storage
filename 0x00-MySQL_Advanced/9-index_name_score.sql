-- creating index on the firstname

CREATE INDEX idx_name_first_score ON names (name(1), score);
