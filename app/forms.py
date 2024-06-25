from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, FileField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')


class QuestionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5)])
    message = TextAreaField('Message', validators=[DataRequired()])
    image = FileField('Image', render_kw={"accept": "image/jpeg, image/png"})
    submit = SubmitField('Add question')


class AnswerForm(FlaskForm):
    message = TextAreaField('Answer', validators=[DataRequired()])
    image = FileField('Image to add', render_kw={"accept": "image/jpeg, image/png"})
    submit = SubmitField('Add new Answer')


class CommentForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')


class TagForm(FlaskForm):
    new_tag = StringField('New tag', validators=[Optional(), Length(max=20)])
    existing_tag = SelectField('Existing tag', validators=[Optional()])
    submit = SubmitField('Add Tag')


class EditAnswerForm(FlaskForm):
    message = TextAreaField('Edit Answer', validators=[DataRequired()])
    image = FileField('Image', render_kw={"accept": "image/jpeg, image/png"})
    submit = SubmitField('Edit Answer')


class EditQuestionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5)])
    message = TextAreaField('Message', validators=[DataRequired()])
    image = FileField('Image', render_kw={"accept": "image/jpeg, image/png"})
    submit = SubmitField('Edit question')

