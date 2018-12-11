
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, IntegerField, \
    TextAreaField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired, Length, ValidationError, Email


# 4.3.1 basic form example
class CheckHashForm(FlaskForm):
    hash_1 = StringField('String_1', validators=[DataRequired()])
    hash_2 = StringField('String_2', validators=[DataRequired()])
    submit = SubmitField('Collide')


