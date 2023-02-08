from flask import Flask, request, render_template, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'something'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1212'
app.config['MYSQL_DB'] = 'comma_patient'

mysql = MySQL(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT Email, Password FROM doctors")
        doctors = cur.fetchall()
        cur.close()

        cur1 = mysql.connection.cursor()
        cur1.execute("SELECT Email, Password FROM nurse")
        nurses = cur1.fetchall()
        cur1.close()
       
        cur2 = mysql.connection.cursor()
        cur2.execute("SELECT Email, Password FROM patient")
        patients = cur2.fetchall()
        cur2.close()

        cur3 = mysql.connection.cursor()
        cur3.execute("SELECT Email, Password FROM admin")
        admins = cur3.fetchall()
        cur3.close()
        
        for doctor in doctors:
            if email in doctor and password in doctor:
                session['email'] = email
                session['role'] = 'doc'
                return redirect(url_for("doctor"))
        for nurse in nurses:
            if email in nurse and password in nurse:
                session['email'] = email
                session['role'] = 'nur'
                return redirect(url_for("nurse"))
        for patient in patients:
            if email in patient and password in patient:
                session['email'] = email
                session['role'] = 'pat'
                return redirect(url_for('patient'))
        for admin in admins:
            if email in admin and password in admin:
                session['email'] = email
                session['role'] = 'adm'
                return redirect(url_for('admin'))
               
    return render_template("signin.html")


@app.route("/admin_about")
def admin_about():
    if 'email' not in session or session.get('role', '') != 'adm':
        return redirect(url_for('signin'))
    return render_template('admin/about.html')

@app.route("/doctor_about")
def doctor_about():
    if 'email' not in session or session.get('role', '') != 'doc':
        return redirect(url_for('signin'))
    return render_template('doc/about.html')

@app.route("/nurse_about")
def nurse_about():
    if 'email' not in session or session.get('role', '') != 'nur':
        return redirect(url_for('signin'))
    return render_template('nurse/about.html')

@app.route("/pat_about")
def pat_about():
    if 'email' not in session or session.get('role', '') != 'pat':
        return redirect(url_for('signin'))
    return render_template('patient/about.html')

@app.route('/admin')
def admin():
    if 'email' not in session or session.get('role', '') != 'adm':
        return redirect(url_for('signin'))

    return render_template('admin/admin.html')

@app.route('/doctor')
def doctor():
    if 'email' not in session or session.get('role', '') != 'doc':
        return redirect(url_for('signin'))

    return render_template('doc/doctor.html')

@app.route('/nurse')
def nurse():
    if 'email' not in session or session.get('role', '') != 'nur':
        return redirect(url_for('signin'))

    return render_template('nurse/nurse.html')

@app.route('/patient')
def patient():
    if 'email' not in session or session.get('role', '') != 'pat':
        return redirect(url_for('signin'))
    return render_template('patient/patient.html')

@app.route('/<name>')
def lost(name):
    return redirect(url_for('home'))

@app.route('/new_account', methods=['GET', 'POST'])
def new_account():
    if 'email' not in session or session.get('role', '') != 'adm':
        return redirect(url_for('signin'))
    if request.method == "POST":
        name = request.form["first_name"] + ' ' + request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]
        cur0 = mysql.connection.cursor()
        cur0.execute("INSERT INTO doctors (Name, Email, Password) VALUES (%s, %s, %s)", (name, email, password))
        mysql.connection.commit()
        cur0.close()    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM doctors")
    doctors = cur.fetchall()
    cur.close()
    return render_template('admin/admin_tool/new_account.html', doctors = doctors)

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if 'email' not in session or session.get('role', '') != 'adm':
        return redirect(url_for('signin'))
    if request.method == "POST":
        name = request.form["first_name"] + ' ' + request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]
        cur0 = mysql.connection.cursor()
        cur0.execute("INSERT INTO patient (Name, Email, Password) VALUES (%s, %s, %s)", (name, email, password))
        mysql.connection.commit()
        cur0.close()    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM patient")
    patient = cur.fetchall()
    cur.close()
    return render_template('admin/admin_tool/add_patient.html', patient = patient)

@app.route('/admin_news', methods=['GET', 'POST'])
def admin_news():
    if 'email' not in session or session.get('role', '') != 'adm':
        return redirect(url_for('signin'))
    if request.method == "POST":
        name = request.form["name"]
        mon = request.form["monday"]
        tue = request.form["tuesday"]
        wed = request.form["wednesday"]
        thu = request.form["thursday"]
        fri = request.form["friday"]
        sat = request.form["saturday"]
        sun = request.form["sunday"]
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO news (Name, monday, tuesday, wednesday, thursday, friday, saturday, sunday) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (name, mon, tue, wed, thu, fri, sat, sun))
        mysql.connection.commit()
        cur.close()
    return render_template("admin/news.html")

