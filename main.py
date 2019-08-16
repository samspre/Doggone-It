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
from lostdog.lostdog import findLostDog
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
dog_temp =[{'image': 'http://g.petango.com/photos/2276/5179a7d4-5031-423d-a828-ff280663db71_TN2.jpg', 'name': 'Bella', 'distance': '140', 'gender': 'Female', 'breed': 'Chinese Crested / Terrier', 'link': 'https://www.petango.com/LostFound/Dog-Chinese-Crested-39485957'}, {'image': 'http://g.petango.com/photos/2276/239d98be-8acb-4b60-bdb1-c11b0b24991d_TN2.jpg', 'name': 'Roosevelt', 'distance': '140', 'gender': 'Male', 'breed': 'Terrier / Mix', 'link': 'https://www.petango.com/LostFound/Dog-Terrier-42209881'}, {'image': 'http://g.petango.com/photos/2495/d3a78349-c20b-4c4a-9974-ac5ad08c4ab8_TN2.jpg', 'name': 'Pandora- adoption pending', 'distance': '151', 'gender': 'Female', 'breed': 'Terrier / Mix', 'link': 'https://www.petango.com/LostFound/Dog-Terrier-30333868'}, {'image': 'http://g.petango.com/photos/2495/39dff880-a9d4-41bb-9f8e-d1264675d2d3_TN2.jpg', 'name': 'Raul Wally', 'distance': '156', 'gender': 'Male', 'breed': 'Boxer / Terrier', 'link': 'https://www.petango.com/LostFound/Dog-Boxer-40611568'}, {'image': 'http://g.petango.com/photos/3223/bde773bb-bb96-4e38-8573-264af8aea41c_TN2.jpg', 'name': 'Champ', 'distance': '179', 'gender': 'Male', 'breed': 'Terrier / Mix', 'link': 'https://www.petango.com/LostFound/Dog-Terrier-40022450'}, {'image': 'http://g.petango.com/photos/2137/ddf01112-78f5-4502-98f9-b97580c797b1_TN2.jpg', 'name': 'Max', 'distance': '191', 'gender': 'Male', 'breed': 'Terrier / Boxer', 'link': 'https://www.petango.com/LostFound/Dog-Terrier-42325370'}, {'image': 'http://g.petango.com/photos/1309/4f10d7e0-f9b9-44b4-9ad8-010b4951454e_TN2.jpg', 'name': 'Crepe', 'distance': '203', 'gender': 'Male', 'breed': 'Terrier / Mix', 'link': 'https://www.petango.com/LostFound/Dog-Terrier-41866349'}, {'image': 'http://g.petango.com/photos/624/ce374281-8bec-49cf-ae38-97445f99d254_TN2.jpg', 'name': 'Champ', 'distance': '204', 'gender': 'Male', 'breed': 'Terrier / Mix', 'link': 'https://www.petango.com/LostFound/Dog-Terrier-41888781'}, {'image': 'http://g.petango.com/photos/1309/54682393-ad92-475f-939f-4bd9b22624ac_TN2.jpg', 'name': 'Blenca', 'distance': '206', 'gender': 'Female', 'breed': 'Terrier / Mix', 'link': 'https://www.petango.com/LostFound/Dog-Terrier-41706640'}, {'image': 'http://g.petango.com/photos/1309/7a75333b-3ff8-495c-94c6-27916ad8670e_TN2.jpg', 'name': 'Nika', 'distance': '209', 'gender': 'Female', 'breed': 'Terrier / Mix', 'link': 'https://www.petango.com/LostFound/Dog-Terrier-42194407'}, {'image': 'http://g.petango.com/photos/1309/eb9e7809-bfa0-47f4-b658-ceeffaf850cb_TN2.jpg', 'name': 'Peppy', 'distance': '211', 'gender': 'Male', 'breed': 'Terrier / Mix', 'link': 'https://www.petango.com/LostFound/Dog-Terrier-42361721'}, {'image': 'http://g.petango.com/photos/1833/994fb7dc-a0b4-4f64-b47d-2546832ba210_TN2.jpg', 'name': 'Ana', 'distance': '212', 'gender': 'Female', 'breed': 'Terrier / Mix', 'link': 'https://www.petango.com/LostFound/Dog-Terrier-39851984'}, {'image': 'http://g.petango.com/photos/490/d08865d1-2c93-4f19-aef3-13f6450766a5_TN2.jpg', 'name': 'Ace', 'distance': '319', 'gender': 'Male', 'breed': 'Terrier / Mix', 'link': 'https://www.petango.com/LostFound/Dog-Terrier-42085773'}, {'image': 'http://g.petango.com/photos/490/9300dd32-0c0c-432c-af74-20d9fb11a10d_TN2.jpg', 'name': 'King Kong', 'distance': '321', 'gender': 'Male', 'breed': 'Terrier / Mix', 'link': 'https://www.petango.com/LostFound/Dog-Terrier-42390124'}, {'image': 'http://g.petango.com/photos/2657/ba25b1a3-2c04-4ae3-9ee4-262eb35c5679_TN2.jpg', 'name': 'Jojo', 'distance': '330', 'gender': 'Male', 'breed': 'Terrier / Mix', 'link': 'https://www.petango.com/LostFound/Dog-Terrier-42266261'}, {'image': 'http://g.petango.com/photos/2657/8ec03337-a095-403a-ad09-341b3bc38a49_TN2.jpg', 'name': 'Morgan', 'distance': '333', 'gender': 'Male', 'breed': 'Terrier / Mix', 'link': 'https://www.petango.com/LostFound/Dog-Terrier-40084598'}]

def get_zip(results):
    for i in range(len(results)):
        if "postal_code" in results[i]['types']:
            return results[i]["long_name"] 

@app.route('/getlostdog', methods=["GET"])
def lostdog():
    breed = request.args.get("breed")
    zipcode = request.args.get("zipcode")
    results = findLostDog(breed, zipcode)
    return results.json()

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
    #print(zipcode, file=sys.stderr)
    image_path = request.args['image_path']
    results = session['results']
    dogs_list = findLostDog(results[0][0], zipcode)
    #print(results, file=sys.stderr)
    return render_template('results.html', image_path=image_path, dogs_list= dogs_list, results=results, form=form, zipcode=zipcode, breed=results[0][0])

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
        session['results'] = result
        return redirect(url_for('results', image_path=image_path_flask)) #redirects the user to a "results" page (currently nothings in it)
    elif request.method == "POST":
        response = request.json
        #print(response, file=sys.stderr)
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