import sqlite3


def init_db():
    with sqlite3.connect("log.db") as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS challenges (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, method TEXT, challenge TEXT)")
        conn.commit()

def showDB(filter):
    with sqlite3.connect("log.db") as conn:
        c = conn.cursor()
        if(filter == "*"):
            c.execute("SELECT * FROM challenges")
        else:
            c.execute(f'SELECT * FROM challenges WHERE challenge="{filter}"')
        challenges = c.fetchall()
        print("id,      username,     password,     method,      challenge")
        for challenge in challenges:
            print(challenge)
        conn.commit()

def addEntry(username, password, method, challenge):
    with sqlite3.connect("log.db") as conn:
        c = conn.cursor()
        c.execute(f'INSERT INTO challenges (username, password, method, challenge) VALUES("{username}", "{password}", "{method}", "{challenge}")')
        conn.commit()

def removeEntry(isAll):
    with sqlite3.connect("log.db") as conn:
        c = conn.cursor()
        if(isAll):
            c.execute("DELETE FROM sqlite_sequence")
            c.execute(f'DELETE FROM challenges')
        else:
            c.execute("SELECT * FROM challenges ORDER BY id")
            challenges = c.fetchall()
            id = challenges[len(challenges)-1][0];
            c.execute(f'DELETE FROM challenges WHERE id={id}')
            id = id-1;
            c.execute(f'UPDATE sqlite_sequence SET seq={id}')
        conn.commit()

def modifyEntry(id, selection, modifiedValue):
    with sqlite3.connect("log.db") as conn:
        c = conn.cursor()
        if(selection == "username"):
            c.execute(f'UPDATE challenges SET username="{modifiedValue}" WHERE id={id}')
        elif(selection == "password"):
            c.execute(f'UPDATE challenges SET password="{modifiedValue}" WHERE id={id}')
        elif(selection == "method"):
            c.execute(f'UPDATE challenges SET method="{modifiedValue}" WHERE id={id}')
        elif(selection == "challenge"):
            c.execute(f'UPDATE challenges SET challenge="{modifiedValue}" WHERE id={id}')
        else:
            print("selection is not a possible value please retry")
        conn.commit()

def modifyEntireEntry(id, modifiedUsername, modifiedPassword, modifiedMethod, modifiedChallenge):
    partsOfEntry = ["username", "password", "method", "challenge"]
    partsOfModifiedEntry = [modifiedUsername, modifiedPassword, modifiedMethod, modifiedChallenge]
    for i in range(0,4):
        modifyEntry(id, partsOfEntry[i], partsOfModifiedEntry[i])

init_db()
continueLoop = False
filter = "*"
while(not continueLoop):
    showDB(filter)
    print("1. filter DB")
    print("2. add entry")
    print("3. remove last entry")
    print("4. remove all entries")
    print("5. modify an entry")
    print("")
    choice = int(input("What do you want to do: "))
    if(choice == 1):
        filter = (input("What challenge do you want to see: "))
    elif(choice == 2):
        username = (input("What is your username: "))
        password = (input("What is your password: "))
        method = (input("What is your method: "))
        challenge = (input("What is your challenge: "))
        addEntry(username, password, method, challenge)
    elif(choice == 3):
        removeEntry(False)
    elif(choice == 4):
        removeEntry(True)
    elif(choice == 5):
        choice2 = bool(input("Do you want a specific value to be modified (type anything for the entire entry); "))
        if(not choice2):
            choice3 = (input("What value do you want to modify a value: "))
            id = int(input("What is the id of the entry you want to modify: "))
            modifiedValue = (input("What is the updated value: "))
            modifyEntry(id, choice3, modifiedValue)
        else:
            id = int(input("What is the id of the entry you want to modify: "))
            modifiedUsername = (input("What is the updated username: "))
            modifiedPassword = (input("What is the updated password: "))
            modifiedMethod = (input("What is the updated method: "))
            modifiedChallenge = (input("What is the updated challenge: "))
            modifyEntireEntry(id, modifiedUsername, modifiedPassword, modifiedMethod, modifiedChallenge)
    else:
        continueLoop = True
        break
    showDB(filter)
    continueLoop = bool(input("Press enter to continue or type anything to exit: "))
print("Logs are stored in log.db thank you for using this tool: ")



