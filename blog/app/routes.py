# The Data Tool created December 11, 2019
# @author Nicholas Grokhowsky
# 
# This tool is a web application that can be used locally or distributed on a public site.  The application can be used 
# to wrangle and query data, in addition to exploratory analysis.  Eventually predictive analysis will be built into
# this program.

#from __init__ import app, models
from app import app, db
from app.forms import LoginForm

from flask import Flask, render_template, flash, redirect, url_for, request 
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app.forms import RegistrationForm
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')

		if not next_page or url_parse(next_page).netloc != '':
				next_page = url_for('index')

		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations!  You are now registered.')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

if __name__ == '__main__':
	app.run()