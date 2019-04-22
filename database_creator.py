import sqlite3
import facerecogntition_api as fa
import os
import pickle

connection = sqlite3.connect('database.db')

connection.execute('CREATE TABLE USERS(FILENAME TEXT,ENCODING TEXT)')
known_image_path = "./test_images/image_database/"

for known_image in os.listdir(known_image_path):
    img = fa.load_image_file(os.path.join(known_image_path,known_image))
    img_encoding = fa.face_encodings(img)
    img_encoding = pickle.dumps(img_encoding,protocol=pickle.HIGHEST_PROTOCOL)
    current = connection.cursor()
    current.execute("INSERT INTO USERS VALUES(?,?)",(os.path.join(known_image_path,known_image),img_encoding))
    connection.commit()

connection.close()
