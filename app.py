from flask import Flask, render_template, request, redirect, url_for, json, jsonify, Response
import sqlite3
import os
import csv
from datetime import datetime, timedelta
from io import StringIO

app = Flask(__name__)

from flask import Flask, render_template, request, redirect, url_for, json, jsonify, Response
import sqlite3
import os
import csv
from datetime import datetime, timedelta
from io import StringIO

app = Flask(__name__)

def get_db():
    caminho = os.path.join(os.path.dirname(__file__), 'database.db')
    conn = sqlite3.connect(caminho)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    agora = datetime.now()
    mes_real = agora.strftime('%Y-%m')
    mes_selecionado = request.args.get('mes', mes_real)
    conn = get_db()
    meta_db = conn.execute("SELECT valor_limite FROM metas WHERE categoria = 'Global' AND mes = ?", (mes_selecionado,)).fetchone()
    meta_atual_existe = meta_db is not None
    meta_global_valor = meta_db['valor_limite'] if meta_atual_existe else 0
    gastos = conn.execute("SELECT * FROM gastos WHERE strftime('%Y-%m', data) = ? ORDER BY data DESC", (mes_selecionado,)).fetchall()
    total_gasto = sum(g['valor'] for g in gastos)
    
    dados_grafico = {row['categoria']: row['total'] for row in conn.execute("SELECT categoria, SUM(valor) as total FROM gastos WHERE strftime('%Y-%m', data) = ? GROUP BY categoria", (mes_selecionado,)).fetchall()}
    conn.close()
    
    return render_template('index.html', gastos=gastos, total=total_gasto, meta_global=meta_global_valor, meta_atual_existe=meta_atual_existe, mes_selecionado=mes_selecionado, dados_grafico=json.dumps(dados_grafico))

@app.route('/proximo_mes')
def proximo_mes():
    mes_atual = request.args.get('mes')
    data = datetime.strptime(mes_atual + "-01", "%Y-%m-%d")
    proximo = (data + timedelta(days=32)).replace(day=1)
    return redirect(url_for('index', mes=proximo.strftime('%Y-%m')))

@app.route('/add', methods=['POST'])
def add_gasto():
    valor = request.form.get('valor')
    categoria = request.form.get('categoria')
    data = request.form.get('data')
    mes_ref = data[:7]
    conn = get_db()
    conn.execute("INSERT INTO gastos (valor, categoria, data) VALUES (?, ?, ?)", (valor, categoria, data))
    conn.commit()
    conn.close()
    return redirect(url_for('index', mes=mes_ref))

