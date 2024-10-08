from flask import Flask, request, render_template, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'something'

app.config['MYSQL_HOST'] = 'sql7.freesqldatabase.com'
app.config['MYSQL_USER'] = 'sql7731106'
app.config['MYSQL_PASSWORD'] = 'GYuPgfN1Cx'
app.config['MYSQL_DB'] = 'sql7731106'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'BGPHMS@gmail.com'
app.config['MAIL_PASSWORD'] = 'vjkcslwthvdgerod'

mysql = MySQL(app)
mail = Mail(app)

def send_email(subject, recipient_email, email_content):
    msg = Message(subject = subject,
                  recipients=[recipient_email],
                  sender=app.config.get("MAIL_USERNAME"))
    msg.body = email_content
    mail.send(msg)

# def emergency():
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM patient_info")
#     data = cur.fetchall()
#     for item in data:
#         if item[1] > 100:
#             send_email('yoseph.kedir10@gmail.com', 'Your patient is in emergency!!!')


# schedule.every(1).minutes.do(emergency)
# while True:
#     schedule.run_pending()
#     time.sleep(1)

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
               
    return render_template("index.html")


@app.route("/admin_about")
def admin_about():
    if 'email' not in session or session.get('role', '') != 'adm':
        return redirect(url_for('home'))
    return render_template('admin/about.html')

@app.route("/doctor_about")
def doctor_about():
    if 'email' not in session or session.get('role', '') != 'doc':
        return redirect(url_for('home'))
    return render_template('doc/about.html')

@app.route("/nurse_about")
def nurse_about():
    if 'email' not in session or session.get('role', '') != 'nur':
        return redirect(url_for('home'))
    return render_template('nurse/about.html')

@app.route("/pat_about")
def pat_about():
    if 'email' not in session or session.get('role', '') != 'pat':
        return redirect(url_for('home'))
    return render_template('patient/about.html')

@app.route("/pat_Amhabout")
def pat_Amhabout():
    if 'email' not in session or session.get('role', '') != 'pat':
        return redirect(url_for('home'))
    return render_template('patient/Amh-about.html')

@app.route('/admin')
def admin():
    if 'email' not in session or session.get('role', '') != 'adm':
        return redirect(url_for('home'))

    return render_template('admin/admin.html')

@app.route('/doctor')
def doctor():
    if 'email' not in session or session.get('role', '') != 'doc':
        return redirect(url_for('home'))

    return render_template('doc/doctor.html')

@app.route('/nurse')
def nurse():
    if 'email' not in session or session.get('role', '') != 'nur':
        return redirect(url_for('home'))

    return render_template('nurse/nurse.html')

@app.route('/patient')
def patient():
    if 'email' not in session or session.get('role', '') != 'pat':
        return redirect(url_for('home'))
    return render_template('patient/patient.html')

@app.route('/Amhpatient')
def Amhpatient():
    if 'email' not in session or session.get('role', '') != 'pat':
        return redirect(url_for('home'))
    return render_template('patient/Amh-patient.html')

@app.route('/<name>')
def lost(name):
    return redirect(url_for('home'))

@app.route('/new_account', methods=['GET', 'POST'])
def new_account():
    if 'email' not in session or session.get('role', '') != 'adm':
        return redirect(url_for('home'))
    if request.method == "POST":
        name = request.form["first_name"] + ' ' + request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]
        cur0 = mysql.connection.cursor()
        cur0.execute("INSERT INTO doctors (Name, Email, Password) VALUES (%s, %s, %s)", (name, email, password))
        mysql.connection.commit()
        cur0.close()
        send_email('Welcome Doctor', email, 'We are pleased to inform you that you have been added to the hospitals health monitoring system.') 
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM doctors")
    doctors = cur.fetchall()
    cur.close()
    return render_template('admin/admin_tool/new_account.html', doctors = doctors)

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if 'email' not in session or session.get('role', '') != 'adm':
        return redirect(url_for('home'))
    if request.method == "POST":
        name = request.form["first_name"] + ' ' + request.form["last_name"]
        name1 = request.form["first_name"] + request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]
        cur0 = mysql.connection.cursor()
        cur0.execute("INSERT INTO patient (Name, Email, Password) VALUES (%s, %s, %s)", (name, email, password))
        mysql.connection.commit()
        cur0.close()   
        # cur1 = mysql.connection.cursor()
        # cur1.execute("CREATE TABLE %s (day DATE NOT NULL,temperature FLOAT NOT NULL,pulse_rate INT NOT NULL,blood_pressure VARCHAR(10) NOT NULL);" % name1)
        # mysql.connection.commit()
        # cur1.close() 
        send_email('Welcome Patient', email, 'We are pleased to inform you that you have been enrolled in our health monitoring system, which will help you keep track of your health status from the comfort of your own home.Thank you for choosing us for your health monitoring needs. We look forward to helping you take control of your health.')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM patient")
    patient = cur.fetchall()
    cur.close()
    return render_template('admin/admin_tool/add_patient.html', patient = patient)

