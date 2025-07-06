from app.db.postgres_vuln import get_db_connection as postgres_conn
from app.labs.sqli.services.mission_service import Missions

postgres_mission_service = Missions(postgres_conn,'%s')

def cadastrar_missao(nome_missao, status):
    return postgres_mission_service.add_mission(nome_missao, status)

def buscar_missoes_por_nome(nome):
    return postgres_mission_service.get_all_missions(nome)

def delete_mission(id):
    return postgres_mission_service.delete_mission(id)

def update_mission(termo):
    return postgres_mission_service.update_mission(termo)
