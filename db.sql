-- SQLINES DEMO *** rated by MySQL Workbench
-- SQLINES DEMO *** 0:09:52
-- SQLINES DEMO ***    Version: 1.0
-- SQLINES DEMO *** orward Engineering

/* SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0; */
/* SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0; */
/* SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'; */

-- SQLINES DEMO *** ------------------------------------
-- Schema solve
-- SQLINES DEMO *** ------------------------------------

-- SQLINES DEMO *** ------------------------------------
-- Schema solve
-- SQLINES DEMO *** ------------------------------------
CREATE SCHEMA IF NOT EXISTS solve ;
SET SCHEMA 'solve' ;

-- SQLINES DEMO *** ------------------------------------
-- SQLINES DEMO *** cal`
-- SQLINES DEMO *** ------------------------------------
-- SQLINES LICENSE FOR EVALUATION USE ONLY

CREATE TABLE IF NOT EXISTS solve.local (
  id SERIAL,
  nome VARCHAR(45) NOT NULL,
  PRIMARY KEY (id))
;


-- SQLINES DEMO *** ------------------------------------
-- SQLINES DEMO *** tor`
-- SQLINES DEMO *** ------------------------------------
-- SQLINES LICENSE FOR EVALUATION USE ONLY

CREATE TABLE IF NOT EXISTS solve.setor (
  id SERIAL,
  nome VARCHAR(45) NOT NULL,
  desc_responsabilidades TEXT NOT NULL,
  status VARCHAR(45) NOT NULL,
  PRIMARY KEY (id))
;


-- SQLINES DEMO *** ------------------------------------
-- SQLINES DEMO *** orrencia`
-- SQLINES DEMO *** ------------------------------------
-- SQLINES LICENSE FOR EVALUATION USE ONLY

CREATE TABLE IF NOT EXISTS solve.ocorrencia (
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
    REFERENCES solve.local (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_ocorrencia_setor1
    FOREIGN KEY (id_setor)
    REFERENCES solve.setor (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- SQLINES DEMO *** ------------------------------------
-- SQLINES DEMO *** cais_atuacao`
-- SQLINES DEMO *** ------------------------------------
-- SQLINES LICENSE FOR EVALUATION USE ONLY

