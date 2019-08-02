import os
import jinja2
from flask import Flask, render_template, redirect, session, request
#from models.Setting import Setting
import logging
from forms.dogImage import DogImage 

current_directory = jinja2.Environment(loader=jinja2.FileSystemLoader(
os.path.dirname(__file__)), extensions=['jinja2.ext.autoescape'], autoescape=True)
app = Flask(__name__)



@app.route('/', methods = ["GET"])
def home():
    dog_image = DogImage(request.form)
    #print(assets.url)
    # return redirect("/login", code=302)
    #logging.info("testingadjfladjflkdsajfiefjalsfslkfjeaifjealfekajfakdsfijewaf")
    return render_template("home.html", form=dog_image)

if __name__ == '__main__':
    app.secret_key = 'secret1234'
    TEMPLATES_AUTO_RELOAD = True
    app.run(debug=True)