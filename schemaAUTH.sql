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


ALTER DATABASE auth_proj_es SET search_path TO auth;


INSERT INTO users (email, password, cargo) VALUES ('adm@adm.com', '86f65e28a754e1a71b2df9403615a6c436c32c42a75a10d02813961b86f1e428', 'adm');
