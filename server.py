from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for registered users (replace with a database in production)
registered_users = {
            '우정균':'2022108145',
            '현은솔':'2020107140',
            '최예람':'2022108151'
}

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username and password:
        if username not in registered_users:
            registered_users[username] = password
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
