from flask import Flask, render_template, request, session, redirect, url_for, flash
from functools import wraps
from dbconnection import connection


# check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        session['next_url'] = request.referrer
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(session['next_url'])
    return wrap


# check if admin logged in
def required_login(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and session['username'] == 'Jaydeep':
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('admin_login'))
    return wrap



# getting users from users table
def get_users():
    data = ()
    # creating cursor
    cur,conn = connection()
    # getting users
    result = cur.execute("SELECT * FROM users")
    
    if result > 0:
        data = cur.fetchall()
        return data
    
    return data 


# getting devices from database
def get_gadgets():
    data = ()
    # creating cursor
    cur,conn = connection()
    # getting users
    result = cur.execute("SELECT * FROM  mobile")
       
    if result > 0:
        data = cur.fetchall()
        return data
    
    return data

# count users and gadgets
def count_gadgets_users():
    args = ('gadgets','users')
    # creating cursor
    cur,conn = connection()
    # getting users
    cur.callproc("count_gadgets_users", args)

    cur.execute("""SELECT @_count_gadgets_users_0, @_count_gadgets_users_1""")  

    data = cur.fetchone()

    return data
    

# get upcomming mobiles
def upcoming_mobiles():
    key = '%-1.%'
    # create cursor
    cur, conn = connection()

    # execute 
    cur.execute("""SELECT mobile.model_name, brand, price, img_url FROM  mobile JOIN images ON 
    mobile.model_name = images.model_name WHERE mobile.model_name IN (%s,%s,%s,%s) AND images.img_url LIKE %s """,
     ('Redmi Note 10 Pro','V20 Pro','Rog Phone 3','Realme 7 Pro',key))

    # fetch
    data = cur.fetchall()

    return data


# recommendations
def recommendations():
    key = '%-1.%'
    # create cursor
    cur, conn = connection()

    # execute 
    cur.execute("""SELECT mobile.model_name, brand, price, img_url FROM  mobile JOIN images ON 
    mobile.model_name = images.model_name WHERE mobile.model_name IN (%s,%s,%s,%s) AND images.img_url LIKE %s """,
     ('Nord','iphone 11 pro','Redmi Note 8 pro','Galaxy M31',key))

    # fetch
    data = cur.fetchall()

    return data


# gaming
def gaming():
    key = '%-1.%'
    # create cursor
    cur, conn = connection()

    # execute 
    cur.execute("""SELECT mobile.model_name, brand, price, img_url FROM  mobile JOIN images ON 
    mobile.model_name = images.model_name WHERE mobile.model_name IN (%s,%s,%s,%s) AND images.img_url LIKE %s """,
     ('Black Shark 2','iphone 11 pro','ROG phone 3','IQOO 3',key))

    # fetch
    data = cur.fetchall()

    return data


# photographic
def photography():
    key = '%-1.%'
    # create cursor
    cur, conn = connection()

    # execute 
    cur.execute("""SELECT mobile.model_name, brand, price, img_url FROM  mobile JOIN images ON 
    mobile.model_name = images.model_name WHERE mobile.model_name IN (%s,%s,%s,%s) AND images.img_url LIKE %s """,
     ('v20 pro','galaxy s10 plus','iphone 11 pro','F17',key))

    # fetch
    data = cur.fetchall()
    print(data)

    return data    



# perfomacnce
def performance():
    key = '%-1.%'
    # create cursor
    cur, conn = connection()

    # execute 
    cur.execute("""SELECT mobile.model_name, brand, price, img_url FROM  mobile JOIN images ON 
    mobile.model_name = images.model_name WHERE mobile.model_name IN (%s,%s,%s,%s) AND images.img_url LIKE %s """,
     ('8T','Nord','Redmi Note 8 Pro','Galaxy M51',key))

    # fetch
    data = cur.fetchall()
    print(data)

    return data    