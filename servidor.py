from flask import Flask, request, session, render_template, redirect
from model import usuarios

app = Flask(__name__)
app.secret_key = "HI_LORENA1234"

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def logar():
    msg=''
    if request.method == 'POST':
        nome = request.form.get('nome')
        senha = request.form.get('senha')
        if nome in usuarios:
            if senha == str(usuarios.get(nome)):
                session['usuario'] = nome
                return redirect('/alunos/5')
            else:
                msg="Senha inválida!"
        else:
            msg = "Nome não encontrado!"
    return render_template('login.html', erro=msg)

@app.route('/alunos')
@app.route('/alunos/<int:qtd>')
def adicionar_alunos(qtd=5):
    if 'usuario' in session and qtd > 0:
        session['qtd'] = qtd
        return render_template('alunos.html', n=qtd)
    else:
        return redirect('/login')

@app.route('/resultado', methods=['GET', 'POST'])
def resultado():
    if 'usuario' in session:
        if request.method == 'POST':
            qtd = session.get('qtd')
            dic = {}
            for i in range(1, qtd+1):
                nome = request.form.get(f'nome{i}')
                media = request.form.get(f'media{i}')
                dic[nome] = float(media)
            return render_template('resultado.html', alunos=dic)
        else:
            return redirect('/alunos')
    return redirect('/login')

@app.route('/sair')
def sair():
    session.clear()
    return redirect('/login')
app.run(debug=True)