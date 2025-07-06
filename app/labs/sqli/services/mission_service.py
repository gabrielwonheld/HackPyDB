from flask import Response

class Missions():
    
    def __init__(self,get_connection, placeholder = '%s'):
        self.get_connection = get_connection
        self.placeholder = placeholder
    
    
    def add_mission(self,titulo,status):

        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            print('Debug master', titulo, status)
            cursor.execute(f"INSERT INTO missions (mission_name, status) VALUES ({self.placeholder}, {self.placeholder})", (titulo, status))
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
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            query = f"SELECT * FROM missions WHERE mission_name LIKE '%{termo}%'"
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
    
    def update_mission(self,termo):

        try:
            conn = self.get_connection()
            cursor = conn.cursor()
    
            query = f"SELECT * FROM missions WHERE mission_name LIKE '%{termo}%'"
            #print(f"[DEBUG] Query: {query}")  # Para debug interno
    
            cursor.execute(query)
            mission = cursor.fetchall()
            return mission
    
        except Exception as e:
            # Retorna só a mensagem do erro
            return Response(f"{str(e)}", status=500, mimetype='text/plain')
    
        finally:
            if cursor: cursor.close()
            if conn: conn.close()


    def pendente_mission(self,termo):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # VULNERABILIDADE SQL INJECTION AQUI
            query = f"SELECT * FROM missions WHERE mission_name LIKE '%{termo}%'"
            cursor.execute(query)
            mission = cursor.fetchall()
        except Exception as e:
            #return f"Erro: {e}"
            return [("Erro SQL", str(e))]
        finally:
            cursor.close()
            conn.close()

    def update_status(self,id, status):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"UPDATE missions SET status = {self.placeholder} WHERE id = {self.placeholder}", (status, id))
        conn.commit()
        cursor.close()
        conn.close()

    def delete_mission(self,id):
        conn = self.get_connection()
        cursor = conn.cursor()
        print('No service',id)
        cursor.execute(f"DELETE FROM missions WHERE id = {self.placeholder}", (id,))
        conn.commit()
        cursor.close()
        conn.close()
