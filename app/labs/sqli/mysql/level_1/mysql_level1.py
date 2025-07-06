from app.db.mysql import get_connection as mysql_conn
from app.labs.sqli.services.mission_service import Missions

mysql_mission_service = Missions(mysql_conn)

def cadastrar_missao(nome_missao, status):
    return mysql_mission_service.add_mission(nome_missao, status)

def buscar_missoes_por_nome(nome):
    return mysql_mission_service.get_all_missions(nome)

def delete_mission(id):
    return mysql_mission_service.delete_mission(id)

def update_mission(termo):
    return mysql_mission_service.update_mission(termo)
