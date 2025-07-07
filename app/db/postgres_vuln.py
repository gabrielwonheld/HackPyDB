import psycopg2
import os

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'postgres_vuln'),  # O nome correto do serviço no docker-compose
        database=os.getenv('DB_NAME', 'todo_db'),  # O nome do banco de dados
        user=os.getenv('DB_USER', 'postgres'),  # O usuário do banco de dados
        password=os.getenv('DB_PASS', 'postgres'),  # A senha do banco de dados
        port=int(os.getenv('DB_PORT', 5433))
    )

def get_connection_level1():
    return psycopg2.connect(
        host='postgres_vuln',
        database='todo_db',
        user='level1_user',
        password='senha1',
        port=int(os.getenv('DB_PORT', 5433))    
    )


def init_db_postgres_vuln():
    try:    
        conn = get_db_connection()
        cur = conn.cursor()

        # Criação dos schemas
        cur.execute('''
            CREATE SCHEMA IF NOT EXISTS level1;
            CREATE SCHEMA IF NOT EXISTS level2;
            CREATE SCHEMA IF NOT EXISTS level3;
        ''')

        # Função auxiliar para criar usuários
        def create_user_if_not_exists(username, password):
            cur.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (username,))
            if not cur.fetchone():
                print(f"[INFO] Criando usuário {username}")
                cur.execute(f"CREATE USER {username} WITH PASSWORD %s", (password,))

        create_user_if_not_exists("level1_user", "senha1")
        create_user_if_not_exists("level2_user", "senha2")
        create_user_if_not_exists("level3_user", "senha3")

        # Conceder uso dos schemas
        cur.execute('''
            GRANT USAGE ON SCHEMA level1 TO level1_user;
            GRANT USAGE ON SCHEMA level2 TO level2_user;
            GRANT USAGE ON SCHEMA level3 TO level3_user;
        ''')

        # Criar tabelas
        cur.execute('''
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
        ''')

        # Permissões
        cur.execute('''
            GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA level1 TO level1_user;
            GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA level2 TO level2_user;
            GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA level3 TO level3_user;
        ''')

        conn.commit()
        cur.close()
        conn.close()
        print("[OK] Banco de dados **postgres_vuln** inicializado com sucesso!")

    except Exception as e:
        print("[ERRO]", e)



#def init_db_postgres_vuln():
#
#    try:    
#        conn = get_db_connection()
#        cur = conn.cursor()
#        # Criação dos schemas
#        cur.execute('''
#            CREATE SCHEMA IF NOT EXISTS level1;
#            CREATE SCHEMA IF NOT EXISTS level2;
#            CREATE SCHEMA IF NOT EXISTS level3;
#        ''')
#        # Criação dos usuários, com bloco anônimo para evitar erros caso existam
#        cur.execute('''
#        DO
#        $do$
#        BEGIN
#            IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'level1_user') THEN
#                CREATE USER level1_user WITH PASSWORD 'senha1';
#            END IF;
#            IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'level2_user') THEN
#                CREATE USER level2_user WITH PASSWORD 'senha2';
#            END IF;
#            IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'level3_user') THEN
#                CREATE USER level3_user WITH PASSWORD 'senha3';
#            END IF;
#        END
#        $do$;
#        ''')
#        # Conceder uso dos schemas para os usuários
#        cur.execute('''
#            GRANT USAGE ON SCHEMA level1 TO level1_user;
#            GRANT USAGE ON SCHEMA level2 TO level2_user;
#            GRANT USAGE ON SCHEMA level3 TO level3_user;
#        ''')
#        # Criar tabelas dentro dos schemas (se não existirem)
#        cur.execute('''
#            CREATE TABLE IF NOT EXISTS level1.missions (
#                id SERIAL PRIMARY KEY,
#                mission_name VARCHAR(255),
#                status VARCHAR(100)
#            );
#            CREATE TABLE IF NOT EXISTS level2.missions (
#                id SERIAL PRIMARY KEY,
#                mission_name VARCHAR(255),
#                status VARCHAR(100)
#            );
#            CREATE TABLE IF NOT EXISTS level3.missions (
#                id SERIAL PRIMARY KEY,
#                mission_name VARCHAR(255),
#                status VARCHAR(100)
#            );
#        ''')
#        # Dar permissões para as tabelas já criadas
#        cur.execute('''
#            GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA level1 TO level1_user;
#            GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA level2 TO level2_user;
#            GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA level3 TO level3_user;
#        ''')
#        conn.commit()
#        cur.close()
#        conn.close()
#        print("[OK] Banco de dados **postgres_vuln** inicializado com sucesso!")
#
#
#
#    except Exception as e:
#        print(e)