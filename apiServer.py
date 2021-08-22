import json
import pandas as pd

from flask import Flask
    
app = Flask(__name__)

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

@app.route('/weap/<name>')
def express5(name):
    df = pd.read_csv (r'isWeapon.csv')
    df.to_json (r'isWeap.json')
    with open('isWeap.json', 'r') as jsonfile:
        file_data = json.loads(jsonfile.read())
    return json.dumps(file_data[name])

if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1', port=8000)