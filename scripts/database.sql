CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS unaccent;
CREATE TYPE relationship AS ENUM ('COLABORADOR', 'PERMANENTE');
CREATE TYPE hop_status AS ENUM ('PADRÃO', 'CARGA SOLICITADA', 'EM PROCESSAMENTO');
CREATE TABLE IF NOT EXISTS public.institution(
      institution_id uuid DEFAULT uuid_generate_v4(),
      name VARCHAR(255) NOT NULL,
      acronym VARCHAR(50) UNIQUE,
      lattes_id CHAR(16),
      load_status hop_status NOT NULL DEFAULT 'PADRÃO',
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (institution_id)
);
CREATE TABLE IF NOT EXISTS public.researcher(
      researcher_id uuid NOT NULL DEFAULT uuid_generate_v4(),
      name VARCHAR(150) NOT NULL,
      lattes_id VARCHAR(20) UNIQUE,
      institution_id uuid NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (researcher_id),
      FOREIGN KEY (institution_id) REFERENCES institution (institution_id)
);
CREATE TABLE IF NOT EXISTS public.graduate_program(
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
CREATE TABLE IF NOT EXISTS public.graduate_program_researcher(
      graduate_program_id uuid NOT NULL,
      researcher_id uuid NOT NULL,
      year INTEGER,
      type_ relationship,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (graduate_program_id, researcher_id, year),
      FOREIGN KEY (researcher_id) REFERENCES researcher (researcher_id),
      FOREIGN KEY (graduate_program_id) REFERENCES graduate_program (graduate_program_id)
);
CREATE TABLE IF NOT EXISTS public.graduate_program_student(
      graduate_program_id uuid NOT NULL DEFAULT uuid_generate_v4(),
      researcher_id uuid NOT NULL DEFAULT uuid_generate_v4(),
      year INTEGER,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (graduate_program_id, researcher_id, year),
      FOREIGN KEY (researcher_id) REFERENCES researcher (researcher_id),
      FOREIGN KEY (graduate_program_id) REFERENCES graduate_program (graduate_program_id)
);
CREATE TABLE IF NOT EXISTS public.research_group (
      research_group_id uuid NOT NULL DEFAULT uuid_generate_v4(),
      research_group_name VARCHAR(255) UNIQUE,
      researcher_id uuid,
      institution_id uuid NOT NULL,
      area VARCHAR(255),
      last_date_sent DATE,
      situation VARCHAR(50),
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      CONSTRAINT fk_researcher_id FOREIGN KEY (researcher_id) REFERENCES researcher(researcher_id),
      CONSTRAINT fk_institution_id FOREIGN KEY (institution_id) REFERENCES institution(institution_id)
);
CREATE TABLE IF NOT EXISTS public.weights (
      institution_id uuid DEFAULT uuid_generate_v4(),
      a1 numeric(20, 3),
      a2 numeric(20, 3),
      a3 numeric(20, 3),
      a4 numeric(20, 3),
      b1 numeric(20, 3),
      b2 numeric(20, 3),
      b3 numeric(20, 3),
      b4 numeric(20, 3),
      c numeric(20, 3),
      sq numeric(20, 3),
      book numeric(20, 3),
      book_chapter numeric(20, 3),
      software character varying,
      patent_granted character varying,
      patent_not_granted character varying,
      report character varying,
      f1 numeric(20, 3) DEFAULT 0,
      f2 numeric(20, 3) DEFAULT 0,
      f3 numeric(20, 3) DEFAULT 0,
      f4 numeric(20, 3) DEFAULT 0,
      f5 numeric(20, 3) DEFAULT 0
);
CREATE TABLE IF NOT EXISTS public.subsidy (
      id uuid NOT NULL DEFAULT uuid_generate_v4(),
      researcher_id uuid,
      modality_code character varying(50),
      modality_name character varying(255),
      call_title character varying(255),
      category_level_code character varying(50),
      funding_program_name character varying(255),
      institute_name character varying(255),
      aid_quantity character varying(255),
      scholarship_quantity integer
);
CREATE TABLE roles (
      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      role VARCHAR(255) NOT NULL
);
CREATE TABLE permission (
      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
      permission VARCHAR(255) NOT NULL
);
CREATE TABLE researcher_roles (
      role_id UUID NOT NULL,
      researcher_id UUID NOT NULL,
      PRIMARY KEY (role_id, researcher_id),
      FOREIGN KEY (researcher_id) REFERENCES public.researcher (researcher_id)
);
CREATE SCHEMA IF NOT EXISTS UFMG;
CREATE TABLE IF NOT EXISTS UFMG.researcher (
      id uuid,
      researcher_id uuid,
      matric character varying(200),
      inscUFMG character varying(200),
      nome character varying(200),
      genero character varying(40),
      situacao character varying(40),
      rt character varying(40),
      clas character varying(200),
      cargo character varying(40),
      classe character varying(40),
      ref character varying(200),
      titulacao character varying(40),
      entradaNaUFMG DATE,
      progressao DATE,
      semester character varying(6),
      PRIMARY KEY (matric, semester),
      FOREIGN KEY (researcher_id) REFERENCES public.researcher (researcher_id)
);
CREATE TABLE IF NOT EXISTS UFMG.technician (
      technician_id uuid NOT NULL DEFAULT uuid_generate_v4(),
      id VARCHAR(255),
      matric VARCHAR(255),
      ins_ufmg VARCHAR(255),
      nome VARCHAR(255),
      genero VARCHAR(50),
      deno_sit VARCHAR(255),
      rt VARCHAR(255),
      classe VARCHAR(255),
      cargo VARCHAR(255),
      nivel VARCHAR(255),
      ref VARCHAR(255),
      titulacao VARCHAR(255),
      setor VARCHAR(255),
      detalhe_setor VARCHAR(255),
      dting_org DATE,
      data_prog DATE,
      semester character varying(6),
      PRIMARY KEY (technician_id)
);
CREATE TABLE IF NOT EXISTS UFMG.departament (
      dep_id VARCHAR(20),
      org_cod VARCHAR(3),
      dep_nom VARCHAR(100),
      dep_des VARCHAR(500),
      dep_email VARCHAR(100),
      dep_site VARCHAR(100),
      dep_sigla VARCHAR(30),
      dep_tel VARCHAR(20),
      img_data BYTEA,
      PRIMARY KEY (dep_id)
);
CREATE TABLE IF NOT EXISTS UFMG.departament_researcher (
      dep_id VARCHAR(20),
      researcher_id uuid NOT NULL,
      PRIMARY KEY (dep_id, researcher_id),
      FOREIGN KEY (dep_id) REFERENCES UFMG.departament (dep_id),
      FOREIGN KEY (researcher_id) REFERENCES public.researcher (researcher_id)
);
CREATE TABLE UFMG.disciplines (
      dep_id VARCHAR(20),
      id VARCHAR(20),
      semester VARCHAR(20),
      department VARCHAR(255),
      academic_activity_code VARCHAR(255),
      academic_activity_name VARCHAR(255),
      academic_activity_ch VARCHAR(255),
      demanding_courses VARCHAR(255),
      oft VARCHAR(50),
      available_slots VARCHAR(50),
      occupied_slots VARCHAR(50),
      percent_occupied_slots VARCHAR(50),
      schedule VARCHAR(255),
      language VARCHAR(50),
      researcher_id uuid [],
      researcher_name VARCHAR [],
      status VARCHAR(50),
      workload VARCHAR []
);
CREATE TABLE technician_roles (
      role_id UUID NOT NULL,
      technician_id UUID NOT NULL,
      PRIMARY KEY (role_id, technician_id),
      FOREIGN KEY (technician_id) REFERENCES UFMG.technician (technician_id)
);
CREATE TABLE incite_graduate_program(
      incite_graduate_program_id uuid NOT NULL DEFAULT uuid_generate_v4(),
      name VARCHAR(255) NOT NULL,
      description VARCHAR(500) NULL,
      link VARCHAR(500) NULL,
      institution_id uuid NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      visible bool DEFAULT FALSE,
      PRIMARY KEY (incite_graduate_program_id),
      FOREIGN KEY (institution_id) REFERENCES institution (institution_id)
);
CREATE TABLE incite_graduate_program_researcher(
      incite_graduate_program_id uuid NOT NULL DEFAULT uuid_generate_v4(),
      researcher_id uuid NOT NULL DEFAULT uuid_generate_v4(),
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (incite_graduate_program_id, researcher_id),
      FOREIGN KEY (researcher_id) REFERENCES researcher (researcher_id),
      FOREIGN KEY (incite_graduate_program_id) REFERENCES incite_graduate_program (incite_graduate_program_id)
);