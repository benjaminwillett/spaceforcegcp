#!/usr/bin/env python

# Trying to add to Github
# This application is a UAT testing dashboard for managing communications with Testers via sms and email.
# To use this an SMS service is required.
# Import contacts from contacts spreadsheet
from flask import request, render_template, redirect, session, flash, url_for
from flask_login import LoginManager, login_user, current_user, UserMixin, logout_user, login_required
from flask_script import Manager
from flask_wtf import FlaskForm
from flask_wtf.csrf import CsrfProtect
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, InputRequired
import time
import threading
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash

print("loading global variables!!")
time.sleep(1)


print("********************************************************")
print("********************************************************")
print("**        Rare Disease Data Capture tool              **")
print("**  ************************************************  **")
print("**  ************************************************  **")
print("**  ************************************************  **")
print("**          Created by benw@techcamp.com.au           **")
print("********************************************************")
print("********************************************************")

time.sleep(1)

app = Flask(__name__)
manager = Manager(app)
lm = LoginManager(app)

csrf = CsrfProtect()
csrf.init_app(app)

app.config['SECRET_KEY'] = 'SkiCity3192!'
app.secret_key = "afeaddsdasdjkhkjhsfkjhsdsdt5453423f32"


basedir = os.path.abspath(os.path.dirname(__file__))
print("basedir is set to " + basedir)

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
print(app.config)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True


db = SQLAlchemy(app)

print("Session committed")


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


class LoginForm(FlaskForm):
    email = StringField('username', validators=[InputRequired(), Length(min=0, max=20)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=0, max=20)])
    print("LoginForm received Username & Password into variables")

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        user = Users.query.filter_by(email=self.email.data).first()
        if user is None:
            self.email.errors.append('Unknown username')
            return False

        print("This is the user ")
        print(user.email)
        print("This is the user.password ")
        print(user.password)

        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        session['USERNAME'] = self.email

        self.user = user
        return True

y = dict()

credentialsP = "null"
credentialsU = "null"
error = ""

exitFlag = 0


class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting " + self.name)
        print("Exiting " + self.name)


@lm.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@csrf.exempt
@app.route('/', methods=['GET', 'POST'])
def default():
    global error
    error = ""
    form = LoginForm()
    return render_template('index_two3.html', ERROR=error, form=form)


@csrf.exempt
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    form = LoginForm()
    print(form.errors)
    print("form object worked")

    if form.is_submitted():
        print("Submitted")

    if form.validate():
        print("Valid")

    print(form.errors)

    if form.validate_on_submit():
        print("validate_on_submit activated")
        user = Users.query.filter_by(email=form.email.data).first()
        print("%s is attempting to login" % user.email)

        if user is None:
            flash('Invalid Username or Password')
            return redirect(url_for('login'))

        if user.status == "inactive":
            print("%s is an INACTIVE ACCOUNT" % user.email)
            redirect(url_for('default'))
        else:
            login_user(user)
            flash('You are now logged in!')
            return redirect(url_for('admin'))

    return redirect(url_for('default'))


