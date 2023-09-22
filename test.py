from flask import Flask, render_template, request, url_for, session,redirect, flash
import sqlite3 , json ,re
test_app = Flask(__name__,static_folder='templates')
test_app.secret_key = 'my-secret-key'
conn = sqlite3.connect('database.db')  
cursor = conn.cursor()
@test_app.route("/scan")
def scan ():
    if 'user' in session:
        return render_template('index.html',user= session['user'])
    else:
        return redirect(url_for('welcome'))
@test_app.route("/")
def welcome():
    return render_template("welcome.html")
@test_app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        conn.commit()
        # Insert user into 'user_points' table with default points value of 0
        c.execute("INSERT INTO user_points (user, points) VALUES (?, ?)", (username, 0))
        conn.commit()
        conn.close()
        
        
        return redirect(url_for('login'))
    
    return render_template('signup.html')
@test_app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            session['user'] = user[1]
            session['username'] = user[2]
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid login credentials'
            return render_template('login.html', error=error)
    
    return render_template('login.html')
@test_app.route('/dashboard')
def dashboard():
    if 'user' in session:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM user_points WHERE user = ? ", ([session['username']]))
        point = c.fetchone()[2]
        
        
        c.execute("SELECT * FROM user_points WHERE user = ? ", ([session['username']]))
        prod = c.execute("SELECT DISTINCT	product FROM result ").fetchall()
        loc = c.execute("SELECT DISTINCT	location FROM result ").fetchall()
        if not point :
            pointU = 0
        else:
             pointU= point
        conn.close()
        
        # return render_template('dashboard.html', user=session['user'] ,point =pointU ,loc = loc, prod= prod)
        return render_template('dashboard.html',user=session['user'] ,point =pointU ,loc = loc, prod= prod
                               )

    else:
        return redirect(url_for('login'))
@test_app.route('/searchData', methods=['POST'])
def searchData():
    loc = request.form['Location']
    prod = request.form['Product']
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM result WHERE product = ? and location = ?", ([prod,loc]))
    Data = c.fetchall()
    
    conn.close()
    
    return render_template('search_results.html', user=session['user'] , Data=Data )
    
@test_app.route('/insert_data', methods=['POST'])
def insert_data():
    d = request.data
    d= json.loads(d)
    
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT product FROM product  ")
    l  = c.fetchall()
    conn.close()
    
    s1 =d['ocrdata']
    
    market= (s1.lower()).find("market")
    branch= (s1.lower()).find("branch")
    dateR= (s1.lower()).find("date")
    if market !=  -1 and branch != -1 and dateR != -1 :
        # print(s1[0:market])
        
        mar = s1[0:market]
        loc=s1[market+1+len("market"):branch]
        dateOfR = s1[dateR+1+len("date"):len(s1)]
        # print(s1[market+1+len("market"):branch])
        # print(s1[dateR+1+len("date"):len(s1)])
       
        
        for i in l:
            s = (s1.lower()).find((i[0].lower()))
            
            if s!= -1:
                for x in range(0,999):
                    if s1[s+x]=="L" and s1[s+x+1]=="E":
                        # print(s1[s+x])
                        # print(s+x)
                        lens = len(i[0])
                        # print(lens+s)
                        
                        prod = i[0]
                        price = re.sub(r'\D', '', s1[lens+s:s+x])
                        
                        
                        conn = sqlite3.connect('users.db')
                        c = conn.cursor()
                        flag = c.execute("select * from result where product = ? and price = ? and Market =? and location =? and date=? ;", (prod,price,mar,loc,dateOfR)).fetchall()
                        if not flag:
                            c.execute("INSERT INTO result (product,price,Market,location,user,date) VALUES (?,?,?,?,?,?)", (str(prod),str(price),str(mar),str(loc),str([session['username']]),str(dateOfR)))
                            # c.execute("UPDATE user_points SET points = points + 1 WHERE user = ?", ([str([session['username']])]))
                            conn.commit()
                            c.execute("SELECT * FROM user_points WHERE user = ? ", ([session['username']]))
                            point = c.fetchone()[2]
                            print('==============')
                            point=point+1
                            c.execute("delete from user_points  WHERE user = ?;", ([session['username']]))
                            c.execute("INSERT INTO user_points (user,points) values (?,?)",([session['username'],str(point)]))
                            conn.commit()
                            print(point)
                        conn.commit()
                        conn.close()
                        break;
        
    
    
    return 'Data inserted successfully'

    
