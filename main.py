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
import threading
import os
from flask import Flask
import sys
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import time
from message import grouponmessage


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SkiCity3192!'
app.secret_key = "afeaddsdasdjkhkjhsfkjhsdsdt5453423f32"

app.config['SQLALCHEMY_DATABASE_URI'] = \
     'mysql+pymysql://user:password@db:3306' \
     '/spaceforcedb'
print(app.config)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

time.sleep(10)

db = SQLAlchemy(app)

adminUsername = "admin"
adminPassword = "Password3192!"
adminPasswordHash = generate_password_hash(adminPassword)

basedir = os.path.abspath(os.path.dirname(__file__))
print("basedir is set to " + basedir)
file_dir = os.path.dirname(__file__)
print("file_dir path is " + file_dir)
sys.path.append(file_dir)
print("file_dir path is " + (str(sys.path.append(file_dir))))


class Users(db.Model, UserMixin):
        __tablename__ = 'Users'
        id = db.Column(db.Integer, autoincrement=True, primary_key=True)
        email = db.Column(db.String(64), unique=True, nullable=False)
        firstname = db.Column(db.String(64), unique=False, nullable=False)
        surname = db.Column(db.String(64), unique=False, nullable=False)
        password = db.Column(db.String(128), unique=False, nullable=False)
        age = db.Column(db.String(3), unique=False, nullable=False)
        gender = db.Column(db.String(64), unique=False)
        town = db.Column(db.String(64), unique=False)
        country = db.Column(db.String(64), unique=False)
        postcode = db.Column(db.String(64), unique=False)
        role = db.Column(db.String(64), unique=False, nullable=False)
        status = db.Column(db.String(64), unique=False, nullable=False)
        sent_welcome_email = db.Column(db.String(64), unique=False, nullable=False)

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


def buildtable():
    try:
        print("trying to create table")
        db.create_all()
        db.session.commit()
        print("committed DB")
    except:
        db.session.commit()
        print("Could not create table")

buildtable()

def defaultadminsetup():
    exists = db.session.query(Users.id).filter_by(email="admin", firstname="admin", surname="admin").scalar() is not \
             None
    print("this is the content of the exists variable" + (str(exists)))

    try:
        if exists is not True:
            defaultadmin = Users(email='admin', firstname='admin', surname='admin', password=adminPasswordHash,
                             role='ADMIN', status='active', age='0', postcode="3192", gender='male', town='weymouth',
                             country='uk' )
            db.session.add(defaultadmin)
            print("Created DB Admin User")
            db.session.commit()
            print("Committed DB Admin User")

        else:
            print("Admin user exists in the database")
    except:
        pass

defaultadminsetup()

print("loading global variables!!")
time.sleep(1)


print("********************************************************")
print("********************************************************")
print("**                  SpaceForce                        **")
print("**  ************************************************  **")
print("**  ************************************************  **")
print("**  ************************************************  **")
print("**          Created by benw@techcamp.com.au           **")
print("********************************************************")
print("********************************************************")

time.sleep(1)

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'SkiCity3192!'
# app.secret_key = "afeaddsdasdjkhkjhsfkjhsdsdt5453423f32"
#
#
# basedir = os.path.abspath(os.path.dirname(__file__))
# print("basedir is set to " + basedir)
# file_dir = os.path.dirname(__file__)
# print("file_dir path is " + file_dir)
# sys.path.append(file_dir)
# print("file_dir path is " + (str(sys.path.append(file_dir))))


#  app.config['SQLALCHEMY_DATABASE_URI'] = \
#     'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# app.config['SQLALCHEMY_DATABASE_URI'] = \
#     'mysql+pymysql://admin:Mysql3192!@35.244.124.207/spaceforcetestdb'
# print(app.config)
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# from models import db
# from models import Users
time.sleep(5)

print("Session committed")

manager = Manager(app)
lm = LoginManager(app)

csrf = CsrfProtect()
csrf.init_app(app)


class LoginForm(FlaskForm):
    email = StringField('username', validators=[InputRequired(), Length(min=5, max=64)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=0, max=64)])
    loginerror = None
    print("LoginForm received Username & Password into variables")

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        user = Users.query.filter_by(email=self.email.data).first()

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
    loginerror = None
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    form = LoginForm()
    return render_template('index_two3.html', loginerror=loginerror, form=form)


@csrf.exempt
@app.route('/login', methods=['GET', 'POST'])
def login():
    global db
    loginerror = None
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
        print("%s is attempting to login" % form.email.data)
        exists = bool(Users.query.filter_by(email=form.email.data).first())

        if exists is False:
            print('Invalid Username')
            loginerror = "Unknown account"
            return render_template('index_two3.html', loginerror=loginerror, form=form)

        elif user.status == "inactive":
            print("%s is an INACTIVE ACCOUNT" % user.email)
            loginerror = ("%s is an INACTIVE ACCOUNT" % user.email)
            return render_template('index_two3.html', loginerror=loginerror, form=form)

        else:
            login_user(user)

            if user.email == form.email.data:
                if user.sent_welcome_email != "SENT":
                    mailsetup = grouponmessage(sender_email="ben.willett@distortenterprises.com",
                                               receiver_email=user.email)
                    user.sent_welcome_email = "SENT"
                    db.session.flush()
                    db.session.commit()

            else:
                pass

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
    role = "CUSTOMER"
    status = "active"
    print("Form variables populated")

    u = Users(email=email, firstname=firstName, surname=surname, password=password, age=age, gender=gender, town=town,
              country=country, postcode=postcode, role=role, status=status)

    u.set_password(password)
    print("Inserting the following into Database Table " + (str(u)))
    try:
        db.session.add(u)
        db.session.flush()
        db.session.commit()
        return redirect('/admin')
    except:
        print("Can't add a duplicate username")
        flash("Please choose another username")
        return render_template('adduser.html', USERNAME=current_user)

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
        role = request.form['ROLE']
        enabledstate = request.form['ENABLEDSTATE']

        print(username)
        print(password)
        print(town)
        print(country)
        print(postcode)
        print(role)
        print(enabledstate)
        print("user update")

        for each in p:
            if each.email == username:
                if each.password != password:
                    print(each.email + "didn't have a password match when updating so generating new password hash!!")
                    each.set_password(password)
                    print("New hash has been added to password database for user" + each.email)
                    each.town = town
                    each.country = country
                    each.postcode = postcode
                    each.role = role
                    each.status = enabledstate
                    print((str(each)) + " = Status " + (str(each.status)))

                    db.session.commit()
                    return redirect('/admin')
                else:
                    print(each.email + "had a successful password match when updating so no new password generated!!")
                    each.town = town
                    each.country = country
                    each.postcode = postcode
                    each.role = role
                    each.status = enabledstate
                    print((str(each)) + " = Status " + (str(each.status)))

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

    age_count = db.session.query(Users.age, db.func.count()).group_by(Users.age).all()

    for age, count in age_count:
        print(age, count)

    return render_template("stats.html", USERS=p, USERNAME=current_user, RECORDCOUNT=recordcount,
                           GENDER_COUNT=gender_count, AGE_COUNT=age_count,
                           COUNTRY_COUNT=country_count)


@app.route('/uservalue', methods=['GET', 'POST'])
def uservalue():
    exists = bool(Users.query.filter_by(email="ghfgf@werds.com").first())
    print(exists)
    return "value of exists is: " + str(exists)

if __name__ == '__main__':
    manager.run()
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', debug=True, port=port)
