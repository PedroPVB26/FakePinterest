from flask import render_template, url_for,redirect
from fakepinterest import app, database, bcrypt
from fakepinterest.forms import FormLogin, FormCadastro, FormFoto
from fakepinterest.models import Usuario, Foto
from flask_login import login_required, login_user, logout_user, current_user
import os
from werkzeug.utils import secure_filename

@app.route('/', methods=["GET", "POST"])
def homepage():
    formLogin = FormLogin()
    if formLogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formLogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formLogin.senha.data):
            login_user(usuario)
            return redirect(url_for('perfil', id_usuario=usuario.id))
    return render_template('homepage.html', form=formLogin)

@app.route('/criarconta', methods=["GET", "POST"])
def criar_contar():
    form_criar_conta = FormCadastro()
    if form_criar_conta.validate_on_submit():
        senha = bcrypt.generate_password_hash(form_criar_conta.senha.data)
        usuario = Usuario(username=form_criar_conta.username.data, email=form_criar_conta.email.data, senha=senha)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for('perfil', id_usuario=usuario.id))

    return render_template("criarconta.html", form=form_criar_conta)


@app.route('/perfil/<id_usuario>', methods=["GET","POST"])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            # Salvando o arquivo na pasta fotos_posts
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)) # Primeiro pega a linha de onde o código tá, faz a mesma coisa que 'app.root_path'
                              , app.config["UPLOAD_FOLDER"], nome_seguro)
            arquivo.save(caminho)

            # Registrar esse arquivo no banco de dados
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
        return render_template("perfil.html", usuario=current_user, form=form_foto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template('perfil.html', usuario=usuario, form=None)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/feed')
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()
    return render_template("feed.html", fotos=fotos)