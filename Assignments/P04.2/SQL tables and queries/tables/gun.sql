
-- Table: public.gun

-- DROP TABLE IF EXISTS public.gun;

CREATE TABLE IF NOT EXISTS public.gun
(
    name text COLLATE pg_catalog."default" NOT NULL,
    info text COLLATE pg_catalog."default",
    mm numeric,
    ammocat text COLLATE pg_catalog."default",
    ammotype text COLLATE pg_catalog."default",
    propellantkg numeric,
    rof numeric,
    turnrate numeric,
    CONSTRAINT gun_pkey PRIMARY KEY (name)
)

TABLESPACE pg_default;

-- ALTER TABLE IF EXISTS public.gun
--     OWNER to postgres;

COPY public.gun (name, info, mm, ammocat, ammotype, propellantkg, rof, turnrate) FROM stdin;
Mark17	25mm Chain gun	25	cartridge	APEX	0	250	360
Mark15	35 mm gatlin gun. 	35	cartridge	SAPHEI/SD	0	200	360
Mark13	57 mm gatlin gun. 	57	cartridge	L/70 HE	0	150	360
Mark11	120 mm deck mounted gun. Each Mark11 has 2 barrels that can shoot simultaneuously.	120	cartridge	120 IM HE	0	2	360
Mark8	400 mm deck mounted gun. Each Mark7 has 3 barrels that can shoot simultaneuously.	400	projectile	MK13	120	3	90
Mark7	450 mm deck mounted gun. Each Mark7 has 3 barrels that can shoot simultaneuously.	450	projectile	MK3	120	3	90
Mark5	475 mm deck mounted gun. Each Mark5 has 3 barrels that can shoot simultaneuously.	475	projectile	MK1	120	3	90
\.
