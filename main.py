from flask import Flask,jsonify
import sqlite3


app = Flask(__name__)

@app.route("/")
def home():
    return "This API is up!!!"

@app.route("/add-user/<name>/<email>/<password>", methods = ["GET"])
def addUser(name,email,password):
    db = sqlite3.connect("user_data.db")
    cursor = db.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS users 
        (name VARCHAR(20) NOT NULL,
        email VARCHAR(30) NOT NULL PRIMARY KEY, 
        password VARCHAR(16) NOT NULL)"""
        )

    try:
        cursor.execute(f"INSERT INTO users VALUES ('{name}','{email}','{password}')")
        db.commit()
    except:
        db.rollback()
        db.close()
        return jsonify({'status':"User not added"})
    
    db.close()
    return jsonify({'status':"User added successfully"})

@app.route("/get-user/<email>/<password>", methods = ["GET"])
def getUser(email,password):
    db = sqlite3.connect("user_data.db")
    cursor = db.cursor()
    cursor.execute(
    """CREATE TABLE IF NOT EXISTS users 
    (name VARCHAR(20) NOT NULL,
    email VARCHAR(30) NOT NULL PRIMARY KEY, 
    password VARCHAR(16) NOT NULL)"""
    )

    data = cursor.execute(f"SELECT email,password FROM users where email = '{email}'").fetchone()

    if data == None:
        db.close()
        return jsonify({'status':"Invalid email or account doesn't exists"})
    elif data[1] != password:
        db.close()
        return jsonify({'status':"Invalid password entered"})
    else:
        db.close()
        return jsonify({'status':"Account exists"})

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=10000)