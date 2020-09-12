# app.py
from flask import Flask, render_template, request
import AutoStencil as austen

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("app.html")

@app.route("/calculate", methods=['POST'])
def calculate():
    pointsString = request.form['num1']
    dimString = request.form['num2']
    print(pointsString)
    print(dimString)
    operation = request.form['operation']

    latexString, codeString = austen.parseStringInputs(pointsString, dimString)
    return render_template('app.html', result=codeString)

#    if operation == 'add':
#        result = float(num1) + float(num2)
#        return render_template('app.html', result=result)
#    elif operation == 'subtract':
#        result = float(num1) - float(num2)
#        return render_template('app.html', result=result)
#    elif operation == 'multiply':
#        result = float(num1) * float(num2)
#        return render_template('app.html', result=result)
#    elif operation == 'divide':
#        result = float(num1) / float(num2)
#        return render_template('app.html', result=result)
#    else:
#        return render_template('app.html')
