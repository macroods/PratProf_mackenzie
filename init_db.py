import sqlite3

con = sqlite3.connect("database.db")
cur = con.cursor()

# Tabela de usuários
cur.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
);
""")

# Inserir usuário de exemplo
cur.execute(
    "INSERT OR IGNORE INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
    ('João', 'joao@email.com', '123')
)

# Tabela de restaurantes
cur.execute("""
CREATE TABLE IF NOT EXISTS restaurantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE,
    senha TEXT,
    horario_disponivel TEXT NOT NULL
);
""")

# Inserir restaurantes de exemplo
cur.executemany(
    "INSERT OR IGNORE INTO restaurantes (nome, email, senha, horario_disponivel) VALUES (?, ?, ?, ?)",
    [
        ("Sabor da Serra", "sabor@exemplo.com", "rest123", "12:00, 13:00, 14:00"),
        ("La Pasta Bella", "lapasta@exemplo.com", "rest123", "19:00, 20:00, 21:00"),
        ("Sushi Zen", "sushizen@exemplo.com", "rest123", "18:00, 19:30, 21:00"),
    ]
)

# Tabela de reservas
cur.execute('''
CREATE TABLE IF NOT EXISTS reservas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    id_restaurante INTEGER NOT NULL,
    data_reserva TEXT NOT NULL,
    hora_reserva TEXT NOT NULL,
    numero_pessoas INTEGER NOT NULL,
    observacoes TEXT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
    FOREIGN KEY (id_restaurante) REFERENCES restaurantes(id)
)
''')

con.commit()
con.close()
print("Banco de dados criado com sucesso!")
