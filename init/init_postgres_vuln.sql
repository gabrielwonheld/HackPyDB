-- Criação dos schemas
CREATE SCHEMA IF NOT EXISTS level1;
CREATE SCHEMA IF NOT EXISTS level2;
CREATE SCHEMA IF NOT EXISTS level3;

-- Criação dos usuários (com verificação se já existem)
DO
$$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'level1_user') THEN
        CREATE USER level1_user WITH PASSWORD 'senha1';
    END IF;
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'level2_user') THEN
        CREATE USER level2_user WITH PASSWORD 'senha2';
    END IF;
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'level3_user') THEN
        CREATE USER level3_user WITH PASSWORD 'senha3';
    END IF;
END
$$;

-- Permissões de uso dos schemas
GRANT USAGE ON SCHEMA level1 TO level1_user;
GRANT USAGE ON SCHEMA level2 TO level2_user;
GRANT USAGE ON SCHEMA level3 TO level3_user;

-- Criação das tabelas
CREATE TABLE IF NOT EXISTS level1.missions (
    id SERIAL PRIMARY KEY,
    mission_name VARCHAR(255),
    status VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS level2.missions (
    id SERIAL PRIMARY KEY,
    mission_name VARCHAR(255),
    status VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS level3.missions (
    id SERIAL PRIMARY KEY,
    mission_name VARCHAR(255),
    status VARCHAR(100)
);

-- Permissões nas tabelas
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA level1 TO level1_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA level2 TO level2_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA level3 TO level3_user;

-- Permissões nas sequences (para evitar o erro "permission denied for sequence")
GRANT USAGE, SELECT, UPDATE ON SEQUENCE level1.missions_id_seq TO level1_user;
GRANT USAGE, SELECT, UPDATE ON SEQUENCE level2.missions_id_seq TO level2_user;
GRANT USAGE, SELECT, UPDATE ON SEQUENCE level3.missions_id_seq TO level3_user;

-- Inserção de dados de exemplo
INSERT INTO level1.missions (mission_name, status)
VALUES 
    ('Missão de coleta de dados', 'pendente'),
    ('Mapeamento de rede', 'em andamento');

INSERT INTO level2.missions (mission_name, status)
VALUES 
    ('Escalada de privilégios', 'ativa'),
    ('Bypass de autenticação', 'falha');

INSERT INTO level3.missions (mission_name, status)
VALUES 
    ('Exfiltração de dados sensíveis', 'completa'),
    ('Ataque persistente', 'em progresso');
