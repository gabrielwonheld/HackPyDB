from flask import Blueprint, render_template, request, redirect, url_for, session
from ..db.init_pyhackdb import get_app_db_connection
import pyodbc

auth_bp = Blueprint('auth', __name__, template_folder='templates/auth')


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            conn = get_app_db_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            print("[DEBUG] Query segura executada.")
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            if user:
                session["username"] = username
                return redirect(url_for('auth.account'))
            else:
                return "<h3>Credenciais inválidas.</h3>", 403
        except Exception as e:
            return f"<h3>Erro: {str(e)}</h3>", 500
        finally:
            conn.close()

    return render_template("login.html", error=error)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        print(email, username, password)

        try:
            conn = get_app_db_connection()
            cursor = conn.cursor()
            query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, password, email))
            conn.commit()
            return redirect(url_for("auth.login"))
        except pyodbc.IntegrityError:
            return "Usuário já existe!"
        except Exception as e:
            return f"Erro: {e}"
        finally:
            conn.close()

    return render_template("register.html")

@auth_bp.route("/account", methods=["GET"])
def account():
    if "username" not in session:
        return redirect(url_for("auth.login"))
    return render_template("account.html", username=session["username"])

@auth_bp.route('/logout')
def logout():
    session.clear()  # limpa todos os dados da sessão
    return redirect(url_for('auth.login'))