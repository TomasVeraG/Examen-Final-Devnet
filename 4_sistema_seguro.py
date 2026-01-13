import sqlite3
import hashlib
from flask import Flask, request, render_template

app = Flask(__name__)
DB_NAME = "usuarios_examen.db"

# Función para encriptar contraseña (SHA256)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Inicializar Base de Datos
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    users = [
        ("Tomas Vera Garcia", "Devnet123"),
        ("Admin", "Cisco2025")
    ]
    for user, pwd in users:
        try:
            cursor.execute("INSERT INTO usuarios (username, password_hash) VALUES (?, ?)", (user, hash_password(pwd)))
        except sqlite3.IntegrityError:
            pass 
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def login():
    mensaje = ""
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]
        hashed_pwd = hash_password(pwd)
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password_hash = ?", (user, hashed_pwd))
        if cursor.fetchone():
            return f"<h1 style='color:green; text-align:center; margin-top:20%'>¡Bienvenido {user}! <br>Acceso Correcto (Puerto 5800)</h1>"
        else:
            mensaje = "Credenciales Incorrectas"
        conn.close()
            
    return render_template("login.html", mensaje=mensaje)

if __name__ == "__main__":
    init_db()
    print("Iniciando servidor seguro en puerto 5800...")
    app.run(host="0.0.0.0", port=5800)