# from main import app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import time

db = SQLAlchemy(app)

adminUsername = "admin"
adminPassword = "Password3192!"
adminPasswordHash = generate_password_hash(adminPassword)


class Users(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(64), unique=True)
        firstname = db.Column(db.String(64), unique=True)
        surname = db.Column(db.String(64), unique=True)
        password = db.Column(db.String(128), unique=True)
        age = db.Column(db.Integer)
        gender = db.Column(db.String(64), unique=True)
        town = db.Column(db.String(64), unique=True)
        country = db.Column(db.String(64), unique=True)
        postcode = db.Column(db.String(64), unique=True)
        role = db.Column(db.String(64), unique=True)
        status = db.Column(db.String(64), unique=True)
        print("New User done")

        try:
            db.create_all()
            db.session.commit()
        except:
            db.session.commit()

        def set_password(self, password):
            self.password = generate_password_hash(password)

        def check_password(self, password):
            print("Self.password is ")
            print(self.password)
            return check_password_hash(self.password, password)

        def __repr__(self):
            print("returned result")
            return '<Users %r>' % self.email

            db.session.commit()

def defaultadminsetup():
    exists = db.session.query(Users.id).filter_by(email="admin", firstname="admin", surname="admin").scalar() is not \
             None
    print("this is the content of the exists variable" + (str(exists)))

    if exists is not True:
        defaultadmin = Users(email='admin', firstname='admin', surname='admin', password=adminPasswordHash,
                             role='ADMIN', status='active')
        db.session.add(defaultadmin)
        db.session.commit()

time.sleep(5)
defaultadminsetup()