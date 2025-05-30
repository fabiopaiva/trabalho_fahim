from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Conexão MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="500195",
    database="escola_materiais"
)
cursor = conn.cursor(dictionary=True)

# Página principal (listar)
@app.route('/')
def index():
    cursor.execute("SELECT * FROM materiais")
    materiais = cursor.fetchall()
    return render_template('index.html', materiais=materiais)

# Página de formulário
@app.route('/novo')
def novo():
    return render_template('form.html')

# Inserir material
@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    tipo = request.form['tipo']
    quantidade = request.form['quantidade']
    localizacao = request.form['localizacao']
    observacao = request.form['observacao']
    cursor.execute('''
        INSERT INTO materiais (nome, tipo, quantidade, localizacao, observacao)
        VALUES (%s, %s, %s, %s, %s)
    ''', (nome, tipo, quantidade, localizacao, observacao))
    conn.commit()
    return redirect('/')

# Deletar material
@app.route('/deletar/<int:id>')
def deletar(id):
    cursor.execute("DELETE FROM materiais WHERE id = %s", (id,))
    conn.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
