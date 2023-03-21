from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Optional


''' Форма для добавления нового вопроса '''
class AddQuestionForm(FlaskForm):
    text = TextAreaField('Текст вопроса', validators=[DataRequired()], default='')
    answer = StringField('Правильный ответ', validators=[DataRequired()], default='')
    comment = TextAreaField('Комментарии к ответу на вопрос')
    category = SelectField('Категория', validators=[Optional()], choices=[], default='')
    type = SelectField('Тип', validators=[Optional()], choices=[], default='С вариантами')
    complexity = SelectField('Сложность', validators=[Optional()], choices=[], default='Новичок')
    wrong_answer1 = StringField('Неправильные варианты ответа', validators=[DataRequired()])
    wrong_answer2 = StringField('', validators=[DataRequired()])
    wrong_answer3 = StringField('', validators=[DataRequired()])
    submit = SubmitField('Отправить')
