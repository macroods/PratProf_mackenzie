from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3
from datetime import date

app = Flask(__name__)
app.secret_key = "segredo_simples"
DATABASE = "database.db"

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def do_login():
    email = request.form["email"]
    senha = request.form["senha"]

    db = get_db()
    user = db.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha)).fetchone()

    if user:
        session["usuario_id"] = user["id"]
        session["usuario_nome"] = user["nome"]
        return redirect(url_for("index"))
    else:
        return render_template("login.html", erro="Email ou senha incorretos")

@app.route("/index")
def index():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    db = get_db()
    restaurantes = db.execute("SELECT * FROM restaurantes").fetchall()
    return render_template("index.html", restaurantes=restaurantes, nome=session["usuario_nome"])

@app.route("/reserva/<int:id>", methods=["GET", "POST"])
def reserva(id):
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    db = get_db()
    restaurante = db.execute("SELECT * FROM restaurantes WHERE id = ?", (id,)).fetchone()

    if request.method == "POST":
        id_usuario = session["usuario_id"]
        numero_pessoas = request.form["numero_pessoas"]
        hora_reserva = request.form["hora_reserva"]
        data_reserva = date.today().isoformat()

        db.execute('''
            INSERT INTO reserva (id_usuario, id_restaurante, data_reserva, hora_reserva, numero_pessoas)
            VALUES (?, ?, ?, ?, ?)
        ''', (id_usuario, id, data_reserva, hora_reserva, numero_pessoas))
        db.commit()
        return redirect(url_for("minhas_reservas"))

    return render_template("reserva.html", restaurante=restaurante)

@app.route("/minhas_reservas")
def minhas_reservas():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    db = get_db()
    reservas = db.execute('''
        SELECT r.id, re.nome AS restaurante, r.data_reserva, r.hora_reserva, r.numero_pessoas
        FROM reserva r
        JOIN restaurantes re ON r.id_restaurante = re.id
        WHERE r.id_usuario = ?
        ORDER BY r.data_reserva, r.hora_reserva
    ''', (session["usuario_id"],)).fetchall()

    return render_template("minhas_reservas.html", reservas=reservas)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        db = get_db()
        # Verifica se o email já existe
        existente = db.execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()
        if existente:
            return render_template("cadastro.html", erro="Email já cadastrado")
        
        db.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
        db.commit()
        return redirect(url_for("login"))
    return render_template("cadastro.html")

if __name__ == "__main__":
    app.run(debug=True)
