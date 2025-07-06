from flask import Blueprint, render_template, request, redirect, url_for, session,Response
from app.labs.sqli.sqlserver.level_1.sqlserver_level1 import cadastrar_missao, buscar_missoes_por_nome, delete_mission, update_mission



sqlserver_mission_bp = Blueprint('sqlserver_level_1', __name__)

@sqlserver_mission_bp.route('/mission_add', methods=['GET', 'POST'])
def mission_add():
    if "username" not in session:
        return redirect(url_for("auth.login"))
    
    if request.method == "POST":
        titulo = request.form.get("titulo")
        status = request.form.get("status")
        cadastrar_missao(titulo, status)
        return redirect(url_for("sqlserver_level_1.mission_add"))  # redireciona para o GET
    
    return render_template("labs/sqli/sqlserver/level_1/mission_add.html")

@sqlserver_mission_bp.route('/mission_update', methods=['GET'])
def mission_update():
    print("ola print")

    if "username" not in session:
        return redirect(url_for("auth.login"))
    
    try:
        termo = request.args.get('q', '')
        missions = buscar_missoes_por_nome(termo)  # busca tudo ou define um padrão
        print(missions)
        return render_template("labs/sqli/sqlserver/level_1/mission_update.html", missions=missions)

    except Exception as e:
        return Response(f"{str(e)}", status=500)


@sqlserver_mission_bp.route('excluir_mission/<int:id>', methods=['POST'])
def mission_delete(id):
    if "username" not in session:
        return redirect(url_for("auth.login"))
    
    delete_mission(id)
    return redirect(url_for("sqlserver_level_1.mission_update"))
