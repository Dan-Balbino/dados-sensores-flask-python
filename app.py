from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)
DATABASE = "database.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS dados_sensores (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        sensor_id INTEGER, 
        temperatura REAL, 
        umidade REAL, 
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""")
    
    conn.commit()
    conn.close()

@app.route("/dados-sensores", methods=["POST"])
def inserir_dados():
    dados = request.get_json()
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO dados_sensores (sensor_id, temperatura, umidade) VALUES (?, ?, ?)", 
                   (dados['sensor_id'], dados['temperatura'], dados['umidade']))
    conn.commit()
    conn.close()
    return jsonify({'message': "Dados inseridos com sucesso"}), 201  

@app.route("/dados-sensores", methods=["GET"])
def buscar_dados():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dados_sensores")
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

@app.route("/limpar-dados", methods=["DELETE"])
def limpar_dados():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM dados_sensores")
    conn.commit()
    conn.close()
    return jsonify({"message": "Dados limpos com sucesso"}), 200

@app.route("/dados-sensores-json")
def dados_sensores_json():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT timestamp, temperatura, umidade FROM dados_sensores')
    rows = cursor.fetchall()
    conn.close()
    
    timestamps = [row[0] for row in rows]
    temperaturas = [row[1] for row in rows]
    umidades = [row[2] for row in rows]
    
    return jsonify({
        'timestamp': timestamps,
        'temperatura': temperaturas,
        'umidade': umidades
    })

@app.route("/")
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dados_sensores")
    dados = cursor.fetchall()
    conn.close()
    return render_template('index.html', dados=dados)

@app.route("/graficos")
def graficos():
    return render_template("grafico.html")

if __name__ == '__main__':
    app.run(debug=True)
