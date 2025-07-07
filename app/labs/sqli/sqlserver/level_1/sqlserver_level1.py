from app.db.mssql import get_connection as sqlserver_conn
from app.labs.sqli.services.mission_service import Missions

sqlserver_mission_service =  Missions(get_connection=sqlserver_conn, dbtype="mssql", placeholder="?", schema="level1")

def cadastrar_missao(nome_missao, status):
    return sqlserver_mission_service.add_mission(nome_missao, status)

def buscar_missoes_por_nome(nome):
    return sqlserver_mission_service.get_all_missions(nome)

def delete_mission(id):
   return sqlserver_mission_service.delete_mission(id)

def update_mission(termo):
    return sqlserver_mission_service.update_mission(termo)
