# from flask import Flask, render_template, request, redirect, url_for,send_from_directory
# import os
# from datetime import datetime
# import mysql.connector
# import random

# app = Flask(__name__)
# UPLOAD_FOLDER = 'AI_Interviews'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # MySQL connection configuration
# db_config = {
#     'user': 'root',
#     'password': '123@sahil',
#     'host': 'localhost',
#     'database': 'interview_db'
# }

# SUBJECT_MAPPING = {
#     'AIML': 'AIML',
#     'Data Science': 'Data Science',
#     'Java Developer': 'Java Developer'
# }

# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# @app.route('/')
# def index():
#     return render_template('name.html')

# @app.route('/instructions', methods=['GET'])
# def instructions():
#     name = request.args.get('name', '')
#     subject = request.args.get('subject', '')
#     return render_template('instructions.html', name=name, subject=subject)

# @app.route('/record', methods=['GET'])
# def record():
#     name = request.args.get('name', '')
#     subject = request.args.get('subject', '')

#     subject_column = SUBJECT_MAPPING.get(subject, None)

#     if not subject_column:
#         return f"Error: No column found for subject '{subject}'"

#     # Connect to the MySQL database
#     conn = mysql.connector.connect(**db_config)
#     cursor = conn.cursor()

#     # Fetch questions from the database for the specified subject
#     query = "SELECT question FROM questions WHERE subject = %s"
#     cursor.execute(query, (subject_column,))
#     questions = cursor.fetchall()

#     # Close the database connection
#     conn.close()

#     questions = [q[0] for q in questions]

#     if len(questions) < 5:
#         return "Error: Not enough questions available for selection"
    
#     selected_questions = random.sample(questions, 5)

#     return render_template('record.html', name=name, questions=selected_questions)

# @app.route('/save_user_details', methods=['POST'])
# def save_user_details():
#     name = request.form.get('name')
#     age = request.form.get('age')
#     college = request.form.get('college')
#     gender = request.form.get('gender')
#     source = request.form.get('source')
#     purpose = request.form.get('purpose')
#     subject = request.form.get('subject')

#     # Connect to the MySQL database
#     conn = mysql.connector.connect(**db_config)
#     cursor = conn.cursor()

#     # Insert user details into the database
#     query = """
#         INSERT INTO user_details (name,age, college, gender,source, purpose, subject)
#         VALUES (%s,%s,%s, %s, %s, %s, %s)
#     """
#     cursor.execute(query, (name,age, college, gender,source, purpose, subject))

#     # Commit the transaction
#     conn.commit()

#     # Close the database connection
#     cursor.close()
#     conn.close()

#     # Redirect to the appropriate route based on the purpose
#     if purpose == 'Vidume':
#         return redirect(url_for('instructions', name=name, subject=subject))
#     else:
#         return redirect(url_for('record', name=name, subject=subject))
    
# @app.route('/upload', methods=['POST'])
# def upload():
#     if 'video' in request.files:
#         video = request.files['video']
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from datetime import datetime
import mysql.connector
import random
import requests

app = Flask(__name__)
UPLOAD_FOLDER = 'AI_Interviews'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# MySQL connection configuration
db_config = {
    'user': 'root',
    'password': '123@sahil',
    'host': 'localhost',
    'database': 'interview_db'
}

# Telegram bot configuration
TELEGRAM_BOT_TOKEN = '7278808022:AAGwfQ493IvjGRoXJbDYBBP6OxvZ0-oeHJw'
TELEGRAM_CHAT_ID = '7475898415'

SUBJECT_MAPPING = {
    'AIML': 'AIML',
    'Data Science': 'Data Science',
    'Java Developer': 'Java Developer'
}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('name.html')

@app.route('/instructions', methods=['GET'])
def instructions():
    name = request.args.get('name', '')
    subject = request.args.get('subject', '')
    return render_template('instructions.html', name=name, subject=subject)

@app.route('/record', methods=['GET'])
def record():
    name = request.args.get('name', '')
    subject = request.args.get('subject', '')

    subject_column = SUBJECT_MAPPING.get(subject, None)

    if not subject_column:
        return f"Error: No column found for subject '{subject}'"

    # Connect to the MySQL database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Fetch questions from the database for the specified subject
    query = "SELECT question FROM questions WHERE subject = %s"
    cursor.execute(query, (subject_column,))
    questions = cursor.fetchall()

    # Close the database connection
    conn.close()

    questions = [q[0] for q in questions]

    if len(questions) < 5:
        return "Error: Not enough questions available for selection"
    
    selected_questions = random.sample(questions, 5)

    return render_template('record.html', name=name, questions=selected_questions)

@app.route('/save_user_details', methods=['POST'])
def save_user_details():
    name = request.form.get('name')
    age = request.form.get('age')
    college = request.form.get('college')
    gender = request.form.get('gender')
    source = request.form.get('source')
    purpose = request.form.get('purpose')
    subject = request.form.get('subject')

    # Connect to the MySQL database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Insert user details into the database
    query = """
        INSERT INTO user_details (name, age, college, gender, source, purpose, subject)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (name, age, college, gender, source, purpose, subject))

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    # Redirect to the appropriate route based on the purpose
    if purpose == 'Vidume':
        return redirect(url_for('instructions', name=name, subject=subject))
    else:
        return redirect(url_for('record', name=name, subject=subject))

@app.route('/upload', methods=['POST'])
def upload():
    if 'video' in request.files:
        video = request.files['video']
        # Get the current date and time
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        # Construct the filename using the user's name and timestamp
        filename = f"{request.args.get('name', 'default')}_{timestamp}.mp4"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        video.save(file_path)

        # Send the video to Telegram
        send_file_to_telegram(file_path)

        return {'status': 'success', 'filename': filename}
    return {'status': 'failure'}

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def send_file_to_telegram(file_path):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument'
    with open(file_path, 'rb') as file:
        files = {'document': file}
        data = {'chat_id': TELEGRAM_CHAT_ID}
        response = requests.post(url, data=data, files=files)

    if response.status_code == 200:
        print(f"Successfully sent {file_path}")
    else:
        print(f"Failed to send {file_path}. Error: {response.status_code} - {response.text}")

if __name__ == '__main__':
    app.run(debug=True)




