from flask import Flask, redirect, request, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetsForm
import os.path

app = Flask(__name__)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "32m54hwcon49s1kl6"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_pets'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

with app.app_context():
    connect_db(app)
    db.create_all()

debug = DebugToolbarExtension(app)

def dir_last_updated(folder):
    return str(max(os.path.getmtime(os.path.join(root_path, f))
                   for root_path, dirs, files in os.walk(folder)
                   for f in files))
# credit: MarredCheese at https://stackoverflow.com/questions/41144565/flask-does-not-see-change-in-js-file
# is used to automatically update static files without having to hard refresh the browser for every change :D

@app.route("/")
def root():
    pets = Pet.query.all()
    return render_template("home.html", pets=pets, last_updated=dir_last_updated("static"))

@app.route("/add", methods=["GET", "POST"])
def add_pet():
    form = AddPetsForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        available = True if (form.available.data == 'a') else False
        pet = Pet(name=name, species=species, photo_url=url, age=age, notes=notes, available=available)
        db.session.add(pet)
        db.session.commit()
        return redirect("/")
    else:
         return render_template("pet_add.html", form=form, last_updated=dir_last_updated("static"))

@app.route("/<int:id>", methods=["GET", "POST"])
def pet_display(id):
    """Display pet"""
    pet = Pet.query.get_or_404(id)
    form = AddPetsForm(obj=pet)

    if form.validate_on_submit():
        print("hi")
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = True if (form.available.data == 'True') else False
        # db.session.add(pet)
        db.session.commit()
        return redirect("/")
    else:
         return render_template("pet_display.html", form=form, pet=pet, last_updated=dir_last_updated("static"))