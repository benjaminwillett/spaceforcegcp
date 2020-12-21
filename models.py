from __main__ import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


class Users(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    firstname = db.Column(db.String(64), unique=True)
    surname = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64), unique=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(64), unique=True)
    town = db.Column(db.String(64), unique=True)
    country = db.Column(db.String(64), unique=True)
    postcode = db.Column(db.String(64), unique=True)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    race = db.Column(db.String(64), unique=True)
    children = db.Column(db.String(64), unique=True)
    official_diag = db.Column(db.String(64), unique=True)
    age_first_hhd = db.Column(db.Integer)
    parent_hhd = db.Column(db.String(64), unique=True)
    number_of_siblings = db.Column(db.Integer)
    number_of_siblings_hhd = db.Column(db.Integer)
    location_hhd = db.Column(db.String(64), unique=True)
    doctor_hhd = db.Column(db.String(64), unique=True)
    dermatologist = db.Column(db.String(64), unique=True)
    medication_tried = db.Column(db.String(64), unique=True)
    medication_working = db.Column(db.String(64), unique=True)
    tea = db.Column(db.String(64), unique=True)
    coffee = db.Column(db.String(64), unique=True)
    botox = db.Column(db.String(64), unique=True)
    magnesium = db.Column(db.String(64), unique=True)
    vitd3 = db.Column(db.String(64), unique=True)
    vitc = db.Column(db.String(64), unique=True)
    vitk = db.Column(db.String(64), unique=True)
    probiotic = db.Column(db.String(64), unique=True)
    area_affected = db.Column(db.String(64), unique=True)
    length_of_breakouts = db.Column(db.Integer)
    redlight = db.Column(db.String(64), unique=True)
    cream = db.Column(db.String(64), unique=True)
    antibiotic = db.Column(db.String(64), unique=True)
    other_medical = db.Column(db.String(64), unique=True)
    role = db.Column(db.String(64), unique=True)
    status = db.Column(db.String(64), unique=True)
    print("New User done")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        print("Self.password is ")
        print(self.password)
        return check_password_hash(self.password, password)

    def __repr__(self):
        print("returned result")
        return '<Users %r>' % self.email
