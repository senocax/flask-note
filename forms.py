from flask_wtf import FlaskForm
from wtforms import Form, IntegerField,SelectField,SubmitField,StringField
from wtforms.validators import DataRequired	

class PersonaForm(FlaskForm):
        nombre = StringField('Nombre', validators=[DataRequired('Ingresa un Nombre')])
        apellido = StringField('Apellido', validators=[DataRequired('Ingresa apellido')])
        email = StringField('Email', validators=[DataRequired('Ingresa un email')])
        enviar= SubmitField('Enviar')


