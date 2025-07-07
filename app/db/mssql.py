import pyodbc

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=sqlserver;"
    "DATABASE=master;"
    "UID=sa;"
    "PWD=YourStrong!Passw0rd"
)

def get_connection():
    return pyodbc.connect(conn_str)


def init_db_mssql():
    
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Criação dos schemas
        for schema in ['level1', 'level2', 'level3']:
            cursor.execute(f"""
                IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = '{schema}')
                    EXEC('CREATE SCHEMA {schema}')
            """)

        # Criação dos logins e usuários (com checagem)
        for user, password in [('level1_user', 'SenhaForte1!'), ('level2_user', 'SenhaForte2!'), ('level3_user', 'SenhaForte3!')]:
            cursor.execute(f"""
                IF NOT EXISTS (SELECT * FROM sys.sql_logins WHERE name = '{user}')
                    CREATE LOGIN {user} WITH PASSWORD = '{password}';
            """)
            cursor.execute(f"""
                IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = '{user}')
                    CREATE USER {user} FOR LOGIN {user};
            """)

        # Criação das tabelas em cada schema
        for schema in ['level1', 'level2', 'level3']:
            cursor.execute(f"""
                IF OBJECT_ID('{schema}.missions', 'U') IS NULL
                BEGIN
                    CREATE TABLE {schema}.missions (
                        id INT IDENTITY(1,1) PRIMARY KEY,
                        mission_name VARCHAR(255),
                        status VARCHAR(100)
                    )
                END
            """)

        # Concessão de permissões
        for schema, user in [('level1', 'level1_user'), ('level2', 'level2_user'), ('level3', 'level3_user')]:
            cursor.execute(f"""
                GRANT SELECT, INSERT, UPDATE, DELETE ON SCHEMA::{schema} TO {user};
            """)

        # Inserção de dados iniciais (opcional)
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM level1.missions)
            BEGIN
                INSERT INTO level1.missions (mission_name, status)
                VALUES ('Enumeração inicial', 'pendente'),
                       ('Fuzzing de inputs', 'em andamento')
            END
        """)

        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM level2.missions)
            BEGIN
                INSERT INTO level2.missions (mission_name, status)
                VALUES ('Bypass de autenticação JWT', 'ativa'),
                       ('Exploração de LFI', 'falhou')
            END
        """)

        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM level3.missions)
            BEGIN
                INSERT INTO level3.missions (mission_name, status)
                VALUES ('Execução remota de código', 'ativa'),
                       ('Persistência via Agent Job', 'completa')
            END
        """)

        conn.commit()
        print("[OK] Banco de dados **master (SQL Server)** inicializado com sucesso!")

    except Exception as e:
        print("[ERRO] Falha ao criar estrutura no SQL Server:", e)

    finally:
        if conn:
            conn.close()
