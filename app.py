from flask import Flask, render_template, request, redirect, url_for, json, jsonify, Response
import sqlite3
import os
import csv
from datetime import datetime, timedelta
from io import StringIO

app = Flask(__name__)

def iniciar_banco():
    caminho = os.path.join(os.path.dirname(__file__), 'database.db')
    conn = sqlite3.connect(caminho)
    # Criar tabela de gastos (Adicionei a coluna 'tipo' que estava faltando no seu INSERT)
    conn.execute('''CREATE TABLE IF NOT EXISTS gastos 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     valor REAL, 
                     categoria TEXT, 
                     tipo TEXT, 
                     data TEXT)''')
    # Criar tabela de metas
    conn.execute('''CREATE TABLE IF NOT EXISTS metas 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     categoria TEXT, 
                     valor_limite REAL, 
                     mes TEXT)''')
    conn.commit()
    conn.close()

def get_db():
    caminho = os.path.join(os.path.dirname(__file__), 'database.db')
    conn = sqlite3.connect(caminho)
    conn.row_factory = sqlite3.Row
    return conn

iniciar_banco()

@app.route('/')
def index():
    agora = datetime.now()
    mes_real = agora.strftime('%Y-%m')
    mes_selecionado = request.args.get('mes', mes_real)
    mensagem_sucesso = request.args.get('mensagem_sucesso')
    
    conn = get_db()
    meta_db = conn.execute("SELECT valor_limite FROM metas WHERE categoria = 'Global' AND mes = ?", (mes_selecionado,)).fetchone()
    meta_global_valor = meta_db['valor_limite'] if meta_db else 0
    meta_atual_existe = meta_db is not None

    gastos = conn.execute("SELECT * FROM gastos WHERE strftime('%Y-%m', data) = ? ORDER BY data DESC", (mes_selecionado,)).fetchall()
    total_gasto = sum(g['valor'] for g in gastos)

    dados_pizza = {row['categoria']: row['total'] for row in conn.execute(
        "SELECT categoria, SUM(valor) as total FROM gastos WHERE strftime('%Y-%m', data) = ? GROUP BY categoria", 
        (mes_selecionado,)).fetchall()}
    conn.close()

    return render_template('index.html', 
                           gastos=gastos, total=total_gasto, 
                           mes_selecionado=mes_selecionado,
                           meta_global=meta_global_valor,
                           meta_atual_existe=meta_atual_existe,
                           mes_atual=mes_real,
                           dados_grafico=json.dumps(dados_pizza),
                           mensagem_sucesso=mensagem_sucesso)

@app.route('/add', methods=['POST'])
def add():
    valor = request.form.get('valor')
    categoria = request.form.get('categoria')
    tipo = request.form.get('tipo', 'Variável')
    data = request.form.get('data') or datetime.now().strftime('%Y-%m-%d')
    if valor and categoria:
        conn = get_db()
        conn.execute('INSERT INTO gastos (valor, categoria, tipo, data) VALUES (?, ?, ?, ?)', (float(valor), categoria, tipo, data))
        conn.commit()
        conn.close()
    return redirect(url_for('index', mes=data[:7]))

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    gasto = conn.execute('SELECT data FROM gastos WHERE id = ?', (id,)).fetchone()
    if gasto:
        mes_v = gasto['data'][:7]
        conn.execute('DELETE FROM gastos WHERE id = ?', (id,))
        conn.commit()
    conn.close()
    return redirect(url_for('index', mes=mes_v if gasto else None))
 

@app.route('/definir_meta', methods=['POST'])
def definir_meta():
    cat = request.form.get('categoria')
    limite = request.form.get('valor_limite')
    mes = request.form.get('mes')
    if cat and limite and mes:
        conn = get_db()
        conn.execute('INSERT OR REPLACE INTO metas (categoria, valor_limite, mes) VALUES (?, ?, ?)', (cat, float(limite), mes))
        conn.commit()
        conn.close()
    return redirect(url_for('index', mes=mes))

@app.route('/fechar_orcamento', methods=['POST'])
def fechar_orcamento():
    mes_ref = request.form.get('mes_referencia')
    

    dt = datetime.strptime(mes_ref + "-01", "%Y-%m-%d")
    prox_mes_dt = (dt + timedelta(days=32)).replace(day=1)
    prox_mes = prox_mes_dt.strftime('%Y-%m')


    conn = get_db()
    meta_p = conn.execute("SELECT valor_limite FROM metas WHERE categoria = 'Global' AND mes = ?", (mes_ref,)).fetchone()
    gasto_p = conn.execute("SELECT SUM(valor) FROM gastos WHERE strftime('%Y-%m', data) = ?", (mes_ref,)).fetchone()[0] or 0
    conn.close()

    msg = ""
    if meta_p:
        if gasto_p <= meta_p['valor_limite']:
            msg = f"🎉 Parabéns! Você fechou {mes_ref} dentro da meta. Economia de R$ {meta_p['valor_limite'] - gasto_p:.2f}!"
        else:
            msg = f"🚨 Orçamento de {mes_ref} excedido em R$ {gasto_p - meta_p['valor_limite']:.2f}."

    return redirect(url_for('index', mes=prox_mes, mensagem_sucesso=msg))

@app.route('/graficos')
def graficos():
    mes_sel = request.args.get('mes', datetime.now().strftime('%Y-%m'))
    conn = get_db()
    
    dados_pizza = {row['categoria']: row['total'] for row in conn.execute(
        "SELECT categoria, SUM(valor) as total FROM gastos WHERE strftime('%Y-%m', data) = ? GROUP BY categoria", 
        (mes_sel,)).fetchall()}

    ano = mes_sel[:4]
    dados_anual = {row['m']: row['t'] for row in conn.execute(
        "SELECT strftime('%m', data) as m, SUM(valor) as t FROM gastos WHERE strftime('%Y', data) = ? GROUP BY m ORDER BY m ASC", 
        (ano,)).fetchall()}

    metas = conn.execute("SELECT * FROM metas WHERE mes = ? ORDER BY (categoria='Global') DESC", (mes_sel,)).fetchall()
    conn.close()
    
    return render_template('graficos.html', 
                           dados_pizza=json.dumps(dados_pizza), 
                           dados_anual=json.dumps(dados_anual), 
                           mes_selecionado=mes_sel, 
                           metas=metas)

@app.route('/limpar_mes')
def limpar_mes():
    mes = request.args.get('mes')
    conn = get_db()
    conn.execute("DELETE FROM gastos WHERE strftime('%Y-%m', data) = ?", (mes,))
    conn.commit()
    conn.close()
    return redirect(url_for('index', mes=mes))

@app.route('/limpar_tudo')
def limpar_tudo():
    conn = get_db()
    conn.execute("DELETE FROM gastos"); conn.execute("DELETE FROM metas")
    conn.commit(); conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
