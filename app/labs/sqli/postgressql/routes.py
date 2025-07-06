from flask import Blueprint, render_template, request, redirect, url_for, session,Response
from app.labs.sqli.postgressql.postgres_level1 import cadastrar_missao, buscar_missoes_por_nome, delete_mission, update_mission



postgres_mission_bp = Blueprint('mission_postgres', __name__,template_folder='templates_postgres')

@postgres_mission_bp.route('/mission_add_postgres', methods=['GET', 'POST'])
def mission_add():
    if "username" not in session:
        return redirect(url_for("auth.login"))
    
    if request.method == "POST":
        titulo = request.form.get("titulo")
        status = request.form.get("status")
        cadastrar_missao(titulo, status)
        return redirect(url_for("mission_postgres.mission_add"))  # redireciona para o GET
    
    return render_template("mission_add_postgres.html")

@postgres_mission_bp.route('/mission_update_postgres', methods=['GET'])
def mission_update():
    print("postgres")

    if "username" not in session:
        return redirect(url_for("auth.login"))
    
    try:
        termo = request.args.get('q', '')
        missions = buscar_missoes_por_nome(termo)  # busca tudo ou define um padrão
        print(missions)
        return render_template("mission_update_postgres.html", missions=missions)

    except Exception as e:
        return Response(f"{str(e)}", status=500, mimetype='text/plain')


@postgres_mission_bp.route('/excluir_mission_postgres/<int:id>', methods=['POST'])
def mission_delete(id):

    if "username" not in session:
        return redirect(url_for("auth.login"))
    
    print("Olá print")


    delete_mission(id)
    return redirect('/mission_update')
    
