from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class TopicsForm(FlaskForm):
    topic_name = StringField(validators=[DataRequired()])
    submit_field = SubmitField("Get Topics")
