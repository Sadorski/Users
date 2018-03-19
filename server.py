from flask import Flask, session, redirect, render_template, request
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = "penguins"
mysql = MySQLConnector(app, 'fullfriends')

@app.route('/')
def index():
    return redirect('/users')

@app.route('/users')
def usertable():
    users = mysql.query_db("SELECT * FROM friends")

    return render_template('index.html', users=users)

@app.route('/users/new')
def newuser():
    return render_template('newuser.html')

@app.route('/users/<id>')
def induser(id):
    query = "SELECT * FROM friends WHERE id = :id"
    data = {
        "id": id
    }
    users = mysql.query_db(query, data)
    return render_template('user.html', users=users, id=id)

@app.route('/users/<id>/edit')
def edituser(id):
    query = "SELECT * FROM friends WHERE id = :id"
    data = {
        "id": id
    }
    users = mysql.query_db(query,data)
    return render_template('edit.html', users=users, id=id)

@app.route('/users/create', methods=['POST'])
def createuser():
    query = "INSERT INTO friends (first_name, last_name, email, age, created_at, updated_at) VALUES(:first, :last, :email, :age, NOW(), NOW())"
    data = {
        "first": request.form['first_name'],
        "last": request.form['last_name'],
        "email": request.form['email'],
        "age": request.form['age']
    }
    mysql.query_db(query, data)
    return redirect('/users')

@app.route('/users/<id>/destroy')
def deluser(id):
    query = "DELETE FROM friends WHERE id = :id"
    data = {
        "id": id
    }
    mysql.query_db(query, data)
    return redirect('/users')

@app.route('/users/<id>/update', methods=['POST'])
def updateduser(id):
    query = "UPDATE friends SET first_name = '{}', last_name = '{}', email = '{}', age = '{}' WHERE id = '{}'".format(request.form['first_name'], request.form['last_name'], request.form['email'], request.form['age'], id)
    mysql.query_db(query)
    return redirect('/users')
    
app.run(debug=True)




