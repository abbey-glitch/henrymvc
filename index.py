from flask import Flask, render_template, request, url_for, redirect, flash, jsonify, session
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from flask_mail import Message, Mail
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "password"
app.config["MYSQL_DB"] = "marvel"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# configure app to use mail
# Configure Flask-Mail settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Your mail server
app.config['MAIL_PORT'] = 587  # Port for TLS/STARTTLS
app.config['MAIL_USE_TLS'] = True  # Enable TLS
app.config['MAIL_USERNAME'] = 'abiodunonaolapi@gmail.com'  # Your email
app.config['MAIL_PASSWORD'] = 'bmdvbgxapdhjeino'  # Your email password
app.config['MAIL_DEFAULT_SENDER'] = 'abiodunonaolapi@gmail.com'  # Default sender (optional)
subject = "Test Emai"
mail = Mail(app)


UPLOAD_FOLDER = "static/assets/images"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'}

mysql = MySQL(app)


# register route
@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if(request.method == "POST"):
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        passhash = sha256_crypt.encrypt(password)
        # send mail
        msg = Message(subject,
                  recipients= [email],
                  sender=app.config['MAIL_DEFAULT_SENDER'])
        msg.body = "thanks for registering"  # Plain text body
        # msg.html = render_template('email_template.html', message=message_body)  # HTML body
        try:
            mail.send(msg)
            info = 'Email sent successfully!'
            if(info):
                dbcon = mysql.connection.cursor()
                if(dbcon):
                    sql = f"""
                    INSERT INTO user(username, password, email) VALUES(%s, %s, %s)"""
                    dbcon.execute(sql, (username, passhash, email))
                    mysql.connection.commit()
                    return render_template("sign.html")
                error = f"unable to connect to database"
                return render_template("sign.html", error = error)
            return jsonify(info)
        except Exception as e:
            return str(e)
        # end email send notification
    else:
        error = f"wrong request method"
        return render_template("reg.html", error = error)


# login route
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if(request.method == "POST"):
        email = request.form["email"]
        password = request.form["password"]
        cursor = mysql.connection.cursor()
        if(cursor):
            # return("success")
            sql = f"""
            SELECT * FROM user WHERE email = %s"""
            result = cursor.execute(sql, (email,))
            feedback = cursor.fetchone()
            if(feedback):
                username = feedback["username"]
                email = feedback["email"]
                passwordDb = feedback["password"]
                if(sha256_crypt.verify(password, passwordDb)):
                    session['logged_in'] = True
                    session['email'] = email 
                    flash("You are now logged in", "success")
                    return(render_template("dashboard.html", username = username))
                    
                # return(jsonify(feedback["email"]))
            # cursor.connection.commit()
            # cursor.close()
            # return("hello")
            # return(jsonify(result))
        return(render_template("sign.html"))
    else:
        return render_template("sign.html", error = error)
# imageupload route
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/imageupload", methods=["GET", "POST"])
def imageupload():
    if(request.method == "GET"):
        return render_template("imageupload.html")
    if(request.method == "POST"):
        file = request.files['image']
        # print(file)
        # return("success")
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return("image uploaded successfully")
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
        
# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         if 'file1' not in request.files:
#             return 'there is no file1 in form!'
#         file1 = request.files['file1']
#         path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
#         file1.save(path)
#         return path

    # return render_template("imageupload.html")
# update route
@app.route("/update-user", methods=["GET", "POST"])
def updateUser():
    if(request.method == "POST"):
        username = request.form['username']
        # return jsonify(username)
        email = request.form["email"]
        cursor = mysql.connection.cursor()
        if(cursor):
            sql = f"""
            UPDATE user SET username = %s, email = %s WHERE email = %s"""
            cursor.execute(sql, (username, email, session['email']))
            mysql.connection.commit()
            cursor.close()
            return("updated successfully")
    else:
        return render_template("update.html")
        

if(__name__ == "__main__"):
    app.secret_key = "20cb9ac3807fdb8cfce0f2e1a5fe4614459b09f3ad92bb7cc2613582386909f8"
    app.run(debug=True)