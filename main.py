# Flask use for creating framework to run python 
from flask import Flask, render_template, Response,session,url_for
from flask import Flask, flash, redirect, render_template, request, abort
from flask_mail import Mail, Message,Attachment
import pandas as pd
import json

# Main function call and its main file 

from face_recog1 import predict   #call predict function of Face_recog1.py file
from tester import weapDetect   # call weapDetect function of tester.py file
from inference import pose  
from HandgestureOpenCv import handGes
from camera import VideoCamera
from pieexp import expRes
from piehand import handRes #remove 
from piepose import poseRes #remove 
from pieface import faceRes

app = Flask(__name__,template_folder='templates')
app.secret_key = "abc"
mail= Mail(app)

# Login with given mail on smtp(Simple mail Transport protocol) protocol
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'techno.spark8720@gmail.com'
app.config['MAIL_PASSWORD'] = 'NISHANT8720'
app.config['MAIL_USE_TLS'] = False # Transport Layer Security 'default= false'
app.config['MAIL_USE_SSL'] = True  # Secure Sockets Layer 'default=false'
mail = Mail(app)

#start form current dir
@app.route('/')
def home():
        return render_template('/upload.html')


@app.route('/famatch',methods=['POST'])
def faceindex():
    if request.form['action'] == 'Video':    # On video click
        session['path'] = request.form['path3']  # request for a path
        s=session['path']  # store path in s variable
       
    elif request.form['action'] == 'Camera':    # On camera click
        session['path'] = 0 
        s=session['path']
        
    
    # s=session['path']
    # isWeap=weapDetect(s)

    # call predict function of Face_recog1.py file
    id1=predict(s)
    if(id1==1):
        return render_template('/weapon.html') # Open Weapon detection model 
    else:
        return render_template('/fail.html') # Face Not Recognized


@app.route('/weapon',methods=['POST'])
def whome():
    w=session['path']    # store path in w variable
    isWeap=weapDetect(w) # Call weapDetect function of tester.py file 
    if (isWeap==1):
#        mail_flag=1
        #sendMail()
        
        # class Message(subject='', recipients=None, body=None, html=None, sender=None, cc=None, bcc=None, 
        # attachments=None, reply_to=None, date=None, charset=None, extra_headers=None, mail_options=None, rcpt_options=None)
        msg = Message('Weapon Detected', sender = 'techno.spark8720@gmail.com', recipients = ['techno.spark8720@gmail.com'])
        msg.body = "Weapon has been detected at given location!"
        ### msg.attach with app.open_resource("image.png") as fp:
        ### msg.attach("galaxy.png", "image/png", fp.read()) file seprated by ,
           
        mail.send(msg)
        return render_template('/fail2.html')   # May Contain Weapon
    else:
        return render_template('/expr.html')    # Go to the next pose module
"""
@app.route('/pose',methods=['POST'])
def home1():
    # varpath1 = request.form['path1']
    varpath1=session['path']
    isPose=pose(varpath1)
    return render_template('/hand.html')

@app.route('/hand',methods=['POST'])
def home2():
    # varpath2 = request.form['path2']
    varpath2=session['path']
    isGes=handGes(varpath2)
    return render_template('/expr.html')
"""

@app.route('/expr',methods=['POST'])
def index():
    return render_template('/index.html') 



def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/result',methods=['POST'])
def inex():
    #sendMail()
    return render_template('/results.html')

@app.route('/resexpr')
def index11():
    pop1=expRes()
    return render_template('/results.html')
""" 
@app.route('/reshand')
def index22():
    pop2=handRes()
    return render_template('/results.html')

@app.route('/respose')
def index33():
    pop3=poseRes()
    return render_template('/results.html')
"""
@app.route('/resface')
def index55():
    pop4=faceRes()
    return render_template('/results.html')

@app.route('/face_form', methods=['GET', 'POST'])
def face_form():
    #if request.method == 'POST':
    return redirect(url_for('index55'))
"""
@app.route('/pose_form', methods=['GET', 'POST'])
def pose_form():
    # if request.method == 'POST':
    return redirect(url_for('index33'))
"""
@app.route('/expr_form', methods=['GET', 'POST'])
def expr_form():
    #Sif request.method == 'POST':
    return redirect(url_for('index11'))
"""
@app.route('/hand_form', methods=['GET', 'POST'])
def hand_form():
    # if request.method == 'POST':
    return redirect(url_for('index22'))
"""
@app.route('/exp/<name>')
def express1(name):
    df = pd.read_csv (r'isExp.csv')
    df.to_json (r'isExp.json')
    with open('isExp.json', 'r') as jsonfile:
        file_data = json.loads(jsonfile.read())
    return json.dumps(file_data[name])

@app.route('/face/<name>')
def express2(name):
    df = pd.read_csv (r'isFace.csv')
    df.to_json (r'isFace.json')
    with open('isFace.json', 'r') as jsonfile:
        file_data = json.loads(jsonfile.read())
    return json.dumps(file_data[name])
"""
@app.route('/hand/<name>')
def express3(name):
    df = pd.read_csv (r'isHand.csv')
    df.to_json (r'isHand.json')
    with open('isHand.json', 'r') as jsonfile:
        file_data = json.loads(jsonfile.read())
    return json.dumps(file_data[name])

@app.route('/pose/<name>')
def express4(name):
    df = pd.read_csv (r'isPose.csv')
    df.to_json (r'isPose.json')
    with open('isPose.json', 'r') as jsonfile:
        file_data = json.loads(jsonfile.read())
    return json.dumps(file_data[name])
"""
@app.route('/weap/<name>')
def express5(name):
    df = pd.read_csv (r'isWeap.csv')
    df.to_json (r'isWeap.json')
    with open('isWeap.json', 'r') as jsonfile:
        file_data = json.loads(jsonfile.read())
    return json.dumps(file_data[name])



if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1', port=5000)
