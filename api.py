import flask
import os
from flask import request,jsonify
from werkzeug.utils import secure_filename
import faceRecognition as fr
app = flask.Flask(__name__)

# app.config['DEBUG'] = True

UPLOAD_FOLDER = '/tmp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/faceRecognition',methods=['POST','GET'])
def faceRecognition():
    if request.method == 'POST':
        if 'file' not in request.files:
          return jsonify({"Status":False,"Resp":"File not found"})
        file = request.files['file']
        if file.filename == '':
            return jsonify({"Statues":False,"Resp":"No filename"})
        filename = secure_filename(file.filename)
        path =  os.path.join(app.config['UPLOAD_FOLDER'],filename)
        file.save(path)        
        images = fr.face_compare(path)
        return jsonify({"Status":True,"Resp":images})
    elif request.method == 'GET':
        return jsonify({"Hello":"World"})
if __name__ == "__main__":
    app.run()
