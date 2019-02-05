
CREATE TABLE IF NOT EXISTS public.users
(
    id SERIAL,
    username text COLLATE pg_catalog."default" NOT NULL,
    email text COLLATE pg_catalog."default" NOT NULL,
    password text COLLATE pg_catalog."default" NOT NULL,
    firstname text COLLATE pg_catalog."default" NOT NULL,
    lastname text COLLATE pg_catalog."default" NOT NULL,
    othernames text COLLATE pg_catalog."default" NOT NULL,
    phonenumber text COLLATE pg_catalog."default" NOT NULL,
    dteregistered text COLLATE pg_catalog."default" NOT NULL,
    isadmin boolean NOT NULL,
    CONSTRAINT users_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.users
    OWNER to postgres;



CREATE TABLE IF NOT EXISTS public.incidents
(
    id SERIAL,
    createdon timestamp without time zone,
    title text COLLATE pg_catalog."default" NOT NULL,
    comment text COLLATE pg_catalog."default" NOT NULL,
    type character varying(25) COLLATE pg_catalog."default",
    createdby integer,
    location character varying(50) COLLATE pg_catalog."default" NOT NULL,
    status character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT incidents_pkey PRIMARY KEY (id),
    CONSTRAINT incidents_createdby_fkey FOREIGN KEY (createdby)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.incidents
    OWNER to postgres;



CREATE TABLE IF NOT EXISTS public.images
(
    id SERIAL,
    incident integer NOT NULL,
    filename character varying(255) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT images_pkey PRIMARY KEY (id),
    CONSTRAINT images_incident_fkey FOREIGN KEY (incident)
        REFERENCES public.incidents (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.images
    OWNER to postgres;



CREATE TABLE IF NOT EXISTS public.videos
(
    id SERIAL,
    incident integer NOT NULL,
    filename character varying(255) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT videos_pkey PRIMARY KEY (id),
    CONSTRAINT videos_incident_fkey FOREIGN KEY (incident)
        REFERENCES public.incidents (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.videos
    OWNER to postgres;