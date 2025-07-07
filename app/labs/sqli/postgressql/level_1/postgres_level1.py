from app.db.postgres_vuln import get_db_connection as postgres_conn, get_connection_level1
from app.labs.sqli.services.mission_service import Missions

postgres_mission_service = Missions(get_connection=get_connection_level1, dbtype="postgres", placeholder="%s", schema="level1")

def cadastrar_missao(nome_missao, status):
    return postgres_mission_service.add_mission(nome_missao, status)

def buscar_missoes_por_nome(nome):
    return postgres_mission_service.get_all_missions(nome)

def delete_mission(id):
    return postgres_mission_service.delete_mission(id)

def update_mission(termo):
    return postgres_mission_service.update_mission(termo)
