
CREATE SCHEMA IF NOT EXISTS reportify ;
SET SCHEMA 'reportify' ;



CREATE TABLE IF NOT EXISTS reportify.local (
  id SERIAL,
  nome TEXT NOT NULL,
  PRIMARY KEY (id))
;



CREATE TABLE IF NOT EXISTS reportify.setor (
  id SERIAL,
  nome TEXT NOT NULL,
  desc_responsabilidades TEXT NOT NULL,
  status VARCHAR(45) NOT NULL,
  PRIMARY KEY (id))
;

CREATE TABLE problema (
	id SERIAL,
	nome TEXT NOT NULL,
	id_setor INT NOT NULL,
	PRIMARY KEY (id),
	CONSTRAINT fk_id_setor
		FOREIGN KEY (id_setor)
		REFERENCES setor (id)
);



CREATE TABLE IF NOT EXISTS reportify.ocorrencia (
  id SERIAL,
  email_cidadao TEXT NULL DEFAULT NULL,
  descricao TEXT NOT NULL,
  status VARCHAR(45) NOT NULL,
  data_criacao TIMESTAMP(0) NOT NULL DEFAULT timezone('America/Sao_Paulo'::text, CURRENT_TIMESTAMP),
  data_resolucao TIMESTAMP(0) NULL DEFAULT NULL,
  id_local INT NOT NULL,
  id_problema INT NOT NULL,
  id_setor INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_ocorrencia_local1
    FOREIGN KEY (id_local)
    REFERENCES reportify.local (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_ocorrencia_setor1
    FOREIGN KEY (id_setor)
    REFERENCES reportify.setor (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_ocorrencia_id_problema
  	FOREIGN KEY (id_problema)
	REFERENCES problema (id)
	ON DELETE NO ACTION
	ON UPDATE CASCADE

    );




CREATE TABLE IF NOT EXISTS reportify.usuario(
	id SERIAL,
	matricula SERIAL,
	nome TEXT NOT NULL,
	sobrenome TEXT NOT NULL,
	email TEXT NOT NULL,
	status VARCHAR(45) NOT NULL,
	PRIMARY KEY (id)

);


--tabela que mapeia o ID dentro da BD de autênticação com o ID do usuário
CREATE TABLE IF NOT EXISTS reportify.usuario_auth_map(
	id_auth INT NOT NULL,
	id_usuario INT NOT NULL,
	PRIMARY KEY (id_auth, id_usuario),
	CONSTRAINT fk_id_usuario_id
	FOREIGN KEY (id_usuario)
		REFERENCES reportify.usuario (id)
);


CREATE TABLE IF NOT EXISTS reportify.adm_sistema(
	id INT NOT NULL,
	CONSTRAINT fk_adm_sistema_id_usuario
		FOREIGN KEY (id)
		REFERENCES reportify.usuario (id)
		ON DELETE CASCADE
		ON UPDATE CASCADE

);


CREATE TABLE IF NOT EXISTS reportify.gestor_ocorrencia (
  id INT NOT NULL,
  setor_atuacao INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_gestor_ocorrencia_setor1
    FOREIGN KEY (setor_atuacao)
    REFERENCES reportify.setor (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_gestor_ocorrencia_id
    FOREIGN KEY (id)
    REFERENCES reportify.usuario (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);



SET search_path TO reportify;


--Populando a tabela "local":
INSERT INTO reportify.local (nome) VALUES ('Berçario');
INSERT INTO reportify.local (nome) VALUES ('Sala de raio-X');
INSERT INTO reportify.local (nome) VALUES ('Sala de medicamentos');
INSERT INTO reportify.local (nome) VALUES ('Sala de triagem');

--Populando a tabela "setor":
INSERT INTO reportify.setor (nome, desc_responsabilidades, status) VALUES ('Limpeza', 'Limpeza de salas', 'Ativo');
INSERT INTO reportify.setor (nome, desc_responsabilidades, status) VALUES ('Manutenção', 'Manutenção e reparo de elétrica e hidraúlica', 'Ativo');
INSERT INTO reportify.setor (nome, desc_responsabilidades, status) VALUES ('Reposição', 'Reposição de insumos hospitalares', 'Ativo');

INSERT INTO reportify.problema (nome, id_setor) VALUES ('Limpeza', 1);
INSERT INTO reportify.problema (nome, id_setor) VALUES ('Manutenção', 2);
INSERT INTO reportify.problema (nome, id_setor) VALUES ('Falta de materiáis', 3);



-- Povoamente tabela "reportify.usuario"
INSERT INTO reportify.usuario (matricula, nome, sobrenome, email, status) values (000001, 'ADM', 'ADM', 'adm@adm.com', 'Ativo');


INSERT INTO reportify.adm_sistema (id) VALUES (1);

INSERT INTO reportify.usuario_auth_map (id_auth, id_usuario) VALUES (1,1);

-- Povoamento da tabela "reportify.gestor_ocorrencia"
INSERT INTO reportify.gestor_ocorrencia (id, setor_atuacao) values (2, 1);
INSERT INTO reportify.gestor_ocorrencia (id, setor_atuacao) values (3, 2);
INSERT INTO reportify.gestor_ocorrencia (id, setor_atuacao) values (4, 3);

