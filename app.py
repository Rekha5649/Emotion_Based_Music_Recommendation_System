from flask import Flask, request, render_template
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from flask_mysqldb import MySQL
import numpy as np
import base64
import cv2
import json

# create flask app
app = Flask(__name__)

# trained model
classifier = load_model('model_emotion.h5')

# Heroku database configurations
app.config['MYSQL_HOST'] = 'us-cdbr-east-04.cleardb.com'
app.config['MYSQL_USER'] = 'b7a9ad7e9a717d'
app.config['MYSQL_PASSWORD'] = '2a1a1be3'
app.config['MYSQL_DB'] = 'heroku_efa553e0c9160b4'
mysql = MySQL(app)



@app.route('/')
def home():
    return render_template('face_capture.html')

@app.route('/predict', methods = ['GET', 'POST'])
def predict():
    # check if the request is post
    if request.method == "POST":
        data = request.values['imgBase64']  
        encoded_data = data.split(',')[1]
        nparr = np.fromstring( base64.decodestring(encoded_data.encode('utf-8')),dtype=np.uint8)
        
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Labels
        class_labels = ['angry', 'fear', 'happy', 'neutral', 'sad']
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        # converting image to gray scale
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,1.3,5)
                
        if len(faces) != 0:
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray = gray[y:y+h,x:x+w]
                roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)
            
            
            if np.sum([roi_gray])!=0:
                roi = roi_gray.astype('float')/255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi,axis=0)

                # predict what is the emotion
                preds = classifier.predict(roi)[0]
                label=class_labels[preds.argmax()]
        
        else:
            # if the face is not found
            label = 'Face not found be sure there is enough light.'
            

        #Creating a connection cursor
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT Langue, Decade, Song_name, Song_url FROM SONGS WHERE Emotion =%s", [label])
        rows = cursor.fetchall(); 

        decade_dict = dict()
        
        for item in rows:
            if item[0] not in decade_dict.keys():
                decade_dict[item[0]] = dict()
               
            if item[1] not in decade_dict[item[0]].keys():
                decade_dict[item[0]][item[1]] = list()
            decade_dict[item[0]][item[1]].append(tuple([item[2],item[3]]))
    
        parameters = {'user_emotion': label, 'result': decade_dict }
        return render_template('index.html', song_data = json.dumps(parameters))


if __name__ == '__main__':
    app.run(debug=True)