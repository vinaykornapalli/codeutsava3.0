from flask import Flask , render_template , request , jsonify
import sys
import os
from flask_cors import CORS , cross_origin
import json
import base64
from PIL import Image
from io import BytesIO
import re
from avemain import IdentifyPI

path = os.path.dirname(__file__)
uploads = path + 'uploads/'
modified = path + 'modified/'





app = Flask(__name__)
#cors
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app , resources={ r'/*': {'origins': "http://localhost:4200"}})
# app.config.from_object(os.environ['APP_SETTINGS'])



@app.route('/')
def index():
    return render_template('index.html')    





@app.route('/upload' , methods=['POST'])
def imageupload():
    if request.method == 'POST':
        data = request.data
        dataDict = json.loads(data)
        arr = dataDict["unblock"]
        print(arr)
        image_path = toBase64(dataDict['name'] , dataDict['image'])
        if arr == []:
            modified_image_path , modified_text = here_comes_magic(image_path)
        else:
            modified_image_path = corrected_magic(image_path , arr)
            modified_text = []
        response=jsonify({'path' : modified_image_path , 'text' : modified_text })
    return response


def toBase64(filename , codec):
    #converts image to binary and saves it
    data = re.sub('^data:image/.+;base64,', '', codec)
    byte_data = base64.b64decode(data)
    img_data = BytesIO(byte_data)
    img = Image.open(img_data)
    img.save(uploads + filename , "PNG")
    image_path = uploads + filename
    return image_path

def here_comes_magic(image_path):
    obj = IdentifyPI(image_path)
    return obj.retPath() , obj.retInfo()

def corrected_magic(image_path , arr):
    obj = IdentifyPI(image_path,arr=arr)
    return obj.retPath()



if __name__ == '__main__' :
    PORT = int(os.environ.get('PORT' , 5000))
    app.run(debug=True ,host='0.0.0.0' , port=PORT )