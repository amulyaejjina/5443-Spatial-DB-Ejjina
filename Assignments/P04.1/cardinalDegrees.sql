-- Table: public.cardinaldegrees

-- DROP TABLE IF EXISTS public.cardinaldegrees;

CREATE TABLE IF NOT EXISTS public.cardinaldegrees
(
    direction character varying(3) COLLATE pg_catalog."default" NOT NULL,
    start_degree numeric(11,8),
    middle_degree numeric(11,8),
    end_degree numeric(11,8)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.cardinaldegrees
    OWNER to postgres;