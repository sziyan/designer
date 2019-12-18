from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128), nullable=True)
    isDesigner = db.Column(db.Boolean, nullable=True)
    isAdmin = db.Column(db.Boolean, nullable=True)
    designs = db.relationship('Designs', backref='designer', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_admin(self):
        self.isAdmin = True

    def set_designer(self):
        self.isDesigner = True

class Designs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    design_path = db.Column(db.String(128), unique=True)
    votes = db.Column(db.Integer,nullable=True)
    isApproved = db.Column(db.Boolean, nullable=True)
    user_name = db.Column(db.Integer, db.ForeignKey('user.username'))

    def toggle_approved(self):
        if self.isApproved:
            self.isApproved = False
        else:
            self.isApproved = True