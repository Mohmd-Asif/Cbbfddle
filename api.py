import flask
import os
from flask import request,jsonify
from werkzeug.utils import secure_filename
import faceRecognition as fr
app = flask.Flask(__name__)

app.config['DEBUG'] = True

UPLOAD_FOLDER = '/tmp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/faceRecognition',methods=['POST','GET'])
def faceRecognition():
    if request.method == 'POST':
        probable_names = []
        print(set(['file1','file2','file3','file4','file0'])&set(list(request.files.keys())))
        if set(['file1','file2','file3','file4','file0'])& set(list(request.files.keys())) != set(['file1','file2','file3','file4','file0']) :
           return jsonify({"Status":False,"Response":"File not found"})
        for filekey in request.files:
            file = request.files[filekey]
            if file.filename == '':
                return jsonify({"Status":False,"Response":"No filename"})
            filename = secure_filename(file.filename)
            path =  os.path.join(app.config['UPLOAD_FOLDER'],filename)
            file.save(path)
            if len(probable_names) == 0:        
                probable_names = fr.face_compare(path)
            else:
                images = fr.face_compare(path)
                images = set(images)
                probable_names = set(probable_names)
                probable_names = list(probable_names & images)
            
        return jsonify({"Status":True,"Response":probable_names})
    elif request.method == 'GET':
        return jsonify({"Hello":"World"})
if __name__ == "__main__":
    app.run()
