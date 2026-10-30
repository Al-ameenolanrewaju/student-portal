import os
from flask import Flask, render_template, jsonify, request, redirect, flash, url_for
from states_lgas import states_lgas
import mysql.connector
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'super secret key')

# Database connection configured via environment variables
db = mysql.connector.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    user=os.getenv('DB_USER', 'root'),
    passwd=os.getenv('DB_PASSWORD', ''),
    database=os.getenv('DB_NAME', 'Flask_app'),
    port=int(os.getenv('DB_PORT', 3306))
)
cursor = db.cursor()
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/information')
def information():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM applicants")
    data = cursor.fetchall()
    return render_template('information.html', information=data)

   
@app.route('/form', methods=['GET', 'POST'])
def form():
    states = list(states_lgas.keys())
    return render_template('form.html', states=states)


@app.route('/submit', methods=['POST'])
def submit():

    image = request.files.get('image')
    filename = None

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    gender = request.form.get('gender')
    jamb_score = request.form.get('jamb_score')

    # 🔥 Validation
    if not first_name or not last_name or not email or not gender or not jamb_score:
        flash("Please fill all required fields!", "danger")
        return redirect('/form')

    # Image upload (optional)
    if image and image.filename != "":
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Insert into DB
    sql = """
        INSERT INTO applicants 
        (first_name, middle_name, last_name, email, dob, gender, phone, address, state, lga, next_of_kin, jamb_score, image)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        first_name,
        request.form.get('middle_name'),
        last_name,
        email,
        request.form.get('dob'),
        gender,
        request.form.get('phone'),
        request.form.get('address'),
        request.form.get('state'),
        request.form.get('lga'),
        request.form.get('next_of_kin'),
        jamb_score,
        filename
    )

    cursor.execute(sql, values)
    db.commit()

    flash("Application submitted successfully!", "success")
    return redirect('/information')

@app.route('/profile/<int:id>')
def profile(id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM applicants WHERE id = %s", (id,))
    student = cursor.fetchone()
    return render_template('profile.html', student=student)


@app.route('/get_lgas')
def get_lgas():
    state = request.args.get('state')
    if state in states_lgas:
        lgas = states_lgas[state]
    else:
        lgas = []
    return jsonify(lgas)

@app.route('/search_students')
def search_students():
    cursor = db.cursor(dictionary=True)

    search_name = request.args.get('search_name', '').strip()
    search_admission = request.args.get('search_admission', '').strip()
    search_gender = request.args.get('search_gender', '').strip()
    search_jamb = request.args.get('search_jamb', '').strip()

    sql = "SELECT * FROM applicants WHERE 1=1"
    values = []

    if search_name:
        sql += " AND CONCAT(first_name, ' ', last_name) LIKE %s"
        values.append(f"%{search_name}%")
    if search_admission:
        sql += " AND id LIKE %s"
        values.append(f"%{search_admission}%")
    if search_gender:
        sql += " AND gender = %s"
        values.append(search_gender)
    if search_jamb:
        sql += " AND jamb_score = %s"
        values.append(search_jamb)

    cursor.execute(sql, tuple(values))
    data = cursor.fetchall()
    return jsonify(data)


if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() in ('true', '1', 't')
    port = int(os.getenv('PORT', 5000))
    app.run(debug=debug_mode, port=port)
