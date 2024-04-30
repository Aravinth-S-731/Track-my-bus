from flask import Flask , render_template , request , session , redirect , url_for , jsonify
import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    user = "root",
    password = "@Arvi7777",
    database = 'track_my_bus'
)
mycursor = mydb.cursor()

app = Flask(__name__)
app.secret_key = "secret key"


@app.route('/')
def page1():
    return render_template("index.html")

@app.route('/login', methods = ['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        mycursor.execute('SELECT * FROM track_my_bus.user_login WHERE username=%s AND password=%s',(username,password))
        record = mycursor.fetchone()
        if record:
            session['loggedin'] = True
            session['username'] = record[3]
            session['name']     = record[0]
            return redirect(url_for('trackmybus'))      #return redirect(url_for('home'))
        else:
            msg = 'Incorrect password or username'
    return render_template ('login.html',msg=msg)

@app.route('/signup', methods = ['GET','POST'])
def signup():
    msg = ''
    if request.method == 'POST'  and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'name' in request.form:
        name = request.form['name']
        userName = request.form['username']
        password = request.form['password']
        email = request.form['email']
        mycursor.execute('SELECT * FROM track_my_bus.user_login WHERE username=%s AND email=%s',(userName,email))
        account = mycursor.fetchone()
        if account == ( userName or email):
            msg = 'Account already exists !'
        else:
            data = [name, email, userName, password]
            statement = "INSERT INTO track_my_bus.user_login(name,email,username,password) VALUES (%s,%s,%s,%s)"
            mycursor.execute(statement,data)
            mydb.commit()
            msg = 'You have successfully registered !'
            return redirect(url_for('login'))
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('signup.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('username',None)
    session.pop('name',None)
    return redirect(url_for('login'))

@app.route('/trackmybus', methods = ['GET','POST'])
def trackmybus():
    mycursor.execute('SELECT * FROM `track_my_bus`.`city_test`')
    depart_city = mycursor.fetchall()
    mycursor.execute('SELECT * FROM `track_my_bus`.`city_test`')
    arrival_city = mycursor.fetchall()
    return render_template('main.html', name = session['name'], depart_city = depart_city, arrival_city = arrival_city)

@app.route('/showBus', methods = ['GET','POST'])
def showBus():
    depart = request.form['depature']
    arrive = request.form['arrive']
    start = request.form['start']
    end = request.form['end']
    print(depart,arrive,start,end)
    if depart == "Tuticorin":
        mycursor.execute("SELECT provoider,coach,start_time,end_time,duration,stops FROM `track_my_bus`.`tuty_test` WHERE depature_place = %s AND arrival_place = %s AND start_time >= %s AND start_time <= %s",(depart,arrive,start,end))
        data = mycursor.fetchall()

    if depart == "Tirunelveli":
        mycursor.execute("SELECT provoider,coach,start_time,end_time,duration,stops FROM `track_my_bus`.`tvl_test` WHERE depature_place = %s AND arrival_place = %s AND start_time >= %s AND start_time <= %s",(depart,arrive,start,end))
        data = mycursor.fetchall()
    

    temp , x , l = [] , 0 , len(data)
    for i in range(l):
        temp.append(list(data[i]))
    for i in temp:
        temp[x][2], temp[x][3], temp[x][4] = str(data[x][2]), str(data[x][3]), str(data[x][4])
        x += 1

    return render_template ('showBus.html', name = session['name'], depature_city = depart, arrival_city = arrive, start_time = start, end_time = end, data = temp)

@app.route('/map', methods = ['POST','GET'])
def map():
    location = "https://google.com/maps/@9.7040283,78.0994099,15z/data=!4m2!7m1!2e1?hl=en"
    location = "<iframe src='https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3932.718062559942!2d78.0986632140921!3d9.705086693053747!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3b00d7ef1aa5f193%3A0x127c3281a7ee1d2c!2sSethu%20Institute%20of%20Technology!5e0!3m2!1sen!2sin!4v1675230430108!5m2!1sen!2sin' width='600' height='450' style='border:0;' allowfullscreen=' loading='lazy' referrerpolicy='no-referrer-when-downgrade'></iframe>"
    return render_template("map.html", location = location)

@app.route('/developers', methods = ['POST','GET'])
def dev():
    return render_template("developers.html")

if __name__ == "__main__":
    app.run(debug=True)