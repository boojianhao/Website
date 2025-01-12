from flask import Flask, render_template, request, redirect, url_for
from forms import *
from Users import *
import shelve

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignUp(request.form)
    if request.method == 'POST' and form.validate():
        user_dict = {}
        db = shelve.open('users.db', 'c')
        try:
            if "Users" in db:  # is key exist?
                user_dict = db["Users"]  # retrieve data
            else:
                db["Users"] = user_dict  # start with empty
        except:
            print("Error in opening users.db.")
        new_user = Users(name=form.name.data, email=form.email.data.lower(), password=form.password.data)
        user_dict[f"{new_user.get_email()}"] = new_user
        db["Users"] = user_dict
        db.close()

        return redirect(url_for('login'))

    return render_template("signup.html", form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    form = Login(request.form)
    if request.method == 'POST' and form.validate():
        user_dict = {}
        db = shelve.open('users.db', 'c')
        try:
            if "Users" in db:  # is key exist?
                user_dict = db["Users"]  # retrieve data
            else:
                db["Users"] = user_dict  # start with empty
        except:
            print("Error in opening users.db.")
        db.close()
        if form.email.data in user_dict:
            if form.password.data == user_dict[form.email.data].get_password():
                return redirect(url_for('success'))
            else:
                print('Incorrect password, please try again.')
        else:
            print("There is no such email registered with us.")

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    return redirect(url_for('home'))

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run()