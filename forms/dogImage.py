from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SelectField, FileField, validators
from flask_wtf.file import FileField, FileAllowed, FileRequired, DataRequired
from wtforms.fields.html5 import EmailField
from wtforms.widgets import html_params


class DogImage(FlaskForm):
    image = FileField('Image File', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])