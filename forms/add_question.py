from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Optional


class AddQuestionForm(FlaskForm):
    text = TextAreaField('Текст вопроса', validators=[DataRequired()])
    answer = StringField('Правильный ответ', validators=[DataRequired()])
    comments = TextAreaField('Комментарии к ответу на вопрос')
    category = SelectField('Категория', validators=[Optional()], choices=[], default='')
    wrong_answer1 = StringField('Неправильные варианты ответа', validators=[DataRequired()])
    wrong_answer2 = StringField('', validators=[DataRequired()])
    wrong_answer3 = StringField('', validators=[DataRequired()])
    submit = SubmitField('Отправить')
