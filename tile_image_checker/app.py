# app.py

from flask import Flask, jsonify

app = Flask(__name__)

def greeting(name):
    return f"Hello, {name}! Welcome to GitHub Pages!"

@app.route('/greet/<name>')
def greet(name):
    message = greeting(name)
    return jsonify({'message': message})

if __name__ == '__main__':
    app.run()
