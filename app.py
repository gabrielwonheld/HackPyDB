from app import create_app
from app.db.mssql import init_db_mssql
from app.db.postgres_vuln import init_db_postgres_vuln
from app.db.mysql import init_db_mysql
from app.db.init_pyhackdb import init_app_db_postgres

app = create_app()

if __name__ == "__main__":
    init_app_db_postgres()
    init_db_mssql()  # Inicializa as tabelas se ainda não existirem
    # init_db_postgres_vuln()  # Inicializa as tabelas se ainda não existirem
    # init_db_mysql() # Inicializa as tabelas do mysql
    app.run(host="0.0.0.0", port=80, debug=True)
