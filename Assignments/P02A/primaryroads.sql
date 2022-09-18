-- Table: public.primaryroads

-- DROP TABLE IF EXISTS public.primaryroads;

CREATE TABLE IF NOT EXISTS public.primaryroads
(
    gid integer NOT NULL DEFAULT nextval('primaryroads_gid_seq'::regclass),
    linearid character varying(22) COLLATE pg_catalog."default",
    fullname character varying(100) COLLATE pg_catalog."default",
    rttyp character varying(1) COLLATE pg_catalog."default",
    mtfcc character varying(5) COLLATE pg_catalog."default",
    geom geometry(MultiLineString,4326),
    CONSTRAINT primaryroads_pkey PRIMARY KEY (gid)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.primaryroads
    OWNER to amulyaejjina;
-- Index: primaryroads_geom_idx

-- DROP INDEX IF EXISTS public.primaryroads_geom_idx;

CREATE INDEX IF NOT EXISTS primaryroads_geom_idx
    ON public.primaryroads USING gist
    (geom)
    TABLESPACE pg_default;