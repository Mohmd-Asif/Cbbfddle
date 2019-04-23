import flask
import os
from flask import request,jsonify
from werkzeug.utils import secure_filename
import faceRecognition as fr
import facerecogntition_api as fa
import sqlite3

app = flask.Flask(__name__)

app.config['DEBUG'] = True

UPLOAD_FOLDER = '/tmp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/faceRecognition',methods=['POST','GET'])
def faceRecognition():
    if request.method == 'POST':
        probable_names = []
        predictions = []
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
        with sqlite3.connect('database.db') as connection:
            for i in probable_names:
                cur = connection.cursor()
                cur.execute('''SELECT * FROM USER_LICENSE WHERE FILENAME=?''',i)
                row = cur.fetchall()
                if row[3] >=3:
                    row[2] = 30000
                else:
                    row[3]+=1
                    row[2] = 7
                cur.execute('UPDATE USER_LICENSE SET CANCELLATION='+row[2]+',PENALTY='+row[3]+' WHERE FILENAME='+row[0])
                cur.commit()
        return jsonify({"Status":True,"Response":probable_names})
    elif request.method == 'GET':
        return jsonify({"Hello":"World"})
if __name__ == "__main__":
    app.run()
