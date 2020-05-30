from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Optional


''' Форма для модерации нового вопроса '''
class CheckQuestionForm(FlaskForm):
    text = TextAreaField('Текст вопроса', validators=[DataRequired()], default='')
    answer = TextAreaField('Правильный ответ', validators=[DataRequired()], default='')
    comment = TextAreaField('Комментарии к ответу на вопрос', default='')
    category = SelectField('Категория', validators=[Optional()], choices=[], default='')
    wrong_answer1 = TextAreaField('Неправильные варианты ответа', validators=[DataRequired()])
    wrong_answer2 = TextAreaField('', validators=[DataRequired()])
    wrong_answer3 = TextAreaField('', validators=[DataRequired()])
    type = SelectField('Тип вопроса', validators=[Optional()], choices=['all', 'write', 'change'], default='all')
    comp = SelectField('Сложность вопроса', validators=[Optional()], choices=['1', '2', '3', '4', '5'], default='1')
    submit = SubmitField('Редактировать вопрос')
    submitOUT = SubmitField('Удалить вопрос')