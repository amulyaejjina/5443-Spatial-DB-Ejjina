
-- Table: public.cartridge

-- DROP TABLE IF EXISTS public.cartridge;

CREATE TABLE IF NOT EXISTS public.cartridge
(
    name text COLLATE pg_catalog."default" NOT NULL,
    mm numeric,
    kg numeric,
    ms numeric,
    explosive numeric,
    CONSTRAINT cartridge_pkey PRIMARY KEY (name)
)

TABLESPACE pg_default;

-- ALTER TABLE IF EXISTS public.cartridge
--     OWNER to postgres;

COPY public.cartridge (name, mm, kg, ms, explosive) FROM stdin;
APEX	25	0.222	970	0
SAPHEI/SD	35	0.55	1055	0
L/70 HE	57	2.4	1020	0
120 IM HE	120	17	1030	8
155 HE-ER	155	44.4	935	11
\.
