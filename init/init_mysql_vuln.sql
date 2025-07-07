-- Garantir uso do banco
USE vuln_db;

-- Criar usuários se não existirem
CREATE USER IF NOT EXISTS 'level1_user'@'%' IDENTIFIED BY 'senha1';
CREATE USER IF NOT EXISTS 'level2_user'@'%' IDENTIFIED BY 'senha2';
CREATE USER IF NOT EXISTS 'level3_user'@'%' IDENTIFIED BY 'senha3';

-- Tabelas para simular os 3 níveis
CREATE TABLE IF NOT EXISTS level1_missions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mission_name VARCHAR(255),
    status VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS level2_missions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mission_name VARCHAR(255),
    status VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS level3_missions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mission_name VARCHAR(255),
    status VARCHAR(100)
);

-- Conceder permissões específicas para cada usuário
GRANT SELECT, INSERT, UPDATE, DELETE ON vuln_db.level1_missions TO 'level1_user'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON vuln_db.level2_missions TO 'level2_user'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON vuln_db.level3_missions TO 'level3_user'@'%';

-- Dados de exemplo
INSERT INTO level1_missions (mission_name, status) VALUES
('Reconhecimento inicial', 'pendente'),
('Escaneamento de portas', 'em andamento');

INSERT INTO level2_missions (mission_name, status) VALUES
('Injeção SQL básica', 'ativa'),
('Quebra de autenticação', 'falha');

INSERT INTO level3_missions (mission_name, status) VALUES
('Exfiltração via DNS', 'completa'),
('Persistência via backdoor', 'ativa');

-- Aplicar permissões
FLUSH PRIVILEGES;