@app.route('/admin_news', methods=['GET', 'POST'])
def admin_news():
    if 'email' not in session or session.get('role', '') != 'adm':
        return redirect(url_for('home'))
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
        return redirect(url_for('home'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM news")
    news = cur.fetchall()
    cur.close()
    return render_template("doc/news.html", news = news)

@app.route('/nurse_news')
def nurse_news():
    if 'email' not in session or session.get('role', '') != 'nur':
        return redirect(url_for('home'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM news")
    news = cur.fetchall()
    cur.close()
    return render_template("nurse/news.html", news = news)

@app.route('/patient_list')
def patient_list():
    if 'email' not in session or session.get('role', '') != 'doc':
        return redirect(url_for('home'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM patient")
    patient = cur.fetchall()
    cur.close()
    return render_template('doc/patient_list.html', patient = patient)

@app.route('/nursepatient_list')
def nursepatient_list():
    if 'email' not in session or session.get('role', '') != 'nur':
        return redirect(url_for('home'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM patient")
    patient = cur.fetchall()
    cur.close()
    return render_template('nurse/patient_list.html', patient = patient)

@app.route('/prescription', methods=['GET', 'POST'])
def prescription():
    if 'email' not in session or session.get('role', '') != 'doc':
        return redirect(url_for('home'))
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
        return redirect(url_for('home'))
    if request.method == "POST":
        name = request.form["patient_search"]
        reco = request.form["recommendation"]
        cur0 = mysql.connection.cursor()
        cur0.execute("INSERT INTO recommendation (Name, Recommendation) VALUES (%s, %s)", (name, reco))
        mysql.connection.commit()
        cur0.close()
    return render_template('doc/recommendation.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'email' not in session or session.get('role', '') != 'pat':
        return redirect(url_for('home'))
    if request.method == "POST":
        name = session['email']
        feedb = request.form["feedback"]
        cur0 = mysql.connection.cursor()
        cur0.execute("INSERT INTO feedback (Name, Feedback) VALUES (%s, %s)", (name, feedb))
        mysql.connection.commit()
        cur0.close()
    return render_template('patient/feedback.html')

@app.route('/Amhfeedback', methods=['GET', 'POST'])
def Amhfeedback():
    if 'email' not in session or session.get('role', '') != 'pat':
        return redirect(url_for('home'))
    if request.method == "POST":
        name = session['email']
        feedb = request.form["feedback"]
        cur0 = mysql.connection.cursor()
        cur0.execute("INSERT INTO feedback (Name, Feedback) VALUES (%s, %s)", (name, feedb))
        mysql.connection.commit()
        cur0.close()
    return render_template('patient/Amh-feedback.html')

@app.route('/rec')
def rec():
    if 'email' not in session or session.get('role', '') != 'pat':
        return redirect(url_for('home'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM recommendation")
    rec = cur.fetchall()
    cur.close()
    return render_template('patient/rec.html', rec = rec)

@app.route('/Amhrec')
def Amhrec():
    if 'email' not in session or session.get('role', '') != 'pat':
        return redirect(url_for('home'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM recommendation")
    rec = cur.fetchall()
    cur.close()
    return render_template('patient/Amh-rec.html', rec = rec)

@app.route('/feed')
def feed():
    if 'email' not in session or session.get('role', '') != 'doc':
        return redirect(url_for('home'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM feedback")
    feed = cur.fetchall()
    cur.close()
    return render_template('doc/feedback.html', feed = feed)

@app.route('/nurse_pre')
def nurse_pre():
    if 'email' not in session or session.get('role', '') != 'nur':
        return redirect(url_for('home'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM prescriptions")
    pres = cur.fetchall()
    cur.close()
    return render_template('nurse/prescription.html', pres = pres)


@app.route('/stats')
def stats():
    if 'email' not in session or session.get('role', '') != 'pat':
        return redirect(url_for('home'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM patient_info")
    fetchdata = cur.fetchall()
    cur.close()
    return render_template('patient/stats.html', fetchdata = fetchdata)

@app.route('/Amhstats')
def Amhstats():
    if 'email' not in session or session.get('role', '') != 'pat':
        return redirect(url_for('home'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM patient_info")
    fetchdata = cur.fetchall()
    cur.close()
    return render_template('patient/Amh-stats.html', fetchdata = fetchdata)

@app.route('/nurstats')
def nurstats():
    if 'email' not in session or session.get('role', '') != 'nur':
        return redirect(url_for('home'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM patient_info")
    fetchdata = cur.fetchall()
    cur.close()
    return render_template('nurse/stats.html', fetchdata = fetchdata)

@app.route('/docstats')
def docstats():
    if 'email' not in session or session.get('role', '') != 'doc':
        return redirect(url_for('home'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM patient_info")
    fetchdata = cur.fetchall()
    cur.close()
    return render_template('doc/stats.html', fetchdata = fetchdata)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    if 'email' not in session or session.get('role', '') != 'adm':
        return redirect(url_for('home'))
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM patient WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('add_patient'))

@app.route('/dele/<int:id>', methods=['GET', 'POST'])
def dele(id):
    if 'email' not in session or session.get('role', '') != 'adm':
        return redirect(url_for('home'))
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM doctors WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('new_account'))

@app.route('/delnur/<int:id>', methods=['GET', 'POST'])
def delenur(id):
    if 'email' not in session or session.get('role', '') != 'adm':
        return redirect(url_for('home'))
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM nurse WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('new_nurse'))

@app.route('/new_nurse', methods=['GET', 'POST'])
def new_nurse():
    if 'email' not in session or session.get('role', '') != 'adm':
        return redirect(url_for('home'))
    if request.method == "POST":
        name = request.form["first_name"] + ' ' + request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]
        cur0 = mysql.connection.cursor()
        cur0.execute("INSERT INTO nurse (Name, Email, Password) VALUES (%s, %s, %s)", (name, email, password))
        mysql.connection.commit()
        cur0.close()
        send_email('Welcome Nurse', email, 'We are pleased to inform you that you have been added to the hospitals health monitoring system.') 
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM nurse")
    nurse = cur.fetchall()
    cur.close()
    return render_template('admin/admin_tool/new_nurse.html', nurse = nurse)

@app.route('/signout')
def signout():
    session.pop('email', None)
    session.pop('role', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)