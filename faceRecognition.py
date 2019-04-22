import facerecogntition_api as fa
import os
import sqlite3
import pickle


def face_compare(image_path):
    detected_files = []
    with  sqlite3.connect('database.db') as connection:
        img1 = fa.load_image_file(image_path)
        img1_encoding = fa.face_encodings(img1)
        cur = connection.cursor()
        cur.execute('SELECT * FROM USERS')
        rows = cur.fetchall()
        for (file_name,image_encoding) in rows:
            image_encoding = pickle.loads(image_encoding)
            if True in fa.compare_faces(img1_encoding,image_encoding):
                detected_files.append(file_name)
    return detected_files