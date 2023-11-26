#Importing libraries
from ctypes.wintypes import POINT
from re import U
import os
import io
from flask import Flask , request , send_from_directory, jsonify, make_response, send_file
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
from flask_cors import CORS , cross_origin
from werkzeug.utils import secure_filename
import datetime
from Utils.html_to_pdf import *
import requests
from dotenv import load_dotenv


#Initializing our app 
app = Flask(__name__, static_url_path='')

app.config['JWT_SECRET_KEY'] = "HTML_Editor"
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
jwt = JWTManager(app)

#Initialzing the CORS extension with our app
CORS(app)
load_dotenv()


x = datetime.datetime.now()


@app.route("/html-upload", methods=['POST'])
@cross_origin() 
def htmlUpload():
    if request.method == "POST":
        # Storing the uploaded HTML file on the backend
        f = request.files['htmlFile']
        if f:
            # Check if the uploaded file has an HTML extension
            if f.filename.endswith(".html"):
                filename = secure_filename(f.filename)
                global file_path
                file_path = os.path.join('temp_files', filename)
                f.save(file_path)
                PDFPrint(file_path)
                return {"Status": "Successfully Uploaded"}, 201
            else:
                return {"Status": "Error: The uploaded file is not in HTML format"}, 500
        else:
            return {"Status": "Error encountered"}, 500
    
@app.route('/google_login', methods=['POST'])
@cross_origin()
def login():  
    auth_code = request.get_json()['code']

    data = {
        'code': auth_code,
        'client_id': os.getenv('GOOGLE_CLIENT_ID'),  # client ID from the credential at google developer console
        'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),  # client secret from the credential at google developer console
        'redirect_uri': 'postmessage',
        'grant_type': 'authorization_code' 
    }

    response = requests.post('https://oauth2.googleapis.com/token', data=data).json()
    headers = {
        'Authorization': f'Bearer {response["access_token"]}'
    }
    user_info = requests.get('https://www.googleapis.com/oauth2/v3/userinfo', headers=headers).json()

    user_info['access_token'] = response["access_token"]
  
    jwt_token = create_access_token(identity=user_info['email'])  # create jwt token

    response_data = {
        'user': user_info
    }

    response = make_response(jsonify(response_data), 200)

    response.set_cookie('access_token_cookie', value=jwt_token, secure=True)

    return response, 200
    
@app.route('/time')
@cross_origin()
def get_time():
    # Create a JSON object with the current time
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    json_response = {'time': current_time}

    # Return the JSON response
    return jsonify(json_response)   


@app.route('/download')
@cross_origin()
def download_file():
    # Assuming 'edited.pdf' is in the 'temp' folder
    pdf_path = file_path.replace(".html", ".pdf")

    # Send the file as an attachment with a specific filename
    return send_file(pdf_path, as_attachment=True, download_name='edited.pdf')



@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder , 'index.html')

if __name__ == '__main__':
    app.run()  