CREATE TABLE IF NOT EXISTS solve.locais_atuacao (
  id SERIAL,
  setor_id INT NOT NULL,
  local_idlocal INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_locais_atuacao_setor
    FOREIGN KEY (setor_id)
    REFERENCES solve.setor (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_locais_atuacao_local1
    FOREIGN KEY (local_idlocal)
    REFERENCES solve.local (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE);


-- SQLINES DEMO *** ------------------------------------
-- SQLINES DEMO *** stor_ocorrencia`
-- SQLINES DEMO *** ------------------------------------
-- SQLINES LICENSE FOR EVALUATION USE ONLY

CREATE TABLE IF NOT EXISTS solve.gestor_ocorrencia (
  id SERIAL,
  matricula INT NOT NULL,
  nome VARCHAR(45) NOT NULL,
  sobrenome VARCHAR(45) NOT NULL,
  email VARCHAR(45) NOT NULL,
  status VARCHAR(45) NOT NULL,
  setor_atuacao INT NOT NULL,
  PRIMARY KEY (matricula),
  CONSTRAINT fk_gestor_ocorrencia_setor1
    FOREIGN KEY (setor_atuacao)
    REFERENCES solve.setor (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
;


-- SQLINES DEMO *** ------------------------------------
-- SQLINES DEMO *** solve`
-- SQLINES DEMO *** ------------------------------------
-- SQLINES LICENSE FOR EVALUATION USE ONLY
CREATE TABLE IF NOT EXISTS solve.resolve (
  id_ocorrencia INT NOT NULL,
  matricula_gestor INT NOT NULL,
  ultima_alteracao TIMESTAMP(0) NOT NULL,
  PRIMARY KEY (id_ocorrencia, matricula_gestor),
  CONSTRAINT fk_ocorrencia_has_gestor_ocorrencia_ocorrencia1
    FOREIGN KEY (id_ocorrencia)
    REFERENCES solve.ocorrencia (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_ocorrencia_has_gestor_ocorrencia_gestor_ocorrencia1
    FOREIGN KEY (matricula_gestor)
    REFERENCES solve.gestor_ocorrencia (matricula)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
;


/* SET SQL_MODE=@OLD_SQL_MODE; */
/* SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS; */
/* SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS; */

--Populando a tabela "local":
INSERT INTO solve.local (nome) VALUES ('Berçario');
INSERT INTO solve.local (nome) VALUES ('Sala de raio-X');
INSERT INTO solve.local (nome) VALUES ('Sala de medicamentos');
INSERT INTO solve.local (nome) VALUES ('Sala de triagem');

--Populando a tabela "setor":
INSERT INTO solve.setor (nome, desc_responsabilidades, status) VALUES ('Limpeza', 'Limpeza de salas', 'Ativo');
INSERT INTO solve.setor (nome, desc_responsabilidades, status) VALUES ('Manutenção', 'Manutenção e reparo de elétrica e hidraúlica', 'Ativo');
INSERT INTO solve.setor (nome, desc_responsabilidades, status) VALUES ('Reposição', 'Reposição de insumos hospitalares', 'Ativo');

--Populando a tabela "ocorrencia":
INSERT INTO solve.ocorrencia (email_cidadao, nome_cidadao, descricao, status, data_criacao, data_resolucao, id_local, id_setor) VALUES ('jose@gmail.com', 'José', 'Sala de raio-x suja', 'Aberto', '2022-02-01 10:00:00', NULL, 2, 1);
INSERT INTO solve.ocorrencia (email_cidadao, nome_cidadao, descricao, status, data_criacao, data_resolucao, id_local, id_setor) VALUES ('ana@hotmail.com', 'Ana', 'Lâmpada queimada', 'Aberto', '2022-03-15 14:30:00', NULL, 1, 2);
INSERT INTO solve.ocorrencia (email_cidadao, nome_cidadao, descricao, status, data_criacao, data_resolucao, id_local, id_setor) VALUES ('maria@gmail.com', 'Maria', 'Sem papel na sala de triagem', 'Aberto', '2022-03-20 11:00:00', NULL, 4, 3);

--Populando a tabela "locais_atuacao":
INSERT INTO solve.locais_atuacao (setor_id, local_idlocal) VALUES (1, 1);
INSERT INTO solve.locais_atuacao (setor_id, local_idlocal) VALUES (1, 2);
INSERT INTO solve.locais_atuacao (setor_id, local_idlocal) VALUES (1, 3);
INSERT INTO solve.locais_atuacao (setor_id, local_idlocal) VALUES (2, 2);
INSERT INTO solve.locais_atuacao (setor_id, local_idlocal) VALUES (2, 1);
INSERT INTO solve.locais_atuacao (setor_id, local_idlocal) VALUES (2, 3);
INSERT INTO solve.locais_atuacao (setor_id, local_idlocal) VALUES (3, 1);
INSERT INTO solve.locais_atuacao (setor_id, local_idlocal) VALUES (3, 2);
INSERT INTO solve.locais_atuacao (setor_id, local_idlocal) VALUES (3, 3);
INSERT INTO solve.locais_atuacao (setor_id, local_idlocal) VALUES (3, 4);



--Populando a tabela "gestor_ocorrêcnia"
INSERT INTO solve.gestor_ocorrencia (matricula, nome, sobrenome, email, status, setor_atuacao) values (000001, 'Cleiton', 'Do Santos Silva', 'asdkasdjnasdk@gmail.com', 'Ativo', 1);
INSERT INTO solve.gestor_ocorrencia (matricula, nome, sobrenome, email, status, setor_atuacao) values (000002, 'Pedro', 'Do Santos Silva', 'asdkasdjnasdk@gmail.com', 'Ativo', 2);
INSERT INTO solve.gestor_ocorrencia (matricula, nome, sobrenome, email, status, setor_atuacao) values (000003, 'Maria', 'Do Santos Silva', 'asdkasdjnasdk@gmail.com', 'Ativo', 3);
INSERT INTO solve.gestor_ocorrencia (matricula, nome, sobrenome, email, status, setor_atuacao) values (000004, 'Ana', 'Do Santos Silva', 'asdkasdjnasdk@gmail.com', 'Ativo', 1);


