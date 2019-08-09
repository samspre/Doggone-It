import os
import sys
import jinja2
from flask import Flask, render_template, redirect, session, request, flash, url_for, jsonify
import logging
from forms.dogImage import DogImage 
from werkzeug.utils import secure_filename
from PIL import Image

UPLOAD_FOLDER = 'static/images/image_input'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
dir_path = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__, instance_path=dir_path)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

"""
function eval_image takes the user inputted image and reads it utilizing the PIL module
image_path leads to the static/images/image_input folder in the flask app directory 
Note: in order to print items in flask, you need to flush the buffer, or redirect the file via sys.stderr instead of stdout
    usage: print(<message>, file=sys.stderr)
"""
def eval_image(image_path):
    im = Image.open(image_path)
    #im.show()
    print("not implemented yet")

@app.route('/results', methods = ["GET"]) #results page endpoint
def results():
    image_path = request.args['image_path']
    results = session['results']
    print(results, file=sys.stderr)
    return render_template('results.html', image_path=image_path, results=results)

@app.route('/', methods = ["GET", "POST"]) #initial homepage
def home():
    form = DogImage()
    if  request.method == "POST" and form.validate_on_submit(): #reads from the frontend the form image
        image = form.image.data
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.instance_path, app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path) #saves image to specified image path
        eval_image(image)
        image_path_flask = "images/image_input/" + image.filename
        ##hardcoded results
        result = [{'Deer': 90}, {'Bear': 5}, {'Tiger': 1}, {"Lion": 1}]
        session['results'] = result
        print(result, file=sys.stderr)
        return redirect(url_for('results', image_path=image_path_flask)) #redirects the user to a "results" page (currently nothings in it)
    return render_template("home.html", form=form)

if __name__ == '__main__':
    app.secret_key = 'secret1234'
    TEMPLATES_AUTO_RELOAD = True
    app.run(debug=True)