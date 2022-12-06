
-- Table: public.ships_guns

-- DROP TABLE IF EXISTS public.ships_guns;

CREATE TABLE IF NOT EXISTS public.ships_guns
(
    ship_id numeric NOT NULL,
    gun_id numeric NOT NULL,
    type text COLLATE pg_catalog."default",
    pos numeric,
    CONSTRAINT ships_guns_pkey PRIMARY KEY (ship_id, gun_id),
    CONSTRAINT fk_ship FOREIGN KEY (ship_id)
        REFERENCES public.ship (ship_id)
)

TABLESPACE pg_default;

-- ALTER TABLE IF EXISTS public.ships_guns
--     OWNER to postgres;

COPY public.ships_guns (ship_id, gun_id, type, pos) FROM stdin;
0	0	Mark8	20
0	1	Mark11	50
0	2	Mark11	80
0	3	Mark8	1200
1	0	Mark8	20
1	1	Mark11	50
1	2	Mark11	80
1	3	Mark8	1200
2	0	Mark8	10
2	1	Mark13	15
2	2	Mark11	55
2	3	Mark11	90
2	4	Mark8	95
3	0	Mark8	10
3	1	Mark13	15
3	2	Mark11	55
3	3	Mark11	90
3	4	Mark8	95
4	0	Mark8	10
4	1	Mark8	30
4	2	Mark13	60
4	3	Mark11	90
5	0	Mark8	10
5	1	Mark8	30
5	2	Mark13	60
5	3	Mark11	90
6	0	Mark8	20
6	1	Mark11	50
6	2	Mark11	80
6	3	Mark8	1200
7	0	Mark8	20
7	1	Mark11	50
7	2	Mark11	80
7	3	Mark8	1200
8	0	Mark8	10
8	1	Mark8	30
8	2	Mark13	60
8	3	Mark11	90
9	0	Mark8	10
9	1	Mark8	30
9	2	Mark13	60
9	3	Mark11	90
10	0	Mark8	10
10	1	Mark8	30
10	2	Mark13	60
10	3	Mark11	90
11	0	Mark8	10
11	1	Mark13	15
11	2	Mark11	55
11	3	Mark11	90
11	4	Mark8	95
12	0	Mark8	20
12	1	Mark11	50
12	2	Mark11	80
12	3	Mark8	1200
13	0	Mark8	20
13	1	Mark8	70
13	2	Mark8	160
14	0	Mark7	100
14	1	Mark7	400
14	2	Mark7	800
15	0	Mark5	10
15	1	Mark5	70
15	2	Mark5	130
15	3	Mark5	190
15	4	Mark5	250
16	0	Mark7	100
16	1	Mark7	400
16	2	Mark7	800
17	0	Mark7	40
17	1	Mark8	70
17	2	Mark8	180
18	0	Mark7	60
18	1	Mark8	120
18	2	Mark8	180
19	0	Mark7	100
19	1	Mark7	400
19	2	Mark7	800
20	0	Mark5	10
20	1	Mark5	70
20	2	Mark5	130
20	3	Mark5	190
20	4	Mark5	250
21	0	Mark15	10
21	1	Mark13	30
21	2	Mark13	40
21	3	Mark11	50
21	4	Mark11	70
22	0	Mark15	10
22	1	Mark13	30
22	2	Mark13	40
22	3	Mark11	50
22	4	Mark11	70
23	0	Mark15	10
23	1	Mark13	30
23	2	Mark13	40
23	3	Mark11	50
23	4	Mark11	70
24	0	Mark17	3
24	1	Mark15	10
24	2	Mark15	13
24	3	Mark13	17
24	4	Mark13	21
25	0	Mark17	3
25	1	Mark15	10
25	2	Mark15	13
25	3	Mark13	17
25	4	Mark13	21
\.

