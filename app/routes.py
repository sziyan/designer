from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, login_required, logout_user
from app import app, db
from app.forms import LoginForm, RegisterForm, AdminForm, DesignerForm, UploadDesign
from app.models import User, Designs
import os

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/designs/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if form.register_submit.data and form.validate():
        print(form.errors)
        user = User.query.filter_by(username=form.username.data).first()
        if user is None: #user does not exist
            if form.password.data == form.password2.data: #password matches
                new_user = User(username=form.username.data, name=form.name.data, email=form.email.data)
                new_user.set_password(form.password.data)
                db.session.add(new_user)
                db.session.commit()
                flash('Account created successfully. Kindly login now.', 'success')
                return redirect(url_for('login'))
            else: #user does  not exist but password does not match
                flash('Password does not match', 'danger')
                return redirect(url_for('register'))
        else: #user exist
            flash('Account already exists', 'danger')
            return redirect(url_for('register'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.login_submit.data and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('Account does not exist', 'danger')
            return redirect(url_for('login'))
        else:
            if user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('Incorrect password', 'danger')
                return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin', methods=['POST', 'GET'])
@login_required
def admin():
    if current_user.isAdmin is not True:
        return redirect(url_for('index'))
    else:
        admin_form = AdminForm()
        admin_form.update_choices()
        designer_form = DesignerForm()
        designer_form.update_choices()
        if admin_form.admin_submit.data and admin_form.validate():
            user = User.query.filter_by(username=admin_form.username.data).first()
            if user is not None:
                user.set_admin()
                db.session.commit()
                flash("User appointed as admin", 'success')
                return redirect(url_for('admin'))
            else:
                flash("User does not exist", 'danger')
                return redirect(url_for('admin'))
        if designer_form.designer_submit.data and designer_form.validate():
            user = User.query.filter_by(username=designer_form.username.data).first()
            if user is not None:
                user.set_designer()
                db.session.commit()
                flash("User approved as designer.", "success")
                return redirect(url_for('admin'))
            else:
                flash("User does not exist.", "danger")
        return render_template('admin.html', admin_form=admin_form, designer_form=designer_form)

@app.route('/designer', methods=['POST', 'GET'])
@login_required
def designer():
    if current_user.isDesigner is not True:
        return redirect(url_for('index'))
    else:
        form = UploadDesign()
        return render_template('designer.html', form=form)

@app.errorhandler(404)
def error404(e):
    return render_template('404.html')