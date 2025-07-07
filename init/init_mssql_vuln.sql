USE master;
GO

-- Criação do banco (caso não exista)
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'vuln_db')
BEGIN
    CREATE DATABASE vuln_db;
END
GO

USE vuln_db;
GO

-- Criação dos schemas
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'level1')
    EXEC('CREATE SCHEMA level1');
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'level2')
    EXEC('CREATE SCHEMA level2');
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'level3')
    EXEC('CREATE SCHEMA level3');
GO

-- Criação dos logins e usuários
IF NOT EXISTS (SELECT * FROM sys.sql_logins WHERE name = 'level1_user')
    CREATE LOGIN level1_user WITH PASSWORD = 'senha1';
IF NOT EXISTS (SELECT * FROM sys.sql_logins WHERE name = 'level2_user')
    CREATE LOGIN level2_user WITH PASSWORD = 'senha2';
IF NOT EXISTS (SELECT * FROM sys.sql_logins WHERE name = 'level3_user')
    CREATE LOGIN level3_user WITH PASSWORD = 'senha3';
GO

-- Criar usuários no banco
CREATE USER level1_user FOR LOGIN level1_user;
CREATE USER level2_user FOR LOGIN level2_user;
CREATE USER level3_user FOR LOGIN level3_user;
GO

-- Criação das tabelas
IF OBJECT_ID('level1.missions', 'U') IS NULL
BEGIN
    CREATE TABLE level1.missions (
        id INT IDENTITY(1,1) PRIMARY KEY,
        mission_name VARCHAR(255),
        status VARCHAR(100)
    );
END

IF OBJECT_ID('level2.missions', 'U') IS NULL
BEGIN
    CREATE TABLE level2.missions (
        id INT IDENTITY(1,1) PRIMARY KEY,
        mission_name VARCHAR(255),
        status VARCHAR(100)
    );
END

IF OBJECT_ID('level3.missions', 'U') IS NULL
BEGIN
    CREATE TABLE level3.missions (
        id INT IDENTITY(1,1) PRIMARY KEY,
        mission_name VARCHAR(255),
        status VARCHAR(100)
    );
END
GO

-- Permissões
GRANT SELECT, INSERT, UPDATE, DELETE ON SCHEMA::level1 TO level1_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON SCHEMA::level2 TO level2_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON SCHEMA::level3 TO level3_user;
GO

-- Inserção de dados
INSERT INTO level1.missions (mission_name, status)
VALUES ('Enumeração inicial', 'pendente'),
       ('Fuzzing de inputs', 'em andamento');

INSERT INTO level2.missions (mission_name, status)
VALUES ('Bypass de autenticação JWT', 'ativa'),
       ('Exploração de LFI', 'falhou');

INSERT INTO level3.missions (mission_name, status)
VALUES ('Execução remota de código', 'ativa'),
       ('Persistência via Agent Job', 'completa');
GO
