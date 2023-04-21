
CREATE SCHEMA IF NOT EXISTS reportify ;
SET SCHEMA 'reportify' ;



CREATE TABLE IF NOT EXISTS reportify.local (
  id SERIAL,
  nome VARCHAR(45) NOT NULL,
  PRIMARY KEY (id))
;



CREATE TABLE IF NOT EXISTS reportify.setor (
  id SERIAL,
  nome VARCHAR(45) NOT NULL,
  desc_responsabilidades TEXT NOT NULL,
  status VARCHAR(45) NOT NULL,
  PRIMARY KEY (id))
;



CREATE TABLE IF NOT EXISTS reportify.ocorrencia (
  id SERIAL,
  email_cidadao VARCHAR(45) NULL DEFAULT NULL,
  nome_cidadao VARCHAR(45) NULL DEFAULT NULL,
  descricao VARCHAR(45) NOT NULL,
  status VARCHAR(45) NOT NULL,
  data_criacao TIMESTAMP(0) NOT NULL,
  data_resolucao TIMESTAMP(0) NULL DEFAULT NULL,
  id_local INT NOT NULL,
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
    ON UPDATE NO ACTION);


-- SQLINES DEMO *** ------------------------------------
-- SQLINES DEMO *** cais_atuacao`
-- SQLINES DEMO *** ------------------------------------
-- SQLINES LICENSE FOR EVALUATION USE ONLY

CREATE TABLE IF NOT EXISTS reportify.locais_atuacao (
  id SERIAL,
  setor_id INT NOT NULL,
  local_idlocal INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_locais_atuacao_setor
    FOREIGN KEY (setor_id)
    REFERENCES reportify.setor (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_locais_atuacao_local1
    FOREIGN KEY (local_idlocal)
    REFERENCES reportify.local (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE);


-- SQLINES DEMO *** ------------------------------------
-- SQLINES DEMO *** stor_ocorrencia`
-- SQLINES DEMO *** ------------------------------------
-- SQLINES LICENSE FOR EVALUATION USE ONLY


CREATE TABLE IF NOT EXISTS reportify.usuario(
	id SERIAL,
	matricula SERIAL,
	nome VARCHAR(45) NOT NULL,
	sobrenome VARCHAR(90) NOT NULL,
	email VARCHAR(45) NOT NULL,
	status VARCHAR(45) NOT NULL,
	PRIMARY KEY (id),

);


--tabela que mapeia o ID dentro da BD de autênticação com o ID do usuário
CREATE TABLE IF NOT EXISTS reportify.usuario_auth_map(
	id_auth INT NOT NULL,
	id_usuario INT NOT NULL,
	PRIMARY KEY (id_auth, id_usuario),
	CONSTRAINT fk_id_usuario_id
	FOREIGN KEY (id_usuario)
		REFERENCES reportify.usuario (id),
);


CREATE TABLE IF NOT EXISTS reportify.adm_sistema(
	id INT NOT NULL,
	CONSTRAINT fk_adm_sistema_id_usuario
		FOREIGN KEY (id)
		REFERENCES reportify.usuario (id)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	
);


