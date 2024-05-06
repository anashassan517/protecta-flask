#Works well rapid API

# from flask import Flask, request, jsonify
# import os
# import requests
# from firebase_admin import credentials, storage, initialize_app
# import base64
# from PIL import Image
# from io import BytesIO
# import sys
# import subprocess
# # from deepface import DeepFace

# from flask_cors import CORS  # Import CORS from flask_cors

# app = Flask(__name__)
# cors=CORS(app)



# @app.route('/save-signature', methods=['POST']) 
# def save_signature():
#     try:
#         signature = request.json.get('signature')
#         # print("Signature python data api:", signature)

#         encoded_data = signature.split(',')[1]
        
#         # Decode base64 string to binary data
#         binary_data = base64.b64decode(encoded_data)
        
#         # Write binary data to file as image
#         with open('signatureb64.png', 'wb') as f:
#             f.write(binary_data)
        
#         # Optionally, you can open the image using PIL to perform further processing
#         img = Image.open(BytesIO(binary_data))
#         img.show()  # Show the image
        
        
#         return jsonify({"status": "Success"})
#     except Exception as e:
#         return jsonify({"status": "Error", "error_message": str(e)})


# @app.route('/recognize', methods=['POST'])
# def recognize():
#     try:
#         cred = credentials.Certificate("./credentials.json")
#         initialize_app(cred, {'storageBucket': 'protecta-ca1ba.appspot.com'})
#         bucket = storage.bucket()
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


# @app.route('/restart')
# def restart():
#     subprocess.call(['kill', '1'])
#     subprocess.call([sys.executable] + sys.argv)
#     return 'Server is restarting...'

    

# if __name__ == '_main_':
#     app.run(host='0.0.0.0', port=5000,use_reloader=True)


# DeepFace Model
# .venv\Scripts\activate
# python index.py
from flask import Flask, request, jsonify
import os
import requests
from firebase_admin import storage, credentials, initialize_app
from deepface import DeepFace as Facial_model
import base64
from PIL import Image
from io import BytesIO
import sys
import subprocess
import cv2
import numpy as np
from flask_cors import CORS, cross_origin



app = Flask(__name__)
cors = CORS(app)

cred = credentials.Certificate("./credentials.json")
initialize_app(cred, {'storageBucket': 'protecta-ca1ba.appspot.com'})
bucket = storage.bucket()


@app.route("/")
def helloWorld():
  return "Welcome to ProtecTa Backend!"

@app.route('/signature-register', methods=['POST']) 
def save_signature():
    try:
        signatures = request.json.get('signatures')
        # print("Signatures python data api:", signatures)

        for i, signature in enumerate(signatures):
            encoded_data = signature.split(',')[1]
            binary_data = base64.b64decode(encoded_data)
            with open(f'signature{i+1}.png', 'wb') as f:
                f.write(binary_data)
            
            img = Image.open(BytesIO(binary_data))
            input_image_path = f'signature{i+1}.png'
            output_image_path = f'signature{i+1}.jpg'
            result_image = add_white_background(input_image_path, output_image_path)
            print(f"Image {i+1} with white background added and saved successfully.")

        return jsonify({"status": "Success"})
    except Exception as e:
        return jsonify({"status": "Error", "error_message": str(e)})


def add_white_background(foreground_image_path, output_image_path):
    foreground_image = cv2.imread(foreground_image_path, cv2.IMREAD_UNCHANGED)

    has_alpha = foreground_image.shape[-1] == 4 

    foreground_height, foreground_width, channels = foreground_image.shape

    background_image = np.ones((foreground_height, foreground_width, 3), dtype="uint8")
    background_image[:] = 255

    if has_alpha:
        mask = 255 - foreground_image[:, :, 3]
        final_image = cv2.bitwise_or(background_image, background_image, mask=mask)
    else:
        final_image = foreground_image

    cv2.imwrite(output_image_path, final_image)



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

        response = Facial_model.verify("login_photo.jpg","facial_photo.jpg",model_name="Facenet512")
        print(response)
        
        files['image1'][1].close()
        files['image2'][1].close()
        return jsonify(response)
    except Exception as e:
        return jsonify({"status": "Error", "error_message": str(e)})

@app.route('/restart')
def restart():
    subprocess.call(['kill', '1'])
    subprocess.call([sys.executable] + sys.argv)
    return 'Server is restarting...'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,use_reloader=True)