from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash

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
    lista_restaurantes = []
    for r in restaurantes:
        horarios_reservados = db.execute(
            "SELECT hora_reserva FROM reservas WHERE id_restaurante = ?", (r['id'],)
        ).fetchall()
        r = dict(r)
        r['horarios_reservados'] = [h['hora_reserva'] for h in horarios_reservados]
        lista_restaurantes.append(r)

    return render_template("index.html", restaurantes=lista_restaurantes, nome=session["usuario_nome"])

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
            INSERT INTO reservas (id_usuario, id_restaurante, data_reserva, hora_reserva, numero_pessoas)
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
        FROM reservas r
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

@app.route("/cancelar_reserva/<int:reserva_id>", methods=["POST"])
def cancelar_reserva(reserva_id):
    db = get_db()
    db.execute("DELETE FROM reservas WHERE id = ?", (reserva_id,))
    db.commit()
    return redirect(url_for("minhas_reservas"))

@app.route("/cadastro_restaurante", methods=["GET", "POST"])
def cadastro_restaurante():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "").strip()
        horarios = request.form.get("horarios", "").strip()
        if not nome or not email or not senha:
            return render_template("cadastro_restaurante.html", erro="Preencha todos os campos")
        db = get_db()
        # verifica email único
        existente = db.execute("SELECT id FROM restaurantes WHERE email = ?", (email,)).fetchone()
        if existente:
            return render_template("cadastro_restaurante.html", erro="Email já cadastrado")
        senha_hash = generate_password_hash(senha)
        db.execute(
            "INSERT INTO restaurantes (nome, email, senha, horario_disponivel) VALUES (?, ?, ?, ?)",
            (nome, email, senha_hash, horarios)
        )
        db.commit()
        return redirect(url_for("login"))
    return render_template("cadastro_restaurante.html")

# --- rota de login para restaurante (usa o nome do restaurante) ---
@app.route("/login_restaurante", methods=["POST"])
def login_restaurante():
    email = request.form.get("email_rest", "").strip().lower()
    senha = request.form.get("senha_rest", "").strip()
    if not email or not senha:
        return render_template("login.html", erro="Email e senha obrigatórios")
    db = get_db()
    row = db.execute("SELECT * FROM restaurantes WHERE email = ?", (email,)).fetchone()
    if not row:
        return render_template("login.html", erro="Email ou senha inválidos")
    if not check_password_hash(row["senha"], senha):
        return render_template("login.html", erro="Email ou senha inválidos")
    # sucesso: criar sessão específica para restaurante
    session.clear()
    session["restaurante_id"] = row["id"]
    session["restaurante_nome"] = row["nome"]
    return redirect(url_for("minhas_reservas_restaurante"))

# --- área do restaurante: mostra reservas deste restaurante e horários disponíveis ---
@app.route("/minhas_reservas_restaurante")
def minhas_reservas_restaurante():
    if "restaurante_id" not in session:
        return redirect(url_for("login"))
    rest_id = session["restaurante_id"]
    db = get_db()
    reservas = db.execute("""
        SELECT r.id, u.nome AS cliente_nome, r.data_reserva, r.hora_reserva, r.numero_pessoas
        FROM reservas r
        LEFT JOIN usuarios u ON r.id_usuario = u.id
        WHERE r.id_restaurante = ?
        ORDER BY r.data_reserva, r.hora_reserva
    """, (rest_id,)).fetchall()
    # carrega horários disponíveis e transforma em lista
    row = db.execute("SELECT horario_disponivel FROM restaurantes WHERE id = ?", (rest_id,)).fetchone()
    horarios = []
    if row and row["horario_disponivel"]:
        horarios = [h.strip() for h in row["horario_disponivel"].split(",") if h.strip()]
    return render_template("minhas_reservas_restaurante.html", reservas=reservas, horarios=horarios)

# --- remover um horário disponível do restaurante (POST) ---
@app.route("/remover_horario/<int:rest_id>", methods=["POST"])
def remover_horario(rest_id):
    if "restaurante_id" not in session or session["restaurante_id"] != rest_id:
        return redirect(url_for("login"))
    horario = request.form.get("horario", "").strip()
    if not horario:
        return redirect(url_for("minhas_reservas_restaurante"))
    db = get_db()
    row = db.execute("SELECT horario_disponivel FROM restaurantes WHERE id = ?", (rest_id,)).fetchone()
    if not row:
        return redirect(url_for("minhas_reservas_restaurante"))
    horarios = [h.strip() for h in (row["horario_disponivel"] or "").split(",") if h.strip()]
    horarios = [h for h in horarios if h != horario]
    novo = ",".join(horarios)
    db.execute("UPDATE restaurantes SET horario_disponivel = ? WHERE id = ?", (novo, rest_id))
    db.commit()
    return redirect(url_for("minhas_reservas_restaurante"))

# --- excluir restaurante (apaga restaurante e reservas relacionadas) ---
@app.route("/excluir_restaurante/<int:rest_id>", methods=["POST"])
def excluir_restaurante(rest_id):
    if "restaurante_id" not in session or session["restaurante_id"] != rest_id:
        return redirect(url_for("login"))
    db = get_db()
    db.execute("DELETE FROM reservas WHERE id_restaurante = ?", (rest_id,))
    db.execute("DELETE FROM restaurantes WHERE id = ?", (rest_id,))
    db.commit()
    # limpa sessão do restaurante e volta ao login
    session.pop("restaurante_id", None)
    session.pop("restaurante_nome", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
