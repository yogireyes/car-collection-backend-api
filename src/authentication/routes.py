from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from src.forms import UserLoginForm, UserRegistrationForm
from src.models import User, db

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/register', methods = ['GET', 'POST'])
def register_view():
    if current_user.is_authenticated:
        return redirect(url_for("site.profile_view"))
    form = UserRegistrationForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        print(email, password)

        user = User(first_name=first_name, last_name=last_name, email=email, password=password)

        db.session.add(user)
        db.session.commit()

        flash(f'You have successfully created a user account {email}', 'success')
        return redirect(url_for('auth.login_view'))
    return render_template('form.html', form=form,title="Register")



@auth.route('/', methods = ['GET', 'POST'])
def login_view():
    if current_user.is_authenticated:
        return redirect(url_for("site.profile_view"))
    form = UserLoginForm()
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(email,password)

        user = User.query.filter(User.email == email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Successfully logged in!', 'success')
            return redirect(url_for('site.profile_view'))
        else:
            flash('Invalid credentials! Please try again', 'danger')
    return render_template('form.html', form=form,title="Login")


@auth.route('/logout')
@login_required
def logout_view():
    logout_user()
    flash('Successfully logged out!', 'success')
    return redirect(url_for('auth.login_view'))