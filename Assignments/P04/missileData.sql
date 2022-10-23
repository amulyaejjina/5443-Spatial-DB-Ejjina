-- Table: public.missileData

-- DROP TABLE IF EXISTS public."missileData";

CREATE TABLE IF NOT EXISTS public."missileData"
(
    missile_id real NOT NULL,
    "current_time" time without time zone NOT NULL,
    current_loc geometry NOT NULL,
    target_id numeric NOT NULL,
    target_city geometry NOT NULL,
    start_time time without time zone NOT NULL,
    start_loc geometry NOT NULL,
    speed real NOT NULL,
    altitude real NOT NULL,
    CONSTRAINT "missileData_pkey" PRIMARY KEY (missile_id, "current_time", current_loc)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."missileData"
    OWNER to postgres;
