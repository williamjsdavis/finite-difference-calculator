# app.py
from flask import Flask, render_template, request, jsonify
import AutoStencil as austen
import random

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("app.html")

@app.route("/", methods=['POST'])
def calculate():
    pointsString = request.form['num1']
    dimString = request.form['num2']

    latexString, codeString = austen.parseStringInputs(pointsString, dimString)
    return render_template('app.html', resultLatex=latexString,
                                       resultCode=codeString)

@app.route('/get_word')
def languages():
    '''Return data in json format'''
    lst = ["Python", 'HTML', 'JavaScript', 'CSS']
    words = {}
    words['choice'] = random.choice(lst)
    dimString = str(random.randint(1,4))
    pointsString = '-2,-1,0,1,2'
    latexString, codeString = austen.parseStringInputs(pointsString, dimString)
    words['latex'] = latexString
    words['code'] = codeString
    return jsonify(words)

@app.route('/copy_word')
def languages2():
    '''Return data in json format'''
    words = {}
    words['choice'] = 'test'
    return jsonify(words)

@app.route('/background_process')
def background_process():
    

    dimString = str(random.randint(1,4))
    
    try:
        points_str = request.args.get('points_string', 0, type=str)
        derivative_str = request.args.get('derivative_string', 0, type=str)
        latex_str, code_str = austen.parseStringInputs(points_str, derivative_str)
        return jsonify(latex_str=latex_str, code_str=code_str)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
