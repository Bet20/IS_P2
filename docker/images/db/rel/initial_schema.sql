CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS POSTGIS;
CREATE EXTENSION IF NOT EXISTS POSTGIS_TOPOLOGY;

CREATE TABLE public.countries (
	id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name            VARCHAR(250) UNIQUE NOT NULL,
	geom            GEOMETRY,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE public.artists (
  id INT PRIMARY KEY UNIQUE,
  name VARCHAR(250) NOT NULL,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE public.labels (
  id INT PRIMARY KEY UNIQUE,
  name VARCHAR(250) NOT NULL,
  company_name VARCHAR(250) NOT NULL,
  created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE public.releases (
  id INT PRIMARY KEY UNIQUE,
  title VARCHAR(250),
  status VARCHAR(250),
  year VARCHAR(250),
  genre VARCHAR(250),
  style VARCHAR(250),
  country uuid,
  label_id INT,
  artist_id INT,
  notes TEXT,
  created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

ALTER TABLE releases
  ADD CONSTRAINT label_id
    FOREIGN KEY (id) REFERENCES labels
      ON DELETE CASCADE;

ALTER TABLE releases
  ADD CONSTRAINT artist_id
    FOREIGN KEY (id) REFERENCES artists
      ON DELETE CASCADE;
