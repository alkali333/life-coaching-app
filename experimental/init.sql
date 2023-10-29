-- Table: public.diary

-- DROP TABLE IF EXISTS public.diary;

CREATE TABLE IF NOT EXISTS public.diary
(
    id integer NOT NULL DEFAULT nextval('diary_id_seq'::regclass),
    entry character varying COLLATE pg_catalog."default",
    summary character varying COLLATE pg_catalog."default",
    date date,
    user_id integer,
    CONSTRAINT diary_pkey PRIMARY KEY (id),
    CONSTRAINT diary_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.diary
    OWNER to postgres;
-- Index: ix_diary_id

-- DROP INDEX IF EXISTS public.ix_diary_id;

CREATE INDEX IF NOT EXISTS ix_diary_id
    ON public.diary USING btree
    (id ASC NULLS LAST)
    TABLESPACE pg_default;

-- Table: public.mind_state

-- DROP TABLE IF EXISTS public.mind_state;

CREATE TABLE IF NOT EXISTS public.mind_state
(
    id integer NOT NULL DEFAULT nextval('mind_state_id_seq'::regclass),
    hopes_and_dreams character varying COLLATE pg_catalog."default",
    skills_and_achievements character varying COLLATE pg_catalog."default",
    obstacles_and_challenges character varying COLLATE pg_catalog."default",
    grateful_for character varying COLLATE pg_catalog."default",
    current_tasks character varying COLLATE pg_catalog."default",
    user_id integer,
    "timestamp" timestamp without time zone,
    CONSTRAINT mind_state_pkey PRIMARY KEY (id),
    CONSTRAINT mind_state_user_id_key UNIQUE (user_id),
    CONSTRAINT mind_state_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.mind_state
    OWNER to postgres;
-- Index: ix_mind_state_id

-- DROP INDEX IF EXISTS public.ix_mind_state_id;

CREATE INDEX IF NOT EXISTS ix_mind_state_id
    ON public.mind_state USING btree
    (id ASC NULLS LAST)
    TABLESPACE pg_default;

-- Table: public.users

-- DROP TABLE IF EXISTS public.users;

CREATE TABLE IF NOT EXISTS public.users
(
    id integer NOT NULL DEFAULT nextval('users_id_seq'::regclass),
    name character varying COLLATE pg_catalog."default",
    email character varying COLLATE pg_catalog."default",
    password character varying(256) COLLATE pg_catalog."default",
    is_new integer DEFAULT 1,
    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT users_email_key UNIQUE (email)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.users
    OWNER to postgres;
-- Index: ix_users_id

-- DROP INDEX IF EXISTS public.ix_users_id;

CREATE INDEX IF NOT EXISTS ix_users_id
    ON public.users USING btree
    (id ASC NULLS LAST)
    TABLESPACE pg_default;


