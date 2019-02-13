
CREATE TABLE IF NOT EXISTS public.users
(
    id SERIAL,
    username text COLLATE pg_catalog."default" NOT NULL,
    email text COLLATE pg_catalog."default" UNIQUE NOT NULL,
    password text COLLATE pg_catalog."default" NOT NULL,
    firstname text COLLATE pg_catalog."default" NOT NULL,
    lastname text COLLATE pg_catalog."default" NOT NULL,
    othernames text COLLATE pg_catalog."default" NOT NULL,
    phonenumber text COLLATE pg_catalog."default" NOT NULL,
    dteregistered text COLLATE pg_catalog."default" NOT NULL,
    isadmin boolean NOT NULL,
    CONSTRAINT users_pkey PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS public.incidents
(
    id SERIAL,
    createdon timestamp without time zone,
    title text COLLATE pg_catalog."default" NOT NULL,
    comment text COLLATE pg_catalog."default" NOT NULL,
    type character varying(25) COLLATE pg_catalog."default",
    createdby integer,
    latitude REAL,
    longitude REAL,
    status character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT incidents_pkey PRIMARY KEY (id),
    CONSTRAINT incidents_createdby_fkey FOREIGN KEY (createdby)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

INSERT INTO users  ( username, email, password, firstname,lastname, othernames,
 phonenumber, dteregistered, isadmin)
SELECT 'bison', 'bisonlou@gmail.com',
'sha256$a8HCuuXl$7f933b02fa157f5c3faa17950bac0aced460cab2700ca7017c56d987b1ba918c',
'Innocent', 'Lou', '','07553669897','2019-01-01', True
WHERE NOT EXISTS ( SELECT id FROM users WHERE email = 'bisonlou@gmail.com');


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
);



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
);