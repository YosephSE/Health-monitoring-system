from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        username = request.form["email"]
        password = request.form["password"]
        
        return redirect(url_for("home"))
        
    return render_template("signup.html")

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        username = request.form["email"]
        password = request.form["password"]
        
        return redirect(url_for("home"))
        
    return render_template("signin.html")

@app.route("/about")
def about():
    return render_template('about.html')

@app.route('/admin')
def admin():
    if False:
        return redirect(url_for('home'))

    return render_template('admin.html')

@app.route('/doctor')
def doctor():
    if False:
        return redirect(url_for('home'))

    return render_template('doctor.html')

@app.route('/nurse')
def nurse():
    if False:
        return redirect(url_for('home'))

    return render_template('nurse.html')

@app.route('/patient')
def patient():
    if False:
        return redirect(url_for('home'))

    return render_template('patient.html')

@app.route('/<name>')
def lost(name):
    return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(debug=True)
