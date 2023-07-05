from flask import Flask, render_template, request, redirect, session, flash, url_for


class Som:
    def __init__(self, nome, banda, genero):
        self.nome = nome
        self.banda = banda
        self.genero = genero


som1 = Som('Live Wire', 'AC/DC', 'Hard Rock')
som2 = Som('Enter Sandman', 'Metallica', 'Heavy Metal')
som3 = Som('Satisfaction', 'Rolling Stones', 'Classic Rock')
lista = [som1, som2, som3]


class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha


usuario1 = Usuario("Laura", "La", "alohomora")
usuario2 = Usuario("Lorenzzo Batista", "Lo", "1903")
usuario3 = Usuario("Luísa", "Lu", "Theotimo")

usuarios = {usuario1.nickname: usuario1,
            usuario2.nickname: usuario2,
            usuario3.nickname: usuario3}


app = Flask(__name__)
app.secret_key = 'Lolo'


@app.route('/')
def index():
    return render_template('lista.html', titulo='Sons', sons=lista)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('log', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Som')


@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    banda = request.form['banda']
    genero = request.form['genero']
    som = Som(nome, banda, genero)
    lista.append(som)
    return redirect(url_for('index'))


@app.route('/log')
def log():
    proxima = request.args.get('proxima')
    return render_template('log.html', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado')
        return redirect(url_for('log'))


@app.route('/out')
def out():
    session['usuario_logado'] = None
    flash('Logout feito!')
    return redirect(url_for('index'))


app.run(debug=True)
