import os
import sys
import jinja2
from flask import Flask, render_template, redirect, session, request, flash, url_for, jsonify
import logging
from forms.dogImage import DogImage 
from werkzeug.utils import secure_filename
from PIL import Image
import time
from AI.predict_image import predict_image 
import requests

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

def get_zip(results):
    for i in range(len(results)):
        if "postal_code" in results[i]['types']:
            return results[i]["long_name"] 

@app.route('/results', methods = ["GET", "POST"]) #results page endpoint
def results():
    form = DogImage()
    if  request.method == "POST": #reads from the frontend the form image
        image = form.image.data
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.instance_path, app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path) #saves image to specified image path
        result = predict_image(image_path)
        print(result, file=sys.stderr)
        image_path_flask = "images/image_input/" + image.filename
        ##hardcoded results
        session['results'] = [result]
        print(result, file=sys.stderr)
        return redirect(url_for('results', image_path=image_path_flask)) #redirects the user to a "results" page (currently nothings in it)
    URL = 'https://maps.googleapis.com/maps/api/geocode/json'
    api_key = 'AIzaSyCxVNtO3XUfCPFlc4k0PK1r-VqKhimq8as'
    latlng = str(session['latitude']) + "," + str(session['longitude'])
    PARAMS = {'latlng' : latlng, 'key' : api_key}
    r = requests.get(url = URL, params = PARAMS)
    data = r.json()['results'][0]["address_components"]
    zipcode = get_zip(data)
    print(zipcode, file=sys.stderr)
    image_path = request.args['image_path']
    results = session['results']
    print(results, file=sys.stderr)
    petfinder_URL = "https://www.petfinder.com/search/dogs-for-adoption/us/ny/12180/?breed%5B0%5D=Airedale+Terrier"
    return render_template('results.html', image_path=image_path, results=results, form=form)

#'https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452&key=AIzaSyCxVNtO3XUfCPFlc4k0PK1r-VqKhimq8as'
@app.route('/', methods = ["GET", "POST"]) #initial homepage
def home():
    form = DogImage()
    if  request.method == "POST" and form.validate_on_submit(): #reads from the frontend the form image
        image = form.image.data
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.instance_path, app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path) #saves image to specified image path
        result = predict_image(image_path)
        image_path_flask = "images/image_input/" + image.filename
        ##hardcoded results
        session['results'] = [result]
        print(result, file=sys.stderr)
        return redirect(url_for('results', image_path=image_path_flask)) #redirects the user to a "results" page (currently nothings in it)
    elif request.method == "POST":
        response = request.json
        print(response, file=sys.stderr)
        longitude = response['longitude']
        latitude = response['latitude']
        session['longitude'] = longitude
        session['latitude'] = latitude 
        return '', 204
    else:
        return render_template("home.html", form=form)

if __name__ == '__main__':
    app.secret_key = 'secret1234'
    TEMPLATES_AUTO_RELOAD = True
    app.run(debug=True)