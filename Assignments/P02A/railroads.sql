-- Table: public.railroads

-- DROP TABLE IF EXISTS public.railroads;

CREATE TABLE IF NOT EXISTS public.railroads
(
    gid integer NOT NULL DEFAULT nextval('railroads_gid_seq'::regclass),
    linearid character varying(22) COLLATE pg_catalog."default",
    fullname character varying(100) COLLATE pg_catalog."default",
    mtfcc character varying(5) COLLATE pg_catalog."default",
    geom geometry(MultiLineString,4326),
    CONSTRAINT railroads_pkey PRIMARY KEY (gid)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.railroads
    OWNER to amulyaejjina;
-- Index: railroads_geom_idx

-- DROP INDEX IF EXISTS public.railroads_geom_idx;

CREATE INDEX IF NOT EXISTS railroads_geom_idx
    ON public.railroads USING gist
    (geom)
    TABLESPACE pg_default;