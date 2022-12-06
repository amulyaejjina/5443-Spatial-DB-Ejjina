-- Table: public.torpedo_state

-- DROP TABLE IF EXISTS public.torpedo_state;

CREATE TABLE IF NOT EXISTS public.torpedo_state
(
    ship_id numeric NOT NULL,
    torpedo_id numeric NOT NULL,
    speed numeric,
    location text COLLATE pg_catalog."default",
    name text COLLATE pg_catalog."default",
    CONSTRAINT torpedo_state_pkey PRIMARY KEY (ship_id, torpedo_id),
    CONSTRAINT fk_name FOREIGN KEY (name)
        REFERENCES public.torpedo (name),
    CONSTRAINT fk_ship FOREIGN KEY (ship_id)
        REFERENCES public.ship (ship_id) 
)

TABLESPACE pg_default;

-- ALTER TABLE IF EXISTS public.torpedo_state
--     OWNER to postgres;-     OWNER to postgres;

COPY public.torpedo_state (ship_id, torpedo_id, speed, location, name) FROM stdin;
21	0	40	bow, port, ahead	MK39
21	1	60	bow, starboard, ahead	MK35
21	2	50	astern, port, ahead	MK31
21	3	50	bow, port, ahead	MK31
22	0	50	bow, port, ahead	MK31
22	1	60	bow, starboard, ahead	MK35
22	2	40	astern, port, ahead	MK39
22	3	40	bow, port, ahead	MK39
23	0	60	bow, port, ahead	MK35
23	1	102	bow, starboard, ahead	MK42
23	2	60	astern, port, ahead	MK35
23	3	60	bow, port, ahead	MK35
24	0	50	bow, port, ahead	MK31
24	1	102	bow, starboard, ahead	MK42
24	2	102	astern, port, ahead	MK42
24	3	60	bow, port, ahead	MK35
25	0	40	bow, port, ahead	MK39
25	1	102	bow, starboard, ahead	MK42
25	2	40	astern, port, ahead	MK39
25	3	60	bow, port, ahead	MK35
\.