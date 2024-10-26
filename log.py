from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///log.db"
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

class log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), default=f'Bandit{id}')
    password = db.Column(db.String(200), nullable = False, default='test')
    method = db.Column(db.String(200), nullable = False, default='test')
    def __repr__(self):
        return '<Challenege %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        log_id = request.form['id']
        log_passwd = request.form['password']
        log_method = request.form['method']
        new_id = log(id=log_id)
        new_passwd= log(password=log_passwd)
        new_method = log(method=log_method)

        try:
            db.session.add(new_id)
            db.session.add(new_passwd)
            db.session.add(new_method)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"There was an error\n{e}"
        
    else:
        logs = log.query.order_by(log.id).all()
        return render_template('index.html', logs=logs)

app.run(host="0.0.0.0", port=80)
