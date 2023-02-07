from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

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
        cur.execute("SELECT Email FROM doctors")
        doctors = cur.fetchall()
        cur.close()
        doctor = [row[0] for row in doctors]
        cur1 = mysql.connection.cursor()
        cur1.execute("SELECT Email FROM nurse")
        nurses = cur1.fetchall()
        cur1.close()
        nurse = [row[0] for row in nurses]
        cur2 = mysql.connection.cursor()
        cur2.execute("SELECT Email FROM patient")
        patients = cur2.fetchall()
        cur2.close()
        patient = [row[0] for row in patients]
        if email in doctor:
            return redirect(url_for("doctor"))
        if email in nurse:
            return redirect(url_for("nurse"))
        if email in patient:
            return redirect(url_for('patient'))
               
    return render_template("signin.html")

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/admin_about")
def admin_about():
    return render_template('admin/about.html')

@app.route("/doctor_about")
def doctor_about():
    return render_template('doc/about.html')

@app.route('/admin')
def admin():
    if False:
        return redirect(url_for('home'))

    return render_template('admin/admin.html')

@app.route('/doctor')
def doctor():
    if False:
        return redirect(url_for('home'))

    return render_template('doc/doctor.html')

@app.route('/nurse')
def nurse():
    if False:
        return redirect(url_for('home'))

    return render_template('nurse/nurse.html')

@app.route('/patient')
def patient():
    if False:
        return redirect(url_for('home'))

    return render_template('patient/patient.html')

@app.route('/<name>')
def lost(name):
    return redirect(url_for('home'))

@app.route('/new_account', methods=['GET', 'POST'])
def new_account():
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

@app.route('/news')
def news():
    return render_template("news.html")

@app.route('/admin_news')
def admin_news():
    return render_template("admin/news.html")

@app.route('/doctor_news')
def doctor_news():
    return render_template("doc/news.html")

@app.route('/patient_list')
def patient_list():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM patient")
    patient = cur.fetchall()
    cur.close()
    return render_template('doc/patient_list.html', patient = patient)

@app.route('/prescription', methods=['GET', 'POST'])
def prescription():
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
    if request.method == "POST":
        name = request.form["patient_search"]
        reco = request.form["recommendation"]
        cur0 = mysql.connection.cursor()
        cur0.execute("INSERT INTO recommendation (Name, Recommendation) VALUES (%s, %s)", (name, reco))
        mysql.connection.commit()
        cur0.close()
    return render_template('doc/recommendation.html')

@app.route('/nurse_pre')
def nurse_pre():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM prescriptions")
    pres = cur.fetchall()
    cur.close()
    return render_template('nurse/prescription.html', pres = pres)


@app.route('/stats')
def stats():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM doctors")
    fetchdata = cur.fetchall()
    cur.close()
    return render_template('patient/stats.html', fetchdata = fetchdata)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM patient WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('add_patient'))

@app.route('/dele/<int:id>', methods=['GET', 'POST'])
def dele(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM doctors WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('new_account'))

@app.route('/delnur/<int:id>', methods=['GET', 'POST'])
def delenur(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM nurse WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('new_nurse'))

@app.route('/new_nurse', methods=['GET', 'POST'])
def new_nurse():
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


if __name__ == "__main__":
    app.run(debug=True)

