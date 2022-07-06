from typing import final
from flask import Flask, flash, jsonify, redirect, render_template, \
     request, url_for

from model import model

# from model import read_files

app = Flask(__name__)
app.config['JSON_AS_ASCII']=False

@app.route('/')
def index():
    return render_template('index.html',data=[{'name':'headlines'},{'name':'summary'}])

@app.route("/result" , methods=['GET', 'POST'])
def result():
    option = request.form.get('comp_select')
    id_ =request.form.get('data_id')
    print(id_,option)

    final_result = model(option=option,id_=id_)
    data1= {option:final_result}
    return jsonify(data1)

if __name__=='__main__':
    app.run(debug=True)