@test_app.route('/saveToCart', methods=['POST'])
def saveToCrt():
    d = request.data
    d= json.loads(d)
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    flag = c.execute("select * from userCart where nameProud = ? and location = ? and merchent =? and price =? and date=? and userEmail=? ;", ([d['name'],d['location'],d['Merchant'],d['price'],d['date'],session['username']])).fetchall()
    if flag:
        
        return "prouduct exist"
    else:
        
        c.execute("INSERT INTO userCart (nameProud,location,merchent,price,date,userEmail) VALUES (?,?,?,?,?,?)", ([str(d['name']),str(d['location']),str(d['Merchant']),str(d['price']),str(d['date']),str(session['username'])]))
                            # c.execute("UPDATE user_points SET points = points + 1 WHERE user = ?", ([str([session['username']])]))
        conn.commit()
        conn.close()
        
        return "added to cart"
    
@test_app.route('/DeleatCart', methods=['POST'])
def DeleatCart():
    d = request.data
    d= json.loads(d)
    conn = sqlite3.connect('users.db')
    c = conn.cursor()   
    c.execute("DELETE  from userCart where id = ?", ([d['id']]))
                        # c.execute("UPDATE user_points SET points = points + 1 WHERE user = ?", ([str([session['username']])]))
    conn.commit()
    conn.close()
    
    return "deleted"

@test_app.route('/UserCart', methods=['GET'])
def UserCart():

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    pointU=c.execute("SELECT * FROM user_points WHERE user = ? ", ([session['username']])).fetchall()[0][2]
    data = c.execute("select * from userCart where userEmail=? ;", ([session['username']])).fetchall()
    conn.close()
        
    return render_template('Cart.html',name=session['user'],Data=data,point =pointU) 
    
@test_app.route('/admin', methods = ['GET', 'POST'])
def admin():
    if request.method == 'GET':
        return render_template('admin_login.html') 
    elif request.method == 'POST':
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        data = c.execute("SELECT * FROM admin WHERE username = ? AND pass = ?", (request.form['username'],  request.form['password'])).fetchall()
        c.fetchone()
        conn.close()
        print(data)

        if data :
            session['user'] = data[0][3]
            return redirect("/adminView")
        else:
            return redirect("/")
@test_app.route('/adminView', methods = ['GET', 'POST'])
def adminV():
    if request.method == 'POST':
        typ = request.form['type']
        pro = request.form['pruduct']
        if typ == "save":
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("INSERT INTO product (product) VALUES (?)", ([pro]))
            conn.commit()
            conn.close()
            return redirect("/adminView")
        elif typ == "del":
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("DELETE  FROM product  where id = (?)", ([pro]))
            conn.commit()
            conn.close()
            
            return redirect("/adminView")
            
    
    elif request.method == 'GET':
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        data = c.execute("SELECT * FROM product ").fetchall()
        c.fetchone()
        conn.close()
        return render_template('adminHome.html',name=session['user'],Data=data) 
    
@test_app.route('/logout')  
def logout():
    session.pop("Doctor",None)
    session.pop("admin",None)
    flash("loged out")
    return redirect("/")
# @test_app.route('/tsst')
# def tsst():
#      return render_template('base.html')
# @test_app.route('/search', methods = ['GET', 'POST'])
# def search ():
#     if request.method == 'POST':
#         search_term = request.form['search_term']
#         query = "SELECT * FROM your_table WHERE column_name LIKE ?"
#         cursor.execute(query, ('%' + search_term + '%',))
#         results = cursor.fetchall()
#         return render_template('search_results.html', results=results)
#     return render_template('base.html')
@test_app.route('/search')
def search():
    if 'user' in session:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM user_points WHERE user = ? ", ([session['username']]))
        point = c.fetchone()[2]
        
        
        c.execute("SELECT * FROM user_points WHERE user = ? ", ([session['username']]))
        prod = c.execute("SELECT DISTINCT	product FROM result ").fetchall()
        loc = c.execute("SELECT DISTINCT	location FROM result ").fetchall()
        if not point :
            pointU = 0
        else:
             pointU= point
        conn.close()
        
        return render_template('search.html', user=session['user'] ,point =pointU ,loc = loc, prod= prod)
if __name__== "__main__":
    test_app.run(debug=True,host="0.0.0.0")
