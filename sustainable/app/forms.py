from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, SelectField
from wtforms.validators import DataRequired, Optional


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")


class SearchBar(FlaskForm):
    search = StringField("Search")
    go = SubmitField("Search")
    filter = SelectField(
        'Filter By',
        choices=[('p', 'Price: low to high'), ('b', 'Brand: Alphabetical'), ('r', 'Rating: high to low')],  validators=[Optional()]
    )


class ForgetPasswordForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired()])
    submit = SubmitField("Send email")

class ReportForm(FlaskForm):
    reason = StringField("Brief Reason", validators=[DataRequired()])
    submit = SubmitField("Send Report")

class SuggestForm(FlaskForm):
    name = StringField("Name of Company", validators=[DataRequired()])
    reason = StringField("Brief Reason", validators=[DataRequired()])
    url = StringField("url", validators=[DataRequired()])
    submit = SubmitField("Send Report")


class ConfirmForm(FlaskForm):
    keyword = StringField("Confirmation Word", validators=[DataRequired()])
    submit = SubmitField("I want to delete!")