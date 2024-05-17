#!/usr/bin/env python
# encoding: utf-8
import config
import json
import sqlite3 as sql
from flask import Flask, jsonify, request, render_template, url_for
# custom lib
from lib.libDb import *


app = Flask(__name__)

# https://pythonbasics.org/flask-sqlite/

initDB = init_db()
if initDB!=0:
    print("Failed to create db!")

# userFile = './assets/files/users.json'
# print("All ok until here")

@app.route('/')
def index():
   return render_template('index.html')


#### TEACHERS

@app.route('/newTeacher')
def new_teacher():
   return render_template('teacher.html')

@app.route('/addTeacher',methods = ['POST', 'GET'])
def add_teacher():
   if request.method == 'POST':
      try:
          srnm = request.form['srnm']
          nm = request.form['nm']
          cc = request.form['cc']
          # pin = request.form['pin']
       
          # with sql.connect("myTeacher.db") as con:
          conn = get_db_connection()  
          cur = conn.cursor()
          cur.execute("INSERT INTO teacher (cognome, nome, classeconcorso) VALUES (?,?,?)",(srnm, nm, cc) )
          conn.commit()
          msg = "Record successfully added"
      except:
          conn.rollback()
          msg = "error in insert operation"
          conn.close()
      finally:
          return render_template("result.html",msg = msg)
        

@app.route('/list')
def list():
   conn = get_db_connection()   
   cur = conn.cursor()
   cur.execute("select * from teacher")   
   rows = cur.fetchall(); 
   return render_template("list.html",rows = rows)


'''

## Read - GET : all users
@app.route("/users", methods=['GET'])
# @app.route("/users/<pUsername>/<pPassword>", methods=['GET'])
def query_users():

    with open(userFile, "r") as f:
        # returns JSON object as a dictionary
        myData = json.loads(f.read())
    if not myData:
        return jsonify({'0': 'no user found'})
    else:
        allUsers = myData['users']
        return jsonify(allUsers)
    
## Read - GET : single user by username/password
# Es. localhost:5001/users/topolino/abcdef?username=topo345&password=lino123
@app.route("/users/<pUsername>/<pPassword>", methods=['GET'])
def query_user_by_username_password(pUsername, pPassword):
    userByArgs = request.args.get('username')
    if userByArgs:
        print('user(QS):' + userByArgs)

    passByArgs = request.args.get('password')
    if passByArgs:
        print('user(QS):' + passByArgs)

    print('user/pUsername/pPassword):' + pUsername + '/' + pPassword)

    userToFindByUsername = pUsername # userByArgs
    userToFindByPassword = pPassword # passByArgs
    newUsers = {"users" : [] }

    with open(userFile, "r") as f:
        # returns JSON object as a dictionary
        myData = json.loads(f.read())
    if not myData:
        return jsonify({'0': 'no user found'})
    else:
        allUsers = myData['users']
        for currentUser in allUsers:
            print('currentUser:' + currentUser['username'] + '/' + currentUser['password'])
            if (currentUser['username']==userToFindByUsername and currentUser['password']==userToFindByPassword):
                newUsers['users'].append(currentUser)
                return jsonify(newUsers)
        # se non viene trovato alcun utente
        return jsonify({'0': 'no users found: username or password not correct'})


## Create - POST
@app.route("/users", methods=['POST'])
def create_user():
    # lettura dei dati dalla Querystring della request, conversione in un dict
    userToCreate = request.args.to_dict()
    # print(newUser)
    newUsers = {"users" : [] }
    newUsers['users'].append(userToCreate)

    # lettura dal file
    with open(userFile, "r") as fr:
        myData = json.loads(fr.read())

    if not myData:
        print('no data')
    else:
        allUsers = myData['users']
        for currentUser in allUsers:
            newUsers['users'].append(currentUser)
    # print(newUsers)

    # scrittura sul file
    with open(userFile, "w") as fw:
        fw.write(json.dumps(newUsers, indent=2))
    return jsonify(userToCreate)


## Update - PUT
@app.route("/users", methods=['PUT'])
def modify_user():
    # print("All ok until here")
    userToModify = request.args.to_dict()
    newUsers = {"users" : [] }

    # lettura dal file
    with open(userFile, "r") as fr:
        myData = json.loads(fr.read())
    if not myData:
        return jsonify({'0': 'no users found'})
    else:
        allUsers = myData['users']
        for currentUser in allUsers:
            if currentUser['username']==userToModify['username']:
                newUsers['users'].append(userToModify)
            else:
                newUsers['users'].append(currentUser)

    # scrittura sul file
    with open(userFile, "w") as fw:
        fw.write(json.dumps(newUsers, indent=2))

    return jsonify({'modified': userToModify})


## Delete - DELETE
@app.route("/users", methods=['DELETE'])
def delete_user():
    # print("All ok until here")
    userToDelete = request.args.get('username')
    newUsers = {"users" : [] }

    # lettura dal file
    with open(userFile, "r") as fr:
        myData = json.loads(fr.read())
    if not myData:
        return jsonify({'0': 'no users found'})
    else:
        allUsers = myData['users']
        for currentUser in allUsers:
            if currentUser['username']==userToDelete:
                continue
            else:
                newUsers['users'].append(currentUser)

    # scrittura sul file
    with open(userFile, "w") as fw:
        fw.write(json.dumps(newUsers, indent=2))

    return jsonify({'deleted': userToDelete})



'''

if __name__ == '__main__':
   app.run(debug = True)