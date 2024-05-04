CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS unaccent;

CREATE TABLE IF NOT EXISTS research_group (
    research_group_id  uuid NOT NULL DEFAULT uuid_generate_v4(),
    research_group_name VARCHAR(255),
    researcher_id uuid,
    institution_id uuid,
    area VARCHAR(255),
    last_date_sent DATE,
    situation VARCHAR(50),
    file_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_researcher_id FOREIGN KEY (researcher_id) REFERENCES researcher(researcher_id),
    CONSTRAINT fk_institution_id FOREIGN KEY (institution_id) REFERENCES institution(institution_id)
);

CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_research_group_updated_at
BEFORE UPDATE ON research_group
FOR EACH ROW
WHEN (OLD.* IS DISTINCT FROM NEW.*)
EXECUTE FUNCTION update_updated_at();
