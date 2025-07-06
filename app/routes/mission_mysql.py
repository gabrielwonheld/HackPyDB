from flask import Blueprint, request, redirect, render_template, session, url_for
from app.db.mysql import get_connection

mission_bp = Blueprint('mission', __name__)

@mission_bp.route('/mission_add', methods=['GET', 'POST'])
def add_mission():

    if "username" not in session:

        return redirect(url_for("auth.login"))


    if request.method == 'POST':
        titulo = request.form.get('titulo')
        status = request.form.get('status')

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO missions (mission_name, status) VALUES (%s, %s)", (titulo, status))
            conn.commit()
        except Exception as e:
            print(f"[ERRO] Ao adicionar missão: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return redirect(url_for('mission.add_mission'))
    # GET request
    conn = None
    cursor = None
    missions = []
    flag = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, mission_name, status FROM missions")
        missions = cursor.fetchall()

        cursor.execute("SELECT message FROM flag LIMIT 1")
        flag = cursor.fetchone()
    except Exception as e:
        print(f"[ERRO] Ao buscar missões: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template('mission_add.html', missions=missions, flag=flag)

@mission_bp.route('/mission_update', methods=['GET'])
def mission_update():
    
    # if "username" not in session:
        # return redirect(url_for('auth.login'))
    
    termo = request.args.get('q', '')
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # VULNERABILIDADE SQL INJECTION AQUI
        query = f"SELECT * FROM missions WHERE mission_name LIKE '%{termo}%'"
        cursor.execute(query)
        mission = cursor.fetchall()
    except Exception as e:
        return f"Erro: {e}"
    finally:
        cursor.close()
        conn.close()

    # Retorna dados visíveis — ideal para sqlmap
    return render_template('mission_update.html', missions=mission)
    #return str(resultados)


@mission_bp.route('/concluir_mission/<int:id>', methods=['POST'])
def concluir_mission(id):

    if "username" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE missions SET status = 'concluido' WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/mission_update')

@mission_bp.route('/pendente_mission/<int:id>', methods=['POST'])
def pendente_mission(id):

    if "username" not in session:
        return redirect(url_for("auth.login"))
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE missions SET status = 'pendente' WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/mission_update')

@mission_bp.route('/excluir_mission/<int:id>', methods=['POST'])
def excluir_mission(id):
    if "username" not in session:
        return redirect(url_for("auth.login"))
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM missions WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/mission_update')