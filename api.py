from flask import Flask, request, render_template, jsonify
from interpreter import Interpreter

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_template():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def echo_string():
    data = request.get_json()
    if 'input_string' in data:
        code = data['input_string']
        interpreter = Interpreter()
        result = interpreter.start(code)
        return jsonify(result)
    return jsonify({'error': 'No input_string provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)
