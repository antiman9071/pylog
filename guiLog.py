from tkinter import * 
from tkinter import ttk 
from tkinter import simpledialog 
import sqlite3 
from terminalLog import addEntry, removeEntry, modifyEntry, modifyEntireEntry, pad, search
def init_db(): 
    with sqlite3.connect("log.db") as conn: 
        c = conn.cursor() 
        c.execute("CREATE TABLE IF NOT EXISTS challenges (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, method TEXT, challenge TEXT)") 
        conn.commit() 

def guiPrintLine(textBox, output): 
    textBox['state'] = 'normal' 
    textBox.insert(END, output) 
    textBox.insert(END, "\n")
    textBox['state'] = 'disabled'



def showDB(filter, textBox):
    header = ("id", "username", "password", "method", "challenge")
    text = [header]
    with sqlite3.connect("log.db") as conn:
        c = conn.cursor()
        if(filter == "*"):
            c.execute("SELECT * FROM challenges")
        else:
            c.execute(f'SELECT * FROM challenges WHERE challenge="{filter}"')
        challenges = c.fetchall()
        for challenge in challenges:
            text.append(challenge)
        conn.commit()
    for line in text:
        output = pad(line[0], 5, False) + "|" + pad(line[1], 20, False) + "|" + pad(line[2], 20, False) + "|" + pad(line[3], 20, False) + "|" + pad(line[4], 20, False)
        guiPrintLine(textBox, output)

def refresh():
    OutputDB['state'] = 'normal'
    OutputDB.delete("1.0", "end")
    OutputDB['state'] = 'disabled'

def addButton():
    username = simpledialog.askstring(title="Enter a username", prompt="Enter a username")
    password = simpledialog.askstring(title="Enter a password", prompt="Enter a password")
    method = simpledialog.askstring(title="Enter a method", prompt="Enter a method")
    challenge = simpledialog.askstring(title="Enter a challenge", prompt="Enter a challenge")
    if bool(username) and bool(password) and bool(method) and bool(challenge):
        addEntry(username, password, method, challenge)
        with sqlite3.connect("log.db") as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM challenges ORDER BY id")
            challenges = c.fetchall()
            lastChallenge = challenges[len(challenges)-1]
        output = pad(lastChallenge[0], 5, False) + "|" + pad(lastChallenge[1], 20, False) + "|" + pad(lastChallenge[2], 20, False) + "|" + pad(lastChallenge[3], 20, False) + "|" + pad(lastChallenge[4], 20, False)
        guiPrintLine(OutputDB, output)

def removeButton():
    removeEntry(False)
    OutputDB['state'] = 'normal'
    OutputDB.delete("end-2c linestart", "end")
    OutputDB.insert(END, "\n")
    OutputDB['state'] = 'disabled'

def removeAllButton():
    removeEntry(True)
    refresh()
    header = ("id", "username", "password", "method", "challenge")
    output = pad(header[0], 5, False) + "|" + pad(header[1], 20, False) + "|" + pad(header[2], 20, False) + "|" + pad(header[3], 20, False) + "|" + pad(header[4], 20, False)
    guiPrintLine(OutputDB, output)

def modifyButton():
    id = simpledialog.askinteger(title="Enter selection", prompt="What id must be modified")
    choice = simpledialog.askinteger(title="Enter selection", prompt="What value must be modified(1:Username, 2:Password, 3:Method, 4:Challenge, 5:All)")
    if choice == 1:
        username = simpledialog.askstring(title="Enter username", prompt="Enter the new username")
        modifyEntry(id, "username", username)
    elif choice == 2:
        password = simpledialog.askstring(title="Enter password", prompt="Enter the new password")
        modifyEntry(id, "password", password)
    elif choice == 3:
        method = simpledialog.askstring(title="Enter method", prompt="Enter the new method")
        modifyEntry(id, "method", method)
    elif choice == 4:
        challenge = simpledialog.askstring(title="Enter challenge", prompt="Enter the new challenge")
        modifyEntry(id, "challenge", challenge)
    elif choice == 5:
        username = simpledialog.askstring(title="Enter username", prompt="Enter the new username")
        password = simpledialog.askstring(title="Enter password", prompt="Enter the new password")
        method = simpledialog.askstring(title="Enter method", prompt="Enter the new method")
        challenge = simpledialog.askstring(title="Enter challenge", prompt="Enter the new challenge")
        modifyEntireEntry(id, username, password, method, challenge)
    else:
        pass
    refresh()
    showDB(filter, OutputDB)

def setFilter():
    filter = simpledialog.askstring(title="Enter filter", prompt="What challenge do you want to filter by (* for all)")
    refresh()
    showDB(filter, OutputDB)

def searchButton():
    idOrUserInput = simpledialog.askinteger(title="choose type", prompt="What are you looking for(id(0) or username(1))")
    if idOrUserInput == 0:
        searchTermInput = simpledialog.askinteger(title="choose prompt", prompt="What is the id you are looking for")
        challenges = search(True, searchTermInput, False)
    elif idOrUserInput == 1:
        searchTermInput = simpledialog.askstring(title="choose prompt", prompt="What is the username you are looking for")
        challenges = search(False, searchTermInput, False)
    else:
        pass
    refresh()
    header = ("id", "username", "password", "method", "challenge")
    text = [header]
    for challenge in challenges:
        text.append(challenge)
    for line in text:
        output = pad(line[0], 5, False) + "|" + pad(line[1], 20, False) + "|" + pad(line[2], 20, False) + "|" + pad(line[3], 20, False) + "|" + pad(line[4], 20, False)
        guiPrintLine(OutputDB, output)

init_db()

root = Tk()
filter = "*"
Label(root, text="Welcome to CTF Tracker").grid(column=1, row=0)
Label(root, text="Below are your current flags").grid(column=1, row=1)
OutputDB = Text(root, state='disabled', height=11, width=85)
OutputDB.grid(column=0, row=2, columnspan=5)
Button(root, text="Add an entry", command=addButton).grid(column=0, row=0)
Button(root, text="modify an entry", command=modifyButton).grid(column=0, row=1)
Button(root, text="Remove last entry", command=removeButton).grid(column=2, row=0)
Button(root, text="Remove all entries", command=removeAllButton).grid(column=2, row=1)
Button(root, text="filter", command=setFilter).grid(column=3, row=0)
Button(root, text="search", command=searchButton).grid(column=3, row=1)
root.title("CTF Tracker app")
root.title("CTF Tracker app")
showDB(filter, OutputDB)
root.mainloop()

