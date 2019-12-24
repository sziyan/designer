from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    isDesigner = db.Column(db.Boolean, nullable=True)
    isAdmin = db.Column(db.Boolean, nullable=True)
    designs = db.relationship('Designs', backref='designer', lazy='dynamic', foreign_keys='designs.user_name')
    designvotes = db.relationship('Designs', backref='voter', lazy='dynamic', foreign_keys='designs.voter')

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
    design_folder = db.Column(db.String(128), unique=True)
    image_path = db.Column(db.String(128), unique=True)
    isApproved = db.Column(db.Boolean, nullable=True)
    isRejected = db.Column(db.Boolean, nullable=True)
    voter = db.Column(db.Integer, db.ForeignKey('user.username'), nullable=True)
    user_name = db.Column(db.Integer, db.ForeignKey('user.username'))

    def set_approve(self):
        self.isApproved = True
        self.isRejected = False

    def set_reject(self):
        self.isRejected = True
        self.isApproved = False
