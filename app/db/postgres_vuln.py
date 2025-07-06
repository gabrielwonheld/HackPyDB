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


try:


    def init_db_postgres_vuln():
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(''' 
            CREATE TABLE IF NOT EXISTS tarefas (
                id SERIAL PRIMARY KEY,
                titulo TEXT NOT NULL,
                status TEXT NOT NULL
            );
        ''')

        cur.execute('''

            CREATE TABLE IF NOT EXISTS missions (
                    id SERIAL PRIMARY KEY,
                    mission_name VARCHAR(255),
                    status VARCHAR(100)
            )
    ''')


        conn.commit()
        cur.close()
        conn.close()
        print("[OK] Banco de dados inicializado com sucesso!")

except Exception as e:
    print(e)