@app.route('/doctor_news')
def doctor_news():
    if 'email' not in session or session.get('role', '') != 'doc':
        return redirect(url_for('signin'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM news")
    news = cur.fetchall()
    cur.close()
    return render_template("doc/news.html", news = news)

@app.route('/nurse_news')
def nurse_news():
    if 'email' not in session or session.get('role', '') != 'nur':
        return redirect(url_for('signin'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM news")
    news = cur.fetchall()
    cur.close()
    return render_template("nurse/news.html", news = news)

@app.route('/patient_list')
def patient_list():
    if 'email' not in session or session.get('role', '') != 'doc':
        return redirect(url_for('signin'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM patient")
    patient = cur.fetchall()
    cur.close()
    return render_template('doc/patient_list.html', patient = patient)

@app.route('/nursepatient_list')
def nursepatient_list():
    if 'email' not in session or session.get('role', '') != 'nur':
        return redirect(url_for('signin'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM patient")
    patient = cur.fetchall()
    cur.close()
    return render_template('nurse/patient_list.html', patient = patient)

@app.route('/prescription', methods=['GET', 'POST'])
def prescription():
    if 'email' not in session or session.get('role', '') != 'doc':
        return redirect(url_for('signin'))
    if request.method == "POST":
        name = request.form["patient_search"]
        pres = request.form["prescription"]
        cur0 = mysql.connection.cursor()
        cur0.execute("INSERT INTO prescriptions (Name, Prescription) VALUES (%s, %s)", (name, pres))
        mysql.connection.commit()
        cur0.close()
    return render_template('doc/prescription.html')

@app.route('/recommendation', methods=['GET', 'POST'])
def recommendation():
    if 'email' not in session or session.get('role', '') != 'doc':
        return redirect(url_for('signin'))
    if request.method == "POST":
        name = request.form["patient_search"]
        reco = request.form["recommendation"]
        cur0 = mysql.connection.cursor()
        cur0.execute("INSERT INTO recommendation (Name, Recommendation) VALUES (%s, %s)", (name, reco))
        mysql.connection.commit()
        cur0.close()
    return render_template('doc/recommendation.html')

@app.route('/rec')
def rec():
    if 'email' not in session or session.get('role', '') != 'pat':
        return redirect(url_for('signin'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM recommendation")
    rec = cur.fetchall()
    cur.close()
    return render_template('patient/rec.html', rec = rec)

@app.route('/nurse_pre')
def nurse_pre():
    if 'email' not in session or session.get('role', '') != 'nur':
        return redirect(url_for('signin'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM prescriptions")
    pres = cur.fetchall()
    cur.close()
    return render_template('nurse/prescription.html', pres = pres)


@app.route('/stats')
def stats():
    if 'email' not in session or session.get('role', '') != 'pat':
        return redirect(url_for('signin'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM doctors")
    fetchdata = cur.fetchall()
    cur.close()
    return render_template('patient/stats.html', fetchdata = fetchdata)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    if 'email' not in session or session.get('role', '') != 'adm':
        return redirect(url_for('signin'))
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM patient WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('add_patient'))

@app.route('/dele/<int:id>', methods=['GET', 'POST'])
def dele(id):
    if 'email' not in session or session.get('role', '') != 'adm':
        return redirect(url_for('signin'))
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM doctors WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('new_account'))

@app.route('/delnur/<int:id>', methods=['GET', 'POST'])
def delenur(id):
    if 'email' not in session or session.get('role', '') != 'adm':
        return redirect(url_for('signin'))
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM nurse WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('new_nurse'))

@app.route('/new_nurse', methods=['GET', 'POST'])
def new_nurse():
    if 'email' not in session or session.get('role', '') != 'adm':
        return redirect(url_for('signin'))
    if request.method == "POST":
        name = request.form["first_name"] + ' ' + request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]
        cur0 = mysql.connection.cursor()
        cur0.execute("INSERT INTO nurse (Name, Email, Password) VALUES (%s, %s, %s)", (name, email, password))
        mysql.connection.commit()
        cur0.close()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM nurse")
    nurse = cur.fetchall()
    cur.close()
    return render_template('admin/admin_tool/new_nurse.html', nurse = nurse)

@app.route('/signout')
def signout():
    session.pop('email', None)
    return redirect(url_for('signin'))

if __name__ == "__main__":
    app.run(debug=True)

