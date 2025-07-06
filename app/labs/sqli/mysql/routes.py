from flask import Blueprint, render_template, request, redirect, url_for, session,Response
from app.labs.sqli.mysql.mysql_level1 import cadastrar_missao, buscar_missoes_por_nome, delete_mission, update_mission



mission_bp = Blueprint('mission_mysql', __name__,template_folder='templates')

@mission_bp.route('/mission_add', methods=['GET', 'POST'])
def mission_add():
    if "username" not in session:
        return redirect(url_for("auth.login"))
    
    if request.method == "POST":
        titulo = request.form.get("titulo")
        status = request.form.get("status")
        cadastrar_missao(titulo, status)
        return redirect(url_for("mission_mysql.mission_add"))  # redireciona para o GET
    
    return render_template("mission_add.html")

@mission_bp.route('/mission_update', methods=['GET'])
def mission_update():

    if "username" not in session:
        return redirect(url_for("auth.login"))
    
    try:
        termo = request.args.get('q', '')
        missions = buscar_missoes_por_nome(termo)  # busca tudo ou define um padrão
        return render_template("mission_update.html", missions=missions)

    except Exception as e:
        return Response(f"{str(e)}", status=500, mimetype='text/plain')


@mission_bp.route('/excluir_mission_mysql/<int:id>', methods=['POST'])
def mission_delete(id):

    if "username" not in session:
        return redirect(url_for("auth.login"))

    delete_mission(id)
    return redirect('/mission_update')
    
