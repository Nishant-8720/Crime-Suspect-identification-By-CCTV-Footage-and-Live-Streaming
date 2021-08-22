from flask import Flask, render_template, Response
from flask import Flask, flash, redirect, render_template, request, abort
from main import index

app = Flask(__name__,template_folder='templates')

@app.route('/path',methods=['POST'])
def pathing():
    varpath = request.form['path3']
    return varpath

vpath=pathing()
index(vpath)


if __name__ == '__main__':
   app.run(debug=True,host='127.0.0.1', port=5000)