@csrf.exempt
@app.route('/logout', methods=['GET','POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        session.pop('USERNAME', None)
        return redirect(url_for('default'))


@csrf.exempt
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if current_user.is_authenticated:
        global db
        print("/admin")
        p = Users.query.order_by(Users.email).all()
        recordcount = db.session.query(Users.email).count()
        print(current_user)
        return render_template('admin.html', USERS=p, RECORDCOUNT=recordcount)

    else:
        return redirect(url_for('default'))


@csrf.exempt
@app.route('/adminsearch', methods=['GET', 'POST'])
def adminsearch():
    if current_user.is_authenticated:
        global db
        print("adminsearch")
        search = request.form["USERSEARCH"]
        print(search)
        q = Users.query.all()

        if search == "Search":
            p = Users.query.order_by(Users.email).all()
        else:
            p = Users.query.filter(Users.email.contains(search))

        recordcount = db.session.query(Users.email).count()

        return render_template('admin.html', USERS=p, RECORDCOUNT=recordcount)

    else:
        return redirect(url_for('default'))


@csrf.exempt
@app.route('/adduser', methods=['GET', 'POST'])
def addUser():
    if current_user.is_authenticated:
        return render_template('adduser.html', USERNAME=current_user)

    else:
        return redirect(url_for('default'))


@csrf.exempt
@app.route('/deleteadmin', methods=['GET', 'POST'])
def deleteadmin():
    if current_user.is_authenticated:
        global db
        x = False
        p = Users.query.all()
        print(request.method)
        deleterow = request.form["DELETE"]
        print("deleterow = ")
        print(deleterow)

        while x == False:
            print("at start of while loop")
            for each in p:
                print('Each is ')
                print(each)
                if deleterow in each.email:
                    db.session.delete(each)
                    print("tried to delete")
                    x = True
                    return redirect('/admin')

                else:
                    print("else pass")
                    pass

            print("admin")

        return redirect('/')

    else:
        return redirect(url_for('default'))


@csrf.exempt
@app.route('/userupdate', methods=['GET', 'POST'])
def editadmin():
    if current_user.is_authenticated:
        global db
        x = False
        p = Users.query.all()
        print(request.method)
        editrow = request.form['EDIT']
        print("Editrow = ")
        print(editrow)

        while x == False:
            print("at start of while loop")
            for each in p:
                print('Each is ')
                print(each)
                if editrow in each.email:
                    print("tried to edit")
                    x = True
                    return render_template('/userupdate.html', USEREDIT=each, USERNAME=current_user)

            else:
                print("else pass")
                pass

    else:
        redirect(url_for("default"))


@csrf.exempt
@app.route('/submituser', methods=['GET', 'POST'])
def submituser():
    print("submituser URL has been routed to")
    global db
    global error
    print("Global variables have been loaded")
    error = ""
    email = request.form['EMAIL']
    firstName = request.form['FIRSTNAME']
    surname = request.form['SURNAME']
    password = request.form['PASSWORD']
    age = request.form['AGE']
    gender = request.form['GENDER']
    town = request.form['TOWN']
    country = request.form['COUNTRY']
    postcode = request.form['POSTCODE']
    height = request.form['HEIGHT']
    weight = request.form['WEIGHT']
    role = "USER"
    status = "inactive"
    print("Form variables populated")

    u = Users(email=email, firstname=firstName, surname=surname, password=password, age=age, gender=gender, town=town,
              country=country, postcode=postcode, height=height, weight=weight, role=role, status=status)
    #           , race=race, children=children, official_diag=diagnosed, age_first_hhd=agestarted,
    #           parent_hhd=parentshhd, number_of_siblings=numbersiblings,
    #           number_of_siblings_hhd=siblingswithhhd, location_hhd=hhdlocation, doctor_hhd=doctor,
    #           dermatologist=dermo, medication_tried=medicationtried, medication_working=medicationworking,
    #           tea=tea, coffee=coffee, botox=botox, magnesium=magnesium,
    #           vitd3=vitd3, vitc=vitc, vitk=vitk, probiotic=probiotic, area_affected=area,
    #           length_of_breakouts=length,
    #           redlight=red,
    #           cream=cream, antibiotic=antibiotic, other_medical=othermed)

    u.set_password(password)

    db.session.add(u)

    db.session.commit()

    return redirect(url_for("default"))


@csrf.exempt
@app.route('/update', methods=['GET', 'POST'])
def update():
    if current_user.is_authenticated:
        global db
        x = False
        p = Users.query.all()
        print(request.method)
        username = request.form['USERNAME']
        password = request.form['PASSWORD']
        town = request.form['TOWN']
        country = request.form['COUNTRY']
        postcode = request.form['POSTCODE']


        print(username)
        print(password)
        print(town)
        print(country)
        print(postcode)
        print("user update")

        for each in p:
            if each.email == username:
                each.password = password
                each.town = town
                each.country = country
                each.postcode = postcode

                hash = generate_password_hash(each.password)
                print(hash)
                each.password = hash
                db.session.commit()
                return redirect('/admin')
            else:
                pass

        return redirect('/')

    else:
        return redirect(url_for('default'))


@csrf.exempt
@app.route('/stats', methods=['GET', 'POST'])
def stats():
    global db
    x = False
    p = Users.query.all()

    recordcount = db.session.query(Users.email).count()

    gender_count = db.session.query(Users.gender, db.func.count()).group_by(Users.gender).all()

    for gender, count in gender_count:
        print(gender, count)

    country_count = db.session.query(Users.country, db.func.count()).group_by(Users.country).all()

    for country, count in country_count:
        print(country, count)

    height_count = db.session.query(Users.height, db.func.count()).group_by(Users.height).all()

    for height, count in height_count:
        print(height, count)

    age_count = db.session.query(Users.age, db.func.count()).group_by(Users.age).all()

    for age, count in age_count:
        print(age, count)

    weight_count = db.session.query(Users.weight, db.func.count()).group_by(Users.weight).all()

    for weight, count in weight_count:
        print(weight, count)

    return render_template("stats.html", USERS=p, USERNAME=current_user, RECORDCOUNT=recordcount,
                           GENDER_COUNT=gender_count, HEIGHT_COUNT=height_count, AGE_COUNT=age_count,
                           WEIGHT_COUNT=weight_count,
                           COUNTRY_COUNT=country_count)


if __name__ == '__main__':
    manager.run()
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', debug=True, port=port)
