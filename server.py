from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

app = Flask(__name__)
CORS(app)

DATA_FILE = 'announcements.json'
USERS_FILE = 'users.json'

# Создайте директорию, если её не существует
if not os.path.exists('static'):
    os.makedirs('static')

# Функция для загрузки данных из файла
def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return []

# Функция для сохранения данных в файл
def save_data(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/register', methods=['POST'])
def register():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400
        
        users = load_data(USERS_FILE)

        if any(user['username'] == username for user in users):
            return jsonify({"error": "User already exists"}), 400

        hashed_password = generate_password_hash(password)
        new_user = {
            'id': str(uuid.uuid4()),
            'username': username,
            'password': hashed_password
        }

        users.append(new_user)
        save_data(users, USERS_FILE)

        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400
        
        users = load_data(USERS_FILE)
        user = next((user for user in users if user['username'] == username), None)

        if user and check_password_hash(user['password'], password):
            return jsonify({"message": "Login successful", "user_id": user['id']}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/supersecretdomainfortestDHSACVjdafcsaasdasdajdasdasjdasdasjdasdasdijjasdasdjlaksdljaskdjaskd')
def admin_panel():
    return send_from_directory('', './supersecretdomainfortestDHSACVjdafcsaasdasdajdasdasjdasdasjdasdasdijjasdasdjlaksdljaskdjaskd.html')

@app.route('/announcements', methods=['POST'])
def add_announcement():
    try:
        title = request.form.get('title')
        content = request.form.get('content')
        name = request.form.get('name')
        contact = request.form.get('contact')
        image = request.files.get('image')

        if not title or not content:
            return jsonify({"error": "Title and content are required"}), 400

        announcements = load_data(DATA_FILE)

        new_id = max([ann['id'] for ann in announcements], default=0) + 1
        image_path = None
        if image:
            image_filename = f"image_{new_id}.jpg"
            image_path = os.path.join('static', image_filename)
            image.save(image_path)

        new_announcement = {
            'id': new_id,
            'title': title,
            'content': content,
            'name': name,
            'contact': contact,
            'image': image_path
        }

        announcements.append(new_announcement)
        save_data(announcements, DATA_FILE)

        return jsonify(new_announcement), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/announcements', methods=['GET'])
def get_announcements():
    try:
        username = request.args.get('username')
        announcements = load_data(DATA_FILE)
        
        if username:
            announcements = [ann for ann in announcements if ann.get('name') == username]
            
        return jsonify(announcements), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/announcements/<int:id>', methods=['GET'])
def get_announcement(id):
    try:
        announcements = load_data(DATA_FILE)
        announcement = next((ann for ann in announcements if ann['id'] == id), None)
        if announcement:
            return jsonify(announcement), 200
        else:
            return jsonify({"error": "Announcement not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/announcements/<int:id>', methods=['PUT'])
def update_announcement(id):
    try:
        announcements = load_data(DATA_FILE)
        announcement_found = False
        for ann in announcements:
            if ann['id'] == id:
                announcement_found = True
                ann.update({
                    'title': request.form.get('title', ann['title']),
                    'content': request.form.get('content', ann['content']),
                    'name': request.form.get('name', ann['name']),
                    'contact': request.form.get('contact', ann['contact'])
                })
                if 'image' in request.files:
                    image = request.files['image']
                    image_filename = f"image_{id}.jpg"
                    image_path = os.path.join('static', image_filename)
                    image.save(image_path)
                    ann['image'] = image_path

        if announcement_found:
            save_data(announcements, DATA_FILE)
            return jsonify({"message": "Announcement updated"}), 200
        else:
            return jsonify({"error": "Announcement not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/announcements/<int:id>', methods=['DELETE'])
def delete_announcement(id):
    try:
        announcements = load_data(DATA_FILE)
        announcements = [ann for ann in announcements if ann['id'] != id]
        save_data(announcements, DATA_FILE)
        return jsonify({"message": "Announcement deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/users/<username>/change-password', methods=['POST'])
def change_password(username):
    try:
        current_password = request.json.get('currentPassword')
        new_password = request.json.get('newPassword')

        users = load_data(USERS_FILE)
        user = next((user for user in users if user['username'] == username), None)

        if user and check_password_hash(user['password'], current_password):
            user['password'] = generate_password_hash(new_password)
            save_data(users, USERS_FILE)
            return jsonify({"message": "Password changed successfully"}), 200
        else:
            return jsonify({"error": "Invalid current password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
