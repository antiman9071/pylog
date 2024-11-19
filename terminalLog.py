import sqlite3
import sys


file = sys.argv[1]
def init_db():
    with sqlite3.connect(file) as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS challenges (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, method TEXT, challenge TEXT)")
        conn.commit()

def pad(output, charCount, LoR):
    if(len(str(output)) < charCount):
        for i in range(charCount - len(str(output))-1):
            if LoR : 
                output = " " + str(output)
            else:
                output = str(output) + " "
    return output

def showDB(filter):
    with sqlite3.connect(file) as conn:
        c = conn.cursor()
        if(filter == "*"):
            c.execute("SELECT * FROM challenges")
        else:
            c.execute(f'SELECT * FROM challenges WHERE challenge="{filter}"')
        header = ("id", "username", "password", "method", "challenge")
        print(pad(header[0], 5, False) + "|" + pad(header[1], 20, False) + "|" + pad(header[2], 20, False) + "|" + pad(header[3], 20, False) + "|" + pad(header[4], 20, False))
        challenges = c.fetchall()
        for challenge in challenges:
            output = pad(challenge[0], 5, False) + "|" + pad(challenge[1], 20, False) + "|" + pad(challenge[2], 20, False) + "|" + pad(challenge[3], 20, False) + "|" + pad(challenge[4], 20, False)
            print(output)
        conn.commit()

def search(idOrUser, searchTerm, isPrinting):
    with sqlite3.connect(file) as conn:
        c = conn.cursor()
        if idOrUser:
            c.execute(f'SELECT * FROM challenges WHERE id="{searchTerm}"')
        else:
            c.execute(f'SELECT * FROM challenges WHERE username="{searchTerm}"')
        challenges = c.fetchall()
        if isPrinting:
            header = ("id", "username", "password", "method", "challenge")
            print(pad(header[0], 5, False) + "|" + pad(header[1], 20, False) + "|" + pad(header[2], 20, False) + "|" + pad(header[3], 20, False) + "|" + pad(header[4], 20, False))
            for challenge in challenges:
                output = pad(challenge[0], 5, False) + "|" + pad(challenge[1], 20, False) + "|" + pad(challenge[2], 20, False) + "|" + pad(challenge[3], 20, False) + "|" + pad(challenge[4], 20, False)
                print(output)
        else:
            return challenges
        conn.commit()


def addEntry(username, password, method, challenge):
    with sqlite3.connect(file) as conn:
        c = conn.cursor()
        c.execute(f'INSERT INTO challenges (username, password, method, challenge) VALUES("{username}", "{password}", "{method}", "{challenge}")')
        conn.commit()

def removeEntry(isAll):
    with sqlite3.connect(file) as conn:
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
    with sqlite3.connect(file) as conn:
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
if __name__ == "__main__":
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
        print("5. modify an entry")
        print("6. search for entry")
        print("")
        choice = int(input("What do you want to do: "))
        if(choice == 1):
            showDBBool = True 
            filter = (input("What challenge do you want to see: "))
        elif(choice == 2):
            showDBBool = True
            username = (input("What is your username: "))
            password = (input("What is your password: "))
            method = (input("What is your method: "))
            challenge = (input("What is your challenge: "))
            addEntry(username, password, method, challenge)
        elif(choice == 3):
            showDBBool = True
            removeEntry(False)
        elif(choice == 4):
            showDBBool = True
            removeEntry(True)
        elif(choice == 5):
            showDBBool = False
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
        elif(choice == 6):
            showDBBool = False
            idOrUserInput = int(input("What are you looking for(id(0) or username(1)) "))
            if idOrUserInput == 0:
                searchTermInput = input("What is the id you are looking for ")
                search(True, searchTermInput, True)
            elif idOrUserInput == 1:
                searchTermInput = input("What is the username you are looking for ")
                search(False, searchTermInput, True)
            else:
                print("Sorry that input is not supported please run again")
        else:
            continueLoop = True
            break
        if showDBBool:
            showDB(filter)
        continueLoop = bool(input("Press enter to continue or type anything to exit: "))
    print("Logs are stored in log.db thank you for using this tool: ")



