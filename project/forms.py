from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, DateField
from wtforms.validators import InputRequired, NumberRange, DataRequired

class HealthDataForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    exercise = IntegerField('Exercise (minutes)', validators=[InputRequired(), NumberRange(min=0)])
    meditation = IntegerField('Meditation (minutes)', validators=[InputRequired(), NumberRange(min=0)])
    sleep = IntegerField('Sleep (hours)', validators=[InputRequired(), NumberRange(min=0, max=24)])
    submit = SubmitField('Submit')
