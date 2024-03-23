# #Works well rapid API

# from flask import Flask, request, jsonify
# import os
# import requests
# from firebase_admin import credentials, storage, initialize_app
# from deepface import DeepFace
# app = Flask(__name__)
# cred = credentials.Certificate("./credentials.json")
# initialize_app(cred, {'storageBucket': 'protecta-ca1ba.appspot.com'})
# bucket = storage.bucket()

# @app.route('/recognize', methods=['POST'])
# def recognize():
#     try:
#         user_uid = request.json.get('user_uid')
#         user_email = request.json.get('user_email')
#         user_display_name = request.json.get('user_display_name')
#         last_photo_uri = request.json.get('last_photo_uri')
#         login_photo_path = f"userData/{user_uid}/{user_email}/Login/{user_display_name}.jpg"
#         facial_photo_path = f"userData/{user_uid}/{user_email}/Facial/{user_display_name}.jpg"
#         login_photo_blob = bucket.blob(login_photo_path)
#         facial_photo_blob = bucket.blob(facial_photo_path)
#         login_photo_blob.download_to_filename("login_photo.jpg")
#         facial_photo_blob.download_to_filename("facial_photo.jpg")

#         api_url = "https://face-recognition26.p.rapidapi.com/api/face_compare"
#         api_headers = {
#             "X-RapidAPI-Key": "87e18d7938mshac117765358cf43p1a25dajsn087d2f17698e",
#             "X-RapidAPI-Host": "face-recognition26.p.rapidapi.com"
#         }
#         files = {
#             'image1': ('login_photo.jpg', open('login_photo.jpg', 'rb')),
#             'image2': ('facial_photo.jpg', open('facial_photo.jpg', 'rb'))
#         }
#         response = requests.post(api_url, files=files, headers=api_headers)
#         try:
#             response.raise_for_status()
#             result = {"status": "Success", "response_text": response.text}
#         except requests.exceptions.RequestException as e:
#             result = {"status": "Error", "error_message": str(e)}
#         files['image1'][1].close()
#         files['image2'][1].close()
#         print(result)
#         return jsonify(result)

#     except Exception as e:
#         return jsonify({"status": "Error", "error_message": str(e)})

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)


# DeepFace Model
# .venv\Scripts\activate
# python index.py
from flask import Flask, request, jsonify
import os
import requests
from firebase_admin import storage, credentials, initialize_app
from deepface import DeepFace

from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)

cred = credentials.Certificate("./credentials.json")
initialize_app(cred, {'storageBucket': 'protecta-ca1ba.appspot.com'})
bucket = storage.bucket()


@app.route("/")
def helloWorld():
  return "Welcome to ProtecTa Backend!"

@app.route('/face_recognize', methods=['POST'])
def face_recognize():
    try:
        user_uid = request.json.get('user_uid')
        user_email = request.json.get('user_email')
        user_display_name = request.json.get('user_display_name')
        last_photo_uri = request.json.get('last_photo_uri')
        login_photo_path = f"userData/{user_uid}/{user_email}/Login/{user_display_name}.jpg"
        facial_photo_path = f"userData/{user_uid}/{user_email}/Facial/{user_display_name}.jpg"
        login_photo_blob = bucket.blob(login_photo_path)
        facial_photo_blob = bucket.blob(facial_photo_path)
        login_photo_blob.download_to_filename("login_photo.jpg")
        facial_photo_blob.download_to_filename("facial_photo.jpg")
        files = {
            'image1': ('login_photo.jpg', open('login_photo.jpg', 'rb')),
            'image2': ('facial_photo.jpg', open('facial_photo.jpg', 'rb'))
        }

        response = DeepFace.verify("login_photo.jpg","facial_photo.jpg",model_name="Facenet512")
        print(response)
        
        files['image1'][1].close()
        files['image2'][1].close()
        return jsonify(response)
    except Exception as e:
        return jsonify({"status": "Error", "error_message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)