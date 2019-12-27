from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

relationship_table=db.Table('relationship_table',
                            db.Column('user_name', db.Integer, db.ForeignKey('user.username'), nullable=False),
                            db.Column('designs_id', db.Integer, db.ForeignKey('designs.id'), nullable=False),
                            db.PrimaryKeyConstraint('user_name','designs_id'))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    isDesigner = db.Column(db.Boolean, nullable=True)
    isAdmin = db.Column(db.Boolean, nullable=True)
    designs = db.relationship('Designs', backref='designer', lazy='dynamic')
    voted = db.relationship('Designs', secondary=relationship_table, backref='voter')

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
    user_name = db.Column(db.Integer, db.ForeignKey('user.username'))
    no_of_votes = db.Column(db.Integer, nullable=True, default=0)

    def set_approve(self):
        self.isApproved = True
        self.isRejected = False

    def set_reject(self):
        self.isRejected = True
        self.isApproved = False
