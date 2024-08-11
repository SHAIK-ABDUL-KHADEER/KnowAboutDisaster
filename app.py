from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
import json
import os
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

# Configure Google Generative AI
genai.configure(api_key="AIzaSyA-v_ewbJVYSJqrNwvrR8DYvsCthxaYmYo")  # Use the correct API key here

# Create the generative model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# User class
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Load users from Excel (ensure file is created if not present)
def load_users():
    if not os.path.exists('users.xlsx'):
        df = pd.DataFrame(columns=['id', 'username', 'password'])
        df.to_excel('users.xlsx', index=False)
    return pd.read_excel('users.xlsx')

users_df = load_users()

@login_manager.user_loader
def load_user(user_id):
    user_data = users_df[users_df['id'] == int(user_id)]
    if not user_data.empty:
        user_data = user_data.iloc[0]
        return User(user_data['id'], user_data['username'], user_data['password'])
    return None

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = users_df[(users_df['username'] == username) & (users_df['password'] == password)]
        if not user_data.empty:
            user = User(user_data.iloc[0]['id'], username, password)
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    global users_df

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_id = users_df['id'].max() + 1
        new_user = {'id': new_id, 'username': username, 'password': password}
        users_df = users_df.append(new_user, ignore_index=True)
        users_df.to_excel('users.xlsx', index=False)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('index.html', username=current_user.username)

@app.route('/upload_location', methods=['POST'])
@login_required
def upload_location():
    data = request.json
    disaster_name = data.get('disaster_name')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    notification = {
        "username": current_user.username,
        "disaster_name": disaster_name,
        "latitude": latitude,
        "longitude": longitude,
        "timestamp": pd.Timestamp.now()
    }

    notifications_file = 'notifications.json'
    if os.path.exists(notifications_file):
        with open(notifications_file, 'r') as f:
            notifications = json.load(f)
    else:
        notifications = []

    notifications.append(notification)

    with open(notifications_file, 'w') as f:
        json.dump(notifications, f)

    return jsonify(success=True)

@app.route('/get_notifications')
@login_required
def get_notifications():
    notifications_file = 'notifications.json'
    if os.path.exists(notifications_file):
        with open(notifications_file, 'r') as f:
            notifications = json.load(f)
    else:
        notifications = []

    return jsonify(notifications=notifications)

@app.route('/chat', methods=['POST'])
@login_required
def chat():
    data = request.json
    user_question = data.get('question')
    disaster_name = data.get('disaster_name')

    if not user_question:
        return jsonify({"error": "No question provided"}), 400

    try:
        # Define prompt based on the disaster type
        if disaster_name:
            prompt = (
                f"You are an expert on {disaster_name}. Please provide a brief answer related to {disaster_name} "
                "with a maximum of 3 to 4 sentences. Be concise and informative."
            )
        else:
            prompt = (
                "Provide a brief answer with a maximum of 3 to 4 sentences."
            )

        # Combine user question with the prompt
        full_prompt = f"{prompt}\n\nUser question: {user_question}"

        # Generate a response using the Gemini API
        response = model.generate_content(full_prompt)
        answer = response.text.strip() if response.text else "No response text available."

        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
