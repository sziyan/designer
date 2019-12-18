from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, DecimalField, SubmitField, SelectField, FloatField
from wtforms.validators import InputRequired,Optional
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    login_submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    name = StringField('Name', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    password2 = PasswordField('Enter password again', validators=[InputRequired()])
    register_submit = SubmitField('Register')

class AdminForm(FlaskForm):
    username = SelectField(u'Username', choices=[], validators=[InputRequired()])
    admin_submit = SubmitField('Add Admin')

    def update_choices(self):
        new_choice = []
        all_users = User.query.all()
        for u in all_users:
            if u.isAdmin is not True:
                label = u.name
                value = u.username
                new_choice.append((value, label))
        self.username.choices = new_choice