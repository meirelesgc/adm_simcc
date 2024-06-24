CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS unaccent;
CREATE TYPE relationship AS ENUM ('COLABORADOR', 'PERMANENTE');
CREATE TYPE status AS ENUM ('PADRÃO', 'CARGA SOLICITADA', 'EM PROCESSAMENTO');

CREATE TABLE institution(
      institution_id uuid DEFAULT uuid_generate_v4(),
      name VARCHAR(255) NOT NULL,
      acronym VARCHAR(50) UNIQUE,
      lattes_id CHAR(12),
      load_status status NOT NULL DEFAULT 'PADRÃO',
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (institution_id)
);

CREATE TABLE researcher(
      researcher_id uuid NOT NULL DEFAULT uuid_generate_v4(),
      name VARCHAR(150) NOT NULL,
      lattes_id VARCHAR(20) UNIQUE,
      institution_id uuid NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (researcher_id),
      FOREIGN KEY (institution_id) REFERENCES institution (institution_id)
);

CREATE TABLE graduate_program(
      graduate_program_id uuid NOT NULL DEFAULT uuid_generate_v4(),
      code VARCHAR(100),
      name VARCHAR(100) NOT NULL,
      area VARCHAR(100) NOT NULL,
      modality VARCHAR(100) NOT NULL,
      TYPE VARCHAR(100) NULL,
      rating VARCHAR(5),
      institution_id uuid NOT NULL,
      state character varying(4) DEFAULT 'BA'::character varying,
      city character varying(100) DEFAULT 'Salvador'::character varying,
      region character varying(100) DEFAULT 'Nordeste'::character varying,
      instituicao character varying(100),
      url_image VARCHAR(200) NULL,
      sigla character varying(100),
      description VARCHAR(500) NULL,
      visible bool DEFAULT FALSE,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (graduate_program_id),
      FOREIGN KEY (institution_id) REFERENCES institution (institution_id)
);

CREATE TABLE graduate_program_researcher(
      graduate_program_id uuid NOT NULL DEFAULT uuid_generate_v4(),
      researcher_id uuid NOT NULL DEFAULT uuid_generate_v4(),
      year INTEGER,
      type_ relationship,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (graduate_program_id, researcher_id, year),
      FOREIGN KEY (researcher_id) REFERENCES researcher (researcher_id),
      FOREIGN KEY (graduate_program_id) REFERENCES graduate_program (graduate_program_id)
);

CREATE TABLE graduate_program_student(
      graduate_program_id uuid NOT NULL DEFAULT uuid_generate_v4(),
      researcher_id uuid NOT NULL DEFAULT uuid_generate_v4(),
      year INTEGER,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (graduate_program_id, researcher_id, year),
      FOREIGN KEY (researcher_id) REFERENCES researcher (researcher_id),
      FOREIGN KEY (graduate_program_id) REFERENCES graduate_program (graduate_program_id)
);

CREATE TABLE research_group (
    research_group_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    research_group_name VARCHAR(255),
    researcher_id uuid,
    institution_id uuid,
    area VARCHAR(255),
    last_date_sent DATE,
    situation VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_researcher_id FOREIGN KEY (researcher_id) REFERENCES researcher(researcher_id),
    CONSTRAINT fk_institution_id FOREIGN KEY (institution_id) REFERENCES institution(institution_id)
);

CREATE TABLE public.weights
(
    institution_id uuid DEFAULT uuid_generate_v4(),
    a1 numeric(10,3),
    a2 numeric(10,3),
    a3 numeric(10,3),
    a4 numeric(10,3),
    b1 numeric(10,3),
    b2 numeric(10,3),
    b3 numeric(10,3),
    b4 numeric(10,3),
    c numeric(10,3),
    sq numeric(10,3),
    book numeric(10,3),
    book_chapter numeric(10,3),
    software character varying,
    patent_granted character varying,
    patent_not_granted character varying,
    report character varying,
    f1 numeric(10,3) DEFAULT 0,
    f2 numeric(10,3) DEFAULT 0,
    f3 numeric(10,3) DEFAULT 0,
    f4 numeric(10,3) DEFAULT 0,
    f5 numeric(10,3) DEFAULT 0
);

CREATE TABLE IF NOT EXISTS public.subsidy
(
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    researcher_id uuid NOT NULL,
    modality_code character varying(50) ,
    modality_name character varying(255) ,
    call_title character varying(255) ,
    category_level_code character varying(50) ,
    funding_program_name character varying(255) ,
    institute_name character varying(255) ,
    aid_quantity integer,
    scholarship_quantity integer
)