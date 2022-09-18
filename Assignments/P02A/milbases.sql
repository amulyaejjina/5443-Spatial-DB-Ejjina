-- Table: public.milbases

-- DROP TABLE IF EXISTS public.milbases;

CREATE TABLE IF NOT EXISTS public.milbases
(
    gid integer NOT NULL DEFAULT nextval('milbases_gid_seq'::regclass),
    ansicode character varying(8) COLLATE pg_catalog."default",
    areaid character varying(22) COLLATE pg_catalog."default",
    fullname character varying(100) COLLATE pg_catalog."default",
    mtfcc character varying(5) COLLATE pg_catalog."default",
    aland double precision,
    awater double precision,
    intptlat character varying(11) COLLATE pg_catalog."default",
    intptlon character varying(12) COLLATE pg_catalog."default",
    geom geometry(MultiPolygon,4326),
    CONSTRAINT milbases_pkey PRIMARY KEY (gid)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.milbases
    OWNER to amulyaejjina;
-- Index: milbases_geom_idx

-- DROP INDEX IF EXISTS public.milbases_geom_idx;

CREATE INDEX IF NOT EXISTS milbases_geom_idx
    ON public.milbases USING gist
    (geom)
    TABLESPACE pg_default;