from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField, HiddenField
from wtforms.validators import InputRequired, Email, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    login_submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[Email("Invalid Email")])
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

class DesignerForm(FlaskForm):
    username = SelectField(u'Username', choices=[], validators=[InputRequired()])
    designer_submit = SubmitField('Assign Designer')

    def update_choices(self):
        new_choice = []
        designers = User.query.all()
        for u in designers:
            if u.isDesigner is not True:
                label = u.name
                value = u.username
                new_choice.append((value, label))
        self.username.choices = new_choice

class UploadDesign(FlaskForm):
    file = FileField(validators=[InputRequired()])
    blueprint_file = FileField(validators=[InputRequired()])
    file_submit = SubmitField('Upload')


class Approve(FlaskForm):
    id = HiddenField()
    approve_submit = SubmitField('Approve')

class Reject(FlaskForm):
    id = HiddenField()
    reject_submit = SubmitField('Reject')