
-- Table: public.torpedo

-- DROP TABLE IF EXISTS public.torpedo;

CREATE TABLE IF NOT EXISTS public.torpedo
(
    name text COLLATE pg_catalog."default" NOT NULL,
    guidance text COLLATE pg_catalog."default",
    diameter numeric,
    speed numeric,
    kg numeric,
    warheadsize numeric,
    range numeric,
    CONSTRAINT torpedo_pkey PRIMARY KEY (name)
)

TABLESPACE pg_default;

-- ALTER TABLE IF EXISTS public.torpedo
--     OWNER to postgres;

COPY public.torpedo (name, guidance, diameter, speed, kg, warheadsize, range) FROM stdin;
MK42	0	570	102	1814	363	25000
MK39	wire guided	533	40	1000	175	13000
MK35	accoustic	533	60	1300	150	15000
MK31	accoustic	570	50	1000	150	15000
\.
