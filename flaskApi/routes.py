from flask import render_template, request, jsonify
from flaskApi import app
from runServer import  indexManager
import face_recognition
import threading
import time
import os




@app.route('/')
@app.route('/home')
def home():
    picture_of_me = face_recognition.load_image_file("pictures/pic1.jpg")
    my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

    unknown_picture = face_recognition.load_image_file("pictures/pic2.jpg")
    unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]



    # Now we can see the two face encodings are of the same person with `compare_faces`!

    results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)

    if results[0] == True:
        print("It's a picture of me!")
    else:
        print("It's not a picture of me!")
    return "toto"



@app.route("/import_picture_page")
def import_picture_page():
    return render_template(
        'import_picture.html'
    )




@app.route('/submit_picture' , methods=['POST'])
def submit_picture():
    picture = request.files['file']
    if 'file' not in request.files:
        return "No file uploaded"

    if 'username' not in request.form:
        return "Need to give username"

    username = request.form['username']
    filename = picture.filename
    splitted = filename.split('.')

    if len(splitted) == 0:
        return "Problem with filename"

    extension = splitted[len(splitted) - 1]

    picture.save("tmp/650" + str(indexManager.index) + '/' + username + '.' + extension)

    indexManager.increaseIndex()
    return "OK"




@app.route('/look_for_sosie')
def look_for_sosie():
    return render_template(
        'look_for_sosie.html'
    )

@app.route("/submit_look_for_sosie", methods=['POST'])
def submit_look_for_sosie():
    username = request.form['username']

    files = os.listdir("pictures/" + username)

    if (len(files) == 0):
        return "error"

    picture_of_me = face_recognition.load_image_file("pictures/" + username + "/" + files[0])
    my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]


    users = os.listdir("pictures")

    if (len(users) == 0):
        return "error users"

    for user in users:
        if not user == username:
            files2 = os.listdir("pictures/" + user)
            if len(files2) > 0:
                unknown_picture = face_recognition.load_image_file("pictures/" + user + '/' + files2[0])
                unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]
                results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)
                if results:
                    return "L'utilisateur " + username + "est sosie avec l'utilisateur " + user + " !"

    return "prout"