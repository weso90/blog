from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class EntryForm(FlaskForm):
    title = StringField('Tytuł wpisu', validators=[DataRequired()])
    body = TextAreaField('Treść', validators=[DataRequired()])
    is_published = BooleanField('Wpis opublikowany', default=False)
    