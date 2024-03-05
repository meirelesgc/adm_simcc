CREATE DATABASE adm_simcc WITH OWNER = postgres ENCODING = 'UTF8' LC_COLLATE = 'pt_BR.UTF-8' LC_CTYPE = 'pt_BR.UTF-8' TABLESPACE = pg_default CONNECTION
LIMIT = -1 IS_TEMPLATE = FALSE;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
DROP TABLE IF EXISTS institution;
CREATE TABLE institution(
      institution_id uuid DEFAULT uuid_generate_v4(),
      name VARCHAR(255) NOT NULL,
      acronym VARCHAR(50) UNIQUE,
      lattes_id CHAR(12),
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (institution_id)
);
DROP TABLE IF EXISTS researcher;
CREATE TABLE researcher(
      researcher_id uuid NOT NULL DEFAULT uuid_generate_v4(),
      name VARCHAR(150) NOT NULL,
      lattes_id VARCHAR(20) NOT NULL,
      institution_id uuid NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (researcher_id),
      FOREIGN KEY (institution_id) REFERENCES institution (institution_id)
);
DROP TABLE IF EXISTS graduate_program;
CREATE TABLE graduate_program(
      graduate_program_id uuid NOT NULL DEFAULT uuid_generate_v4(),
      code VARCHAR(100) NOT NULL,
      name VARCHAR(100) NOT NULL,
      area VARCHAR(100) NOT NULL,
      modality VARCHAR(100) NOT NULL,
      TYPE VARCHAR(100) NULL,
      rating VARCHAR(5),
      institution_id uuid NOT NULL,
      description VARCHAR(500) NULL,
      url_image VARCHAR(200) NULL,
      city varchar(100) NULL,
      state varchar(4),
      visible bool DEFAULT FALSE,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (graduate_program_id),
      FOREIGN KEY (institution_id) REFERENCES institution (institution_id)
) CREATE TABLE IF NOT EXISTS graduate_program (
      graduate_program_id uuid NOT NULL DEFAULT uuid_generate_v4(),
      code character varying(100) NOT NULL,
      name character varying(100) NOT NULL,
      area character varying(100) NOT NULL,
      modality character varying(100) NOT NULL,
      type character varying(100),
      rating character varying(5),
      institution_id uuid,
      state character varying(4) DEFAULT 'BA'::character varying,
      city character varying(100) DEFAULT 'Salvador'::character varying,
      instituicao character varying(100) DEFAULT NULL::character varying,
      url_image character varying(400) DEFAULT NULL::character varying,
      region character varying(100) DEFAULT NULL::character varying,
      sigla character varying(100) DEFAULT NULL::character varying,
      CONSTRAINT graduate_program_pkey PRIMARY KEY (graduate_program_id)
);
CREATE TABLE graduate_program_researcher(
      graduate_program_id uuid NOT NULL DEFAULT uuid_generate_v4(),
      researcher_id uuid NOT NULL DEFAULT uuid_generate_v4(),
      year INTEGER,
      type_ varchar(100),
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (researcher_id) REFERENCES researcher (researcher_id),
      FOREIGN KEY (graduate_program_id) REFERENCES graduate_program (graduate_program_id)
);