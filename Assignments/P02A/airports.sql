-- Table: public.airports

-- DROP TABLE IF EXISTS public.airports;

CREATE TABLE IF NOT EXISTS public.airports
(
    id numeric,
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    city character varying(64) COLLATE pg_catalog."default" NOT NULL,
    country character varying(256) COLLATE pg_catalog."default" NOT NULL,
    _3code character varying(3) COLLATE pg_catalog."default" NOT NULL,
    _4code character varying(4) COLLATE pg_catalog."default" NOT NULL,
    lat double precision NOT NULL,
    lon double precision NOT NULL,
    elevation character varying(10) COLLATE pg_catalog."default",
    gmt character varying(10) COLLATE pg_catalog."default",
    tz_short character varying(3) COLLATE pg_catalog."default",
    time_zone character varying(64) COLLATE pg_catalog."default",
    type character varying(32) COLLATE pg_catalog."default",
    type2 character varying(32) COLLATE pg_catalog."default",
    geom geometry(Point,4326)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.airports
    OWNER to amulyaejjina;
-- Index: airports_geom_idx

-- DROP INDEX IF EXISTS public.airports_geom_idx;

CREATE INDEX IF NOT EXISTS airports_geom_idx
    ON public.airports USING gist
    (geom)
    TABLESPACE pg_default;