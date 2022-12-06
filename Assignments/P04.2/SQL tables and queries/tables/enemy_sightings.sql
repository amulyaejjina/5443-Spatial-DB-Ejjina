-- Table: public.enemy_sightings

-- DROP TABLE IF EXISTS public.enemy_sightings;

CREATE TABLE IF NOT EXISTS public.enemy_sightings
(
    fleet_id text COLLATE pg_catalog."default" NOT NULL,
    location_range text COLLATE pg_catalog."default",
    bbox_range geometry,
    CONSTRAINT enemy_sightings_pkey PRIMARY KEY (fleet_id)
)

TABLESPACE pg_default;

-- ALTER TABLE IF EXISTS public.enemy_sightings
--     OWNER to postgres;