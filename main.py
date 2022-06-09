import werkzeug
from flask import Flask, url_for, render_template, redirect, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from flask_wtf import FlaskForm
from wtforms import BooleanField, FloatField, IntegerField, StringField, SubmitField, URLField
from wtforms.validators import DataRequired, NumberRange, URL
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'djfaklh029854uhjfakf90djfj03hjkj2890'
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


class EditCafe(FlaskForm):
    has_sockets = BooleanField('Does this place have sockets?')
    has_wifi = BooleanField('Does this place have wifi?')
    has_toilet = BooleanField('Does this place have toilets?')
    location = StringField('What is the correct location?')
    submit = SubmitField('Update', validators=[DataRequired()])


class AddCafe(FlaskForm):
    name = StringField('Cafe name:', validators=[DataRequired()])
    location = StringField('What is the location?', validators=[DataRequired()])
    coffee_price = FloatField('What is the price of coffee?', validators=[DataRequired()])
    seats = IntegerField('Number of seats:', validators=[DataRequired()])
    has_sockets = BooleanField('Does this place have sockets?')
    has_wifi = BooleanField('Does this place have wifi?')
    has_toilet = BooleanField('Does this place have toilets?')
    can_take_calls = BooleanField('Can you take calls?')
    map_url = URLField('Google Maps URL:', validators=[DataRequired(), URL()])
    img_url = URLField('Background image URL:', validators=[DataRequired(), URL()])
    submit = SubmitField('Add Cafe', validators=[DataRequired()])


@app.route('/')
def home():
    cafes = db.session.query(Cafe).all()
    return render_template('index.html', cafes=cafes)


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    cafe_id = request.args.get('id')
    current_cafe = Cafe.query.get(cafe_id)
    edit_form = EditCafe()

    if edit_form.validate_on_submit():
        new_location = request.form['location']
        try:
            if request.form['has_sockets']:
                current_cafe.has_sockets = 1
        except werkzeug.exceptions.BadRequestKeyError:
            current_cafe.has_sockets = 0
        try:
            if request.form['has_wifi']:
                current_cafe.has_wifi = 1
        except werkzeug.exceptions.BadRequestKeyError:
            current_cafe.has_wifi = 0
        try:
            if request.form['has_toilet']:
                current_cafe.has_toilet = 1
        except werkzeug.exceptions.BadRequestKeyError:
            current_cafe.has_toilet = 0
        if new_location != '':
            current_cafe.location = new_location
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', form=edit_form, cafe=current_cafe)


@app.route('/delete')
def delete():
    cafe_id = request.args.get('id')
    current_cafe = Cafe.query.get(cafe_id)
    db.session.delete(current_cafe)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/add', methods=['GET', 'POST'])
def add():
    add_form = AddCafe()

    if add_form.validate_on_submit():
        new_cafe = Cafe()
        try:
            if request.form['has_sockets']:
                new_cafe.has_sockets = 1
        except werkzeug.exceptions.BadRequestKeyError:
            new_cafe.has_sockets = 0
        try:
            if request.form['has_wifi']:
                new_cafe.has_wifi = 1
        except werkzeug.exceptions.BadRequestKeyError:
            new_cafe.has_wifi = 0
        try:
            if request.form['has_toilet']:
                new_cafe.has_toilet = 1
        except werkzeug.exceptions.BadRequestKeyError:
            new_cafe.has_toilet = 0
        try:
            if request.form['can_take_calls']:
                new_cafe.has_toilet = 1
        except werkzeug.exceptions.BadRequestKeyError:
            new_cafe.can_take_calls = 0
        new_cafe.name = request.form['name']
        new_cafe.location = request.form['location']
        new_cafe.coffee_price = f"${request.form['coffee_price']}"
        new_cafe.seats = request.form['seats']
        new_cafe.img_url = request.form['img_url']
        new_cafe.map_url = request.form['map_url']
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=add_form)


if __name__ == '__main__':
    app.run(debug=True)
