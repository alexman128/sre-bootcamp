from flask import Flask
from flask import jsonify
from flask import request
from methods import Token, Restricted
import hashlib
#from flask_mysqldb import MySQL
import mysql.connector


app = Flask(__name__)

#mysql = MySQL(app)
login = Token()
protected = Restricted()

app.config['secret'] = "my2w7wjd7yXF64FIADfJxNs1oupTGAuW"

# Just a health check
@app.route("/")
def url_root():
    return "OK"


# Just a health check
@app.route("/_health")
def url_health():
    return "OK"


# e.g. http://127.0.0.1:8000/login
@app.route("/login", methods=['POST', 'GET'])
def url_login():
    if request.method == 'GET':

        username = request.args.get('username')
        password = request.args.get('password')        
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


    
    #print(f"username {username}, password {password}")

    Conection_db = mysql.connector.connect( 
        host='bootcamp-tht.sre.wize.mx', 
        user= 'secret', 
        passwd='noPow3r', 
        port=3306, 
        db='bootcamp_tht' )
    cur = Conection_db.cursor()

    cur.execute( "SELECT username, password, salt FROM users  WHERE username = %s", (username, ))
    data = cur.fetchall()
    if data:
        row = data[0]
        encrypted_password = row[1]
        salt = str(row[2])
        salted = str(password) + salt
    

        #print(f"encrypted password {encrypted_password}")
        salted = salted.encode('utf-8')
        h = hashlib.sha512(salted)
        encrypted =  h.hexdigest()
        print(f"encrypted {encrypted}")
        print(f"encrypted stored in the database: {encrypted_password}")

        if (encrypted == encrypted_password):
            res = {
                    "data": login.generate_token(username, password)
            }
        else:
            res = None
    else: 
        print("No data")
        res = {'Error': 'wrong credentials'}

    
    return jsonify(res)


# # e.g. http://127.0.0.1:8000/protected
@app.route("/protected")
def url_protected():
    auth_token = request.headers.get('Authorization')
    res = {
        "data": protected.access_data(auth_token)
    }
    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