@app.route('/delete/<int:id>')
def delete_gasto(id):
    conn = get_db()
    gasto = conn.execute("SELECT data FROM gastos WHERE id = ?", (id,)).fetchone()
    mes_ref = gasto['data'][:7]
    conn.execute("DELETE FROM gastos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index', mes=mes_ref))

@app.route('/definir_meta', methods=['POST'])
def definir_meta():
    valor = request.form.get('valor')
    mes = request.form.get('mes')
    conn = get_db()
    conn.execute("INSERT OR REPLACE INTO metas (categoria, valor_limite, mes) VALUES ('Global', ?, ?)", (valor, mes))
    conn.commit()
    conn.close()
    return redirect(url_for('index', mes=mes))

@app.route('/graficos')
def graficos():
    mes_sel = request.args.get('mes', datetime.now().strftime('%Y-%m'))
    conn = get_db()
    dp = {row['categoria']: row['total'] for row in conn.execute("SELECT categoria, SUM(valor) as total FROM gastos WHERE strftime('%Y-%m', data) = ? GROUP BY categoria", (mes_sel,)).fetchall()}
    ano = mes_sel[:4]
    da = {row['m']: row['t'] for row in conn.execute("SELECT strftime('%m', data) as m, SUM(valor) as t FROM gastos WHERE strftime('%Y', data) = ? GROUP BY m ORDER BY m ASC", (ano,)).fetchall()}
    metas = conn.execute("SELECT * FROM metas WHERE mes = ? ORDER BY (categoria='Global') DESC", (mes_sel,)).fetchall()
    conn.close()
    return render_template('graficos.html', dados_pizza=json.dumps(dp), dados_anual=json.dumps(da), mes_selecionado=mes_sel, metas=metas)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def index():
    agora = datetime.now()
    mes_real = agora.strftime('%Y-%m')
    mes_selecionado = request.args.get('mes', mes_real)
    
    conn = get_db()
    
    # Busca se a meta global existe para o mês
    meta_db = conn.execute("SELECT valor_limite FROM metas WHERE categoria = 'Global' AND mes = ?", (mes_selecionado,)).fetchone()
    meta_atual_existe = meta_db is not None
    meta_global_valor = meta_db['valor_limite'] if meta_atual_existe else 0

    # Busca todos os gastos do mês selecionado
    gastos = conn.execute("SELECT * FROM gastos WHERE strftime('%Y-%m', data) = ? ORDER BY data DESC", (mes_selecionado,)).fetchall()
    total_gasto = sum(g['valor'] for g in gastos)

    # Busca todas as metas do mês (Global e por Categoria)
    metas_mes = conn.execute("SELECT * FROM metas WHERE mes = ?", (mes_selecionado,)).fetchall()
    
    # Dados para o gráfico de pizza (Categorias)
    dados_pizza = conn.execute("SELECT categoria, SUM(valor) as total FROM gastos WHERE strftime('%Y-%m', data) = ? GROUP BY categoria", (mes_selecionado,)).fetchall()
    dados_grafico = {row['categoria']: row['total'] for row in dados_pizza}
    
    conn.close()
    
    return render_template('index.html', 
                           gastos=gastos, 
                           total=total_gasto, 
                           meta_global=meta_global_valor,
                           meta_atual_existe=meta_atual_existe,
                           mes_selecionado=mes_selecionado,
                           mes_atual=mes_selecionado,
                           metas_mes=metas_mes,
                           dados_grafico=json.dumps(dados_grafico))

@app.route('/add', methods=['POST'])
def add_gasto():
    valor = request.form.get('valor')
    categoria = request.form.get('categoria')
    data = request.form.get('data')
    tipo = request.form.get('tipo', 'Variável')
    
    if valor and categoria and data:
        conn = get_db()
        conn.execute("INSERT INTO gastos (valor, categoria, data, tipo) VALUES (?, ?, ?, ?)", 
                     (valor, categoria, data, tipo))
        conn.commit()
        conn.close()
    
    return redirect(url_for('index', mes=data[:7]))

@app.route('/definir_meta', methods=['POST'])
def definir_meta():
    categoria = request.form.get('categoria', 'Global')
    valor = request.form.get('valor')
    mes = request.form.get('mes')

    if valor and mes:
        conn = get_db()
        conn.execute("INSERT OR REPLACE INTO metas (categoria, valor_limite, mes) VALUES (?, ?, ?)",
                     (categoria, valor, mes))
        conn.commit()
        conn.close()
    
    return redirect(url_for('index', mes=mes))

@app.route('/delete/<int:id>')
def delete_gasto(id):
    conn = get_db()
    gasto = conn.execute("SELECT data FROM gastos WHERE id = ?", (id,)).fetchone()
    mes_redir = gasto['data'][:7] if gasto else datetime.now().strftime('%Y-%m')
    conn.execute("DELETE FROM gastos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index', mes=mes_redir))

@app.route('/graficos')
def graficos():
    mes_sel = request.args.get('mes', datetime.now().strftime('%Y-%m'))
    conn = get_db()
    
    # Pizza
    dp = {row['categoria']: row['total'] for row in conn.execute("SELECT categoria, SUM(valor) as total FROM gastos WHERE strftime('%Y-%m', data) = ? GROUP BY categoria", (mes_sel,)).fetchall()}
    
    # Anual
    ano = mes_sel[:4]
    da = {row['m']: row['t'] for row in conn.execute("SELECT strftime('%m', data) as m, SUM(valor) as t FROM gastos WHERE strftime('%Y', data) = ? GROUP BY m ORDER BY m ASC", (ano,)).fetchall()}
    
    metas = conn.execute("SELECT * FROM metas WHERE mes = ? ORDER BY (categoria='Global') DESC", (mes_sel,)).fetchall()
    conn.close()
    
    return render_template('graficos.html', dados_pizza=json.dumps(dp), dados_anual=json.dumps(da), mes_selecionado=mes_sel, metas=metas)

@app.route('/exportar_csv')
def exportar_csv():
    mes = request.args.get('mes')
    conn = get_db()
    cursor = conn.execute("SELECT data, categoria, valor, tipo FROM gastos WHERE strftime('%Y-%m', data) = ?", (mes,))
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Data', 'Categoria', 'Valor', 'Tipo'])
    cw.writerows(cursor.fetchall())
    return Response(si.getvalue(), mimetype="text/csv", headers={"Content-Disposition": f"attachment;filename=Vexto_{mes}.csv"})

@app.route('/limpar_mes')
def limpar_mes():
    mes = request.args.get('mes')
    if mes:
        conn = get_db()
        conn.execute("DELETE FROM gastos WHERE strftime('%Y-%m', data) = ?", (mes,))
        conn.execute("DELETE FROM metas WHERE mes = ?", (mes,))
        conn.commit()
        conn.close()
    return redirect(url_for('index', mes=mes))

if __name__ == '__main__':
    app.run(debug=True)
