from flask import Response

class Missions():
    def __init__(self, get_connection, dbtype="postgres", placeholder="%s", schema=None):
        self.get_connection = get_connection
        self.placeholder = placeholder
        self.schema = schema
        self.dbtype = dbtype  # 'postgres', 'mysql', 'mssql'

    def _get_table_name(self):
        """Retorna o nome da tabela com base no banco e schema."""
        if self.dbtype == "mysql":
            return f"{self.schema}_missions" if self.schema else "missions"
        elif self.dbtype == "mssql":
            return f"[{self.schema}].[missions]" if self.schema else "missions"
        elif self.dbtype == "postgres":
            return f"{self.schema}.missions" if self.schema else "missions"
        else:
            return "missions"

    def add_mission(self, titulo, status):
        cursor, conn = None, None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            table = self._get_table_name()
            print(table)
            query = f"INSERT INTO {table} (mission_name, status) VALUES ({self.placeholder}, {self.placeholder})"
            cursor.execute(query, (titulo, status))
            conn.commit()
            return True
        except Exception as e:
            print(f"[ERRO] Ao adicionar missão: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_all_missions(self, termo):
        conn, cursor = None, None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            table = self._get_table_name()
            # query = f"SELECT * FROM {table} WHERE mission_name LIKE {self.placeholder}"
            query = f"SELECT * FROM {table} WHERE mission_name LIKE '%{termo}%'"
            # cursor.execute(query, (f"%{termo}%",))
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"[ERRO] Ao buscar missões: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_mission(self, termo):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            table = self._get_table_name()
            # query = f"SELECT * FROM {table} WHERE mission_name LIKE {self.placeholder}"
            query = f"SELECT * FROM {table} WHERE mission_name LIKE '%{termo}%'"
            # cursor.execute(query, (f"%{termo}%",))
            cursor.execute(query)
            mission = cursor.fetchall()
            print(mission)
            return mission
        except Exception as e:
            return Response(f"{str(e)}", status=500, mimetype='text/plain')
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def pendente_mission(self, termo):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            table = self._get_table_name()
            query = f"SELECT * FROM {table} WHERE mission_name LIKE {self.placeholder}"
            cursor.execute(query, (f"%{termo}%",))
            return cursor.fetchall()
        except Exception as e:
            return [("Erro SQL", str(e))]
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def update_status(self, id, status):
        conn = self.get_connection()
        cursor = conn.cursor()
        table = self._get_table_name()
        query = f"UPDATE {table} SET status = {self.placeholder} WHERE id = {self.placeholder}"
        cursor.execute(query, (status, id))
        conn.commit()
        cursor.close()
        conn.close()

    def delete_mission(self, id):
        conn = self.get_connection()
        cursor = conn.cursor()
        table = self._get_table_name()
        query = f"DELETE FROM {table} WHERE id = {self.placeholder}"
        cursor.execute(query, (id,))
        conn.commit()
        cursor.close()
        conn.close()
