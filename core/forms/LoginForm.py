from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
