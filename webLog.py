from flask import Flask, render_template, url_for, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect("log.db") as conn:
        c = conn.cursor()
        c. execute("CREATE TABLE IF NOT EXISTS challenges (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, method TEXT, challenge TEXT)")
        conn.commit()

@app.route('/', methods=['GET'])
def index():
    with sqlite3.connect("log.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM challenges ORDER BY id")
        challenges = c.fetchall()
    return render_template('index.html', challenges=challenges)

@app.route('/', methods=['POST'])
def add_challenge():
    if request.method == 'POST':
        usernameEntry = request.form['username']
        passwordEntry = request.form['passwd']
        methodEntry = request.form['method']
        challengeEntry = request.form['challenge']

        with sqlite3.connect("log.db") as conn:
            c = conn.cursor()
            c.execute(f'INSERT INTO challenges (username, password, method, challenge) VALUES("{usernameEntry}", "{passwordEntry}", "{methodEntry}", "{challengeEntry}")')
            conn.commit()
        return redirect(url_for('index'))
    return render_template('index.html')
@app.route('/remove', methods=['POST'])
def removeChallenge():
    with sqlite3.connect("log.db") as conn:
        if request.method == 'POST':
            c = conn.cursor()
            c.execute("SELECT * FROM challenges ORDER BY id")
            challenges = c.fetchall()
            id = challenges[len(challenges)-1][0];
            c.execute(f'DELETE FROM challenges WHERE id={id}')
            id = id-1;
            c.execute(f'UPDATE sqlite_sequence SET seq={id}')
            conn.commit()
        return redirect(url_for('index'))
    return render_template('index.html')
@app.route('/removeAll', methods=['POST'])
def removeAllChallenges():
    with sqlite3.connect("log.db") as conn:
        if request.method == 'POST':
            c = conn.cursor()
            c.execute("DELETE FROM sqlite_sequence")
            c.execute(f'DELETE FROM challenges')
            conn.commit()
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/changeUser', methods=['POST'])
def changeUserName():
    with sqlite3.connect("log.db") as conn:
        if request.method == 'POST':
            usernameEntry = request.form['usernameChange']
            idEntry = request.form['id']
            c = conn.cursor()
            c.execute(f'UPDATE challenges SET username="{usernameEntry}" WHERE id={idEntry}')
            conn.commit()
        return redirect(url_for('index'))
    return render_template('index.html')
@app.route('/changePassword', methods=['POST'])
def changePasswd():
    with sqlite3.connect("log.db") as conn:
        if request.method == 'POST':
            passwordEntry = request.form['passwordChange']
            idEntry = request.form['id']
            c = conn.cursor()
            c.execute(f'UPDATE challenges SET password="{passwordEntry}" WHERE id={idEntry}')
            conn.commit()
        return redirect(url_for('index'))
    return render_template('index.html')
@app.route('/changeMethod', methods=['POST'])
def changeMethod():
    with sqlite3.connect("log.db") as conn:
        if request.method == 'POST':
            methodEntry = request.form['methodChange']
            idEntry = request.form['id']
            c = conn.cursor()
            c.execute(f'UPDATE challenges SET method="{methodEntry}" WHERE id={idEntry}')
            conn.commit()
        return redirect(url_for('index'))
    return render_template('index.html')
@app.route('/changeChallenge', methods=['POST'])
def changeChallenge():
    with sqlite3.connect("log.db") as conn:
        if request.method == 'POST':
            challengeEntry = request.form['challengeChange']
            idEntry = request.form['id']
            c = conn.cursor()
            c.execute(f'UPDATE challenges SET challenge="{challengeEntry}" WHERE id={idEntry}')
            conn.commit()
        return redirect(url_for('index'))
    return render_template('index.html')
@app.route('/filterChallenge', methods=['POST','GET'])
def filterChallenges():
    with sqlite3.connect("log.db") as conn:
        challengeEntry = '*'
        if request.method == 'POST':
            challengeEntry = request.form['challengeFilter']
        c = conn.cursor()
        c.execute(f'SELECT * FROM challenges WHERE challenge="{challengeEntry}" ORDER BY id')
        challenges = c.fetchall()
    return render_template('index.html', filteredChallenges=challenges)
@app.route('/searchChallenges', methods=['POST', 'GET'])
def searchChallenges():
    with sqlite3.connect("log.db") as conn:
        searchTerm = '*'
        if request.method == 'POST':
            option = request.form['searchTermChoice']
            searchTerm = request.form['searchTerm']
        c = conn.cursor()
        if option == "ID":
            c.execute(f'SELECT * FROM challenges WHERE id="{searchTerm}"')
        elif option == "Username":
            c.execute(f'SELECT * FROM challenges WHERE username="{searchTerm}"')
        challenges = c.fetchall()
    return render_template('index.html', filteredChallenges=challenges)

init_db()
app.run(host="0.0.0.0", port=80)