CREATE TABLE IF NOT EXISTS reportify.gestor_ocorrencia (
  id INT NOT NULL,
  setor_atuacao INT NOT NULL,
  PRIMARY KEY (matricula),
  CONSTRAINT fk_gestor_ocorrencia_setor1
    FOREIGN KEY (setor_atuacao)
    REFERENCES reportify.setor (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_gestor_ocorrencia_id
    FOREIGN KEY (id)
    REFERENCES reportify.usuario (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
);


-- SQLINES DEMO *** ------------------------------------
-- SQLINES DEMO *** reportify`
-- SQLINES DEMO *** ------------------------------------
-- SQLINES LICENSE FOR EVALUATION USE ONLY
CREATE TABLE IF NOT EXISTS reportify.solucionado (
  id_ocorrencia INT NOT NULL,
  id_gestor INT NOT NULL,
  ultima_alteracao TIMESTAMP(0) NOT NULL,
  PRIMARY KEY (id_ocorrencia, id_gestor),
  CONSTRAINT fk_ocorrencia_has_gestor_ocorrencia_ocorrencia1
    FOREIGN KEY (id_ocorrencia)
    REFERENCES reportify.ocorrencia (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_ocorrencia_has_gestor_ocorrencia_gestor_ocorrencia1
    FOREIGN KEY (id_gestor)
    REFERENCES reportify.gestor_ocorrencia (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
;


--Populando a tabela "local":
INSERT INTO reportify.local (nome) VALUES ('Berçario');
INSERT INTO reportify.local (nome) VALUES ('Sala de raio-X');
INSERT INTO reportify.local (nome) VALUES ('Sala de medicamentos');
INSERT INTO reportify.local (nome) VALUES ('Sala de triagem');

--Populando a tabela "setor":
INSERT INTO reportify.setor (nome, desc_responsabilidades, status) VALUES ('Limpeza', 'Limpeza de salas', 'Ativo');
INSERT INTO reportify.setor (nome, desc_responsabilidades, status) VALUES ('Manutenção', 'Manutenção e reparo de elétrica e hidraúlica', 'Ativo');
INSERT INTO reportify.setor (nome, desc_responsabilidades, status) VALUES ('Reposição', 'Reposição de insumos hospitalares', 'Ativo');

--Populando a tabela "ocorrencia":
INSERT INTO reportify.ocorrencia (email_cidadao, nome_cidadao, descricao, status, data_criacao, data_resolucao, id_local, id_setor) VALUES ('jose@gmail.com', 'José', 'Sala de raio-x suja', 'Aberto', '2022-02-01 10:00:00', NULL, 2, 1);
INSERT INTO reportify.ocorrencia (email_cidadao, nome_cidadao, descricao, status, data_criacao, data_resolucao, id_local, id_setor) VALUES ('ana@hotmail.com', 'Ana', 'Lâmpada queimada', 'Aberto', '2022-03-15 14:30:00', NULL, 1, 2);
INSERT INTO reportify.ocorrencia (email_cidadao, nome_cidadao, descricao, status, data_criacao, data_resolucao, id_local, id_setor) VALUES ('maria@gmail.com', 'Maria', 'Sem papel na sala de triagem', 'Aberto', '2022-03-20 11:00:00', NULL, 4, 3);

--Populando a tabela "locais_atuacao":
INSERT INTO reportify.locais_atuacao (setor_id, local_idlocal) VALUES (1, 1);
INSERT INTO reportify.locais_atuacao (setor_id, local_idlocal) VALUES (1, 2);
INSERT INTO reportify.locais_atuacao (setor_id, local_idlocal) VALUES (1, 3);
INSERT INTO reportify.locais_atuacao (setor_id, local_idlocal) VALUES (2, 2);
INSERT INTO reportify.locais_atuacao (setor_id, local_idlocal) VALUES (2, 1);
INSERT INTO reportify.locais_atuacao (setor_id, local_idlocal) VALUES (2, 3);
INSERT INTO reportify.locais_atuacao (setor_id, local_idlocal) VALUES (3, 1);
INSERT INTO reportify.locais_atuacao (setor_id, local_idlocal) VALUES (3, 2);
INSERT INTO reportify.locais_atuacao (setor_id, local_idlocal) VALUES (3, 3);
INSERT INTO reportify.locais_atuacao (setor_id, local_idlocal) VALUES (3, 4);


-- Povoamente tabela "reportify.usuario"
INSERT INTO reportify.usuario (matricula, nome, sobrenome, email, status) values (000001, 'João', 'Silva', 'joao.silva@exemplo.com', 'Ativo');
INSERT INTO reportify.usuario (matricula, nome, sobrenome, email, status) values (000002, 'Maria', 'Santos', 'maria.santos@exemplo.com', 'Ativo');
INSERT INTO reportify.usuario (matricula, nome, sobrenome, email, status) values (000003, 'Pedro', 'Oliveira', 'pedro.oliveira@exemplo.com', 'Inativo');
INSERT INTO reportify.usuario (matricula, nome, sobrenome, email, status) values (000004, 'Ana', 'Ferreira', 'ana.ferreira@exemplo.com', 'Ativo');

-- Povoamento da tabela "reportify.gestor_ocorrencia"
INSERT INTO reportify.gestor_ocorrencia (matricula, setor_atuacao) values (1, 1);
INSERT INTO reportify.gestor_ocorrencia (matricula, setor_atuacao) values (2, 2);
INSERT INTO reportify.gestor_ocorrencia (matricula, setor_atuacao) values (3, 3);
INSERT INTO reportify.gestor_ocorrencia (matricula, setor_atuacao) values (4, 1);

