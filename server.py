import os
import pickle
from flask import Flask, request, jsonify

app = Flask(__name__)

registered_users = {}

def save_registered_users():
    with open('registered_users.pickle', 'wb') as file:
        pickle.dump(registered_users, file)

def load_registered_users():
    if os.path.exists('registered_users.pickle'):
        with open('registered_users.pickle', 'rb') as file:
            return pickle.load(file)
    else:
        return {}

@app.before_request
def setup():
    global registered_users
    registered_users = load_registered_users()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username and password:
        if username not in registered_users:
            registered_users[username] = password
            save_registered_users()
            return jsonify({'message': 'User registered successfully'}), 200
        else:
            return jsonify({'message': 'Username already exists'}), 400
    else:
        return jsonify({'message': 'Please provide both username and password'}), 400
    

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in registered_users and registered_users[username] == password:
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

if __name__ == '__main__':
    app.run()
