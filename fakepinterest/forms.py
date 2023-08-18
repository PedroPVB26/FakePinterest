from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from fakepinterest.models import Usuario
from fakepinterest import bcrypt

class FormLogin(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao_submit = SubmitField("Fazer Login")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if not usuario:
            raise ValidationError("Email não cadastrado, crie uma conta")

    def validate_senha(self, field):
        usuario = Usuario.query.filter_by(email=self.email.data).first()
        if bcrypt.check_password_hash(usuario.senha, self.senha.data) == False:
            raise ValidationError("Senha Incorreta")


class FormCadastro(FlaskForm):
    username = StringField("Nome de Usuário", validators=[DataRequired()])
    email =  StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6,20)])
    confirmacao_senha = PasswordField("Confirmação de Senha", validators=[DataRequired(), EqualTo("senha")])
    botao_submit = SubmitField("Criar Conta")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("Email já cadastrado, faça login para continuar")

class FormFoto(FlaskForm):
    foto = FileField("Foto", validators=[FileAllowed(['jpg','png']), DataRequired()])
    botao_submit = SubmitField("Enviar")