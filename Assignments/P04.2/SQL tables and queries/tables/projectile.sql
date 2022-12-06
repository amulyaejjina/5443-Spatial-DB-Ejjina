
-- Table: public.projectile

-- DROP TABLE IF EXISTS public.projectile;

CREATE TABLE IF NOT EXISTS public.projectile
(
    name text COLLATE pg_catalog."default" NOT NULL,
    mm numeric,
    kg numeric,
    CONSTRAINT projectile_pkey PRIMARY KEY (name)
)

TABLESPACE pg_default;

-- ALTER TABLE IF EXISTS public.projectile
--     OWNER to postgres;

COPY public.projectile (name, mm, kg) FROM stdin;
MK15	400	1020
MK13	400	1165
MK8	450	1310
MK3	450	1455
MK1	475	1600
\.
