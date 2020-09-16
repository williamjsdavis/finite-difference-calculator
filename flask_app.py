# app.py
from flask import Flask, render_template, request, jsonify
import AutoStencil as austen

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("app.html")

@app.route('/background_process')
def background_process():
    try:
        points_str = request.args.get('points_string', 0, type=str)
        derivative_str = request.args.get('derivative_string', 0, type=str)
        latex_str, code_str = austen.parseStringInputs(points_str, derivative_str)
        return jsonify(latex_str=latex_str, code_str=code_str)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
