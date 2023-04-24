CREATE SCHEMA auth;

CREATE TABLE IF NOT EXISTS auth.users
(
    id integer NOT NULL DEFAULT nextval('users_id_seq'::regclass),
    email text COLLATE pg_catalog."default" NOT NULL,
    password text COLLATE pg_catalog."default" NOT NULL,
    criado_em timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    cargo text COLLATE pg_catalog."default" DEFAULT 'gestor'::text,
    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT users_email_key UNIQUE (email)
)


CREATE TABLE auth.tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES auth.users(id),
    access_token TEXT NOT NULL,
    refresh_token TEXT NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

ALTER DATABASE auth_proj_es SET search_path TO auth