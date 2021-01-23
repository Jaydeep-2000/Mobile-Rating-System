from flask import Flask, render_template, request, session, redirect, url_for, flash
from utilities import is_logged_in,get_gadgets,get_users,required_login,count_gadgets_users,upcoming_mobiles,recommendations,gaming,photography,performance
from werkzeug.utils import secure_filename
from dbconnection import connection
from passlib.hash import sha256_crypt
# from datetime import datetime
# from functools import wraps
# from flask_mail import Mail
import MySQLdb
import os
import json
import math
import random


# reading parameters from config.json
with open ("config.json", "r") as f:
    params = json.load(f)["params"]


app = Flask(__name__, template_folder='templates')
app.secret_key = 'dbms_secrete'
app.config['UPLOAD_FOLDER'] = params['upload_location']
app.config['ALLOWED_EXTENSIONS'] = params['allowed_extensions']

# home
@app.route('/')
def home():
    upcoming_list = upcoming_mobiles()
    recommendation_list = recommendations()
    return render_template('home.html', upcoming_list=upcoming_list, recommendation_list=recommendation_list)


# user profile
@app.route('/profile')
@is_logged_in
def user_profile():
 
    cur, conn = connection()

    # get user by username
    cur.execute("""SELECT * FROM users WHERE email= %s""", (session['username'],))

    # fetch result
    data = cur.fetchone()
        
    return render_template('user_profile.html', data=data)


# user login
@app.route('/login', methods=['GET','POST'])
def user_login():
    if request.method == 'POST':
        # getting previous url
        session['next_url'] = request.referrer

        # get form fields
        email = request.form['email']
        password_candidate = request.form['password']

        print(email)
        print(password_candidate)
        # create cursor
        cur, conn = connection()

        # get user by username
        result = cur.execute("""SELECT * FROM users WHERE email= %s""", (email,))

        if result > 0:
            data = cur.fetchone()
            print(data)
            password = data['password']

            #  close connection
            cur.close()

            # compare  password
            if sha256_crypt.verify(password_candidate, password):
                app.logger.info('PASSWORD MATCHED')
                session['logged_in'] = True
                session['username'] = email
                session['name'] = data['name']
                print(session['next_url'])
                flash('You are now logged in', 'success')
                return redirect(session['next_url'])
            else:
                 flash('Invalid credentials ', 'danger')
                 return redirect(session['next_url'])
            
        else:
            flash('Invalid credentials ', 'danger')
            return redirect(session['next_url'])


# user-signup
@app.route('/signup', methods=['GET','POST'])
def user_signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = sha256_crypt.encrypt(str(request.form.get('password')))
        # password = form.password.data

        print(name)
        print(email)
        print(password)

        # creating cursor
        cur, conn = connection()


        # check if email exists
        result = cur.execute("""SELECT * FROM users WHERE email=%s""", (email,))

        if result > 0:
            flash("user already exist use another email", 'danger')
            return redirect(url_for("home"))

        cur.execute("""INSERT INTO users(name, email, password) VALUES(%s, %s, %s)""", (name, email, password))
    
        # commit
        conn.commit()

        # close connection
        cur.close()

        flash('You are now registered and you can log in', 'success')

        return redirect(url_for('home'))


# update profile
@app.route('/update-profile', methods=['GET','POST'])
@is_logged_in
def update_profile():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')

        # creating cursor
        cur, conn = connection()

        cur.execute("""UPDATE users SET name = %s, email = %s WHERE email = %s""", (name, email, session['username']))
    
        # commit
        conn.commit()

        # close connection
        cur.close()

        return redirect(url_for('user_profile'))


# update profile
@app.route('/change-password', methods=['GET','POST'])
@is_logged_in
def change_password():
    if request.method == 'POST':
        password = sha256_crypt.encrypt(str(request.form.get('new_password')))

        # creating cursor
        cur, conn = connection()

        cur.execute("""UPDATE users SET password = %s WHERE email = %s""", (password, session['username']))
    
        # commit
        conn.commit()

        # close connection
        cur.close()

        return redirect(url_for('home'))


# price list | view all
@app.route('/<brand>-mobile-price-list-in-india', methods=['GET','POST'])
def view_all(brand):
    print(brand)
    key = '%-1.%'
    # creating cursor
    cur,conn = connection()
    # getting users
    result = cur.execute("""SELECT mobile.model_name, brand, price, img_url FROM  mobile JOIN images ON mobile.model_name = images.model_name WHERE brand = %s AND images.img_url LIKE %s """, (brand,key))
    
    if result > 0:
        mobile_list = cur.fetchall()
        print(mobile_list)
        return render_template('view_all.html', mobile_list=mobile_list)
    return render_template('view_all.html', mobile_list=mobile_list)


# view details / specs
@app.route('/<brand>-<model_name>')
def view_details(brand,model_name):
    print(brand)
    print(model_name)
     # create cursor
    cur, conn = connection()

    # specs query
    result = cur.execute("""SELECT mobile.model_name,brand,processor,graphics,os,battery_cap,quick_charge,front_camera,
                rear_camera,display_type,display_size,aspect_ratio,weight,build,dimensions FROM mobile 
                JOIN specifications ON mobile.model_name=specifications.model_name WHERE mobile.model_name=%s""", (model_name,))

    # fetching specs
    if result > 0:
        specs = cur.fetchone()
        print(specs)

    # colours query
    result = cur.execute("""SELECT colour FROM colours WHERE model_name = %s""", (model_name,))

    # fetching colors
    if result > 0:
        colours = cur.fetchall()
        print(colours)

    # images query
    result = cur.execute("""SELECT img_url FROM images WHERE model_name = %s""", (model_name,))

    # fetching images
    if result > 0:
        images = cur.fetchall()
        print(images)

    # variants query
    result = cur.execute("""SELECT variant,price FROM variants WHERE model_name = %s""", (model_name,))

    # fetching variants

    variants = cur.fetchall()
    print(variants)

    # reviews query
    result = cur.execute("""SELECT name,users.email,rating,title,comment,date FROM reviews JOIN users ON users.email=reviews.email WHERE model_name = %s""", (model_name,))

    # fetching reviews   
    reviews = cur.fetchall()
    print(reviews)


    # close connection
    cur.close()

    return render_template("view_details.html", specs=specs, colours=colours, images=images, variants=variants, reviews=reviews)


# add review
@app.route('/post-review/<brand>-<model_name>', methods=['GET','POST'])
@is_logged_in
def post_reviews(brand,model_name):
    if request.method == 'POST':
        print(brand)
        print(model_name)
        
        rating = request.form.get('rating')
        title = request.form.get('title')
        comment = request.form.get('comment')
        print(rating)
        # create cursor
        cur, conn = connection()

        cur.execute("""INSERT INTO reviews (model_name, email, rating, title, comment) VALUES (%s,%s,%s,%s,%s)""" ,(model_name, session['username'], rating, title, comment))

        # commit
        conn.commit()

        #  close connection
        cur.close()
        return redirect(url_for('view_details', brand=brand, model_name=model_name))

    return render_template('add_review.html', brand=brand, model_name=model_name)


@app.route('/compare', methods=['GET','POST'])
def compare():
    if request.method == 'POST':
        model1 = request.form.get('model1')
        model2 = request.form.get('model2')
        print(model1)
        print(model2)
        # intializing dictionaries
        mobile1 = {}
        mobile2 = {}
        
        # create cursor
        cur,conn = connection()

        result = cur.execute("""SELECT * FROM mobile JOIN specifications ON mobile.model_name= specifications.model_name 
        JOIN  images  ON specifications.model_name= images.model_name AND img_url LIKE %s  
        WHERE mobile.model_name = %s""", ('%1%', model1))

        # fetch data
        if result > 0:
            mobile1 = cur.fetchone()
        
    
        result = cur.execute("""SELECT * FROM mobile JOIN specifications ON mobile.model_name= specifications.model_name 
        JOIN  images  ON specifications.model_name= images.model_name AND img_url LIKE %s  
        WHERE mobile.model_name = %s""", ('%1%', model2))

        # fetch data
        if result > 0:
            mobile2 = cur.fetchone()


        print(mobile1)
        print(mobile2)
        # close cursor
        cur.close()
        return render_template('compare.html', mobile1=mobile1, mobile2=mobile2)

    return render_template('compare.html')


# search results
@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST': 
        search_key = request.form.get('search_key')
        print(search_key)
        mobile = {}
        # create cursor
        cur,conn = connection()

        result = cur.execute("""SELECT mobile.model_name, brand, price, img_url FROM  mobile JOIN images ON mobile.model_name = images.model_name WHERE mobile.model_name = %s AND images.img_url LIKE %s """, (search_key,'%1%'))

        # fetch data
        if result > 0:
            mobile = cur.fetchone()

        # close cursor
        cur.close()
        print(type(mobile))
        
        return render_template('search_result.html', mobile=mobile)
    

# best page
@app.route('/best', methods=['GET','POST'])
def best():
    
    # get gaming list
    gaming_list = gaming()

    # photo graphy list
    photography_list = photography()


    # performance
    performance_list = performance()


    return render_template('best.html', gaming_list=gaming_list, photography_list=photography_list, performance_list=performance_list)




# admin login
@app.route('/admin-login', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('uname')
        password = request.form.get('pass')
        if (username==params['admin_user'] and password==params['admin_password']):
            #set session variable
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('adminLogin.html', params=params)


# logout
@app.route('/logout')
def logout():
    session.clear();
    flash('You are now logged out', 'success')
    return redirect(url_for('home'))


# dashboard
@app.route('/admin-panel/dashboard', methods=['GET','POST'])
@required_login
def dashboard():
    count = count_gadgets_users()
    return render_template('dashboard.html', count=count )


# users
@app.route('/admin-panel/users/', methods=['GET','POST'])
@required_login
def users():
    users = get_users()
    last = math.ceil(len(users)/int(params['no_of_users']))
    print(last)

    page = request.args.get('page')
    if(not str(page).isnumeric()):
        page = 1
    
    page= int(page)
    users = users[(page-1)*int(params['no_of_users']): (page-1)*int(params['no_of_users'])+ int(params['no_of_users'])]
    #pagination logic
    # first
    if(page==1):
        prev= "#"
        if(last==1):
            next = "#"
        else:
            next = "/admin-panel/users/?page=" + str(page+1)
    # last
    elif(page==last):
        prev = "/admin-panel/users/?page=" + str(page-1)
        next= "#"
        # middel
    else:
        prev = "/admin-panel/users/?page=" + str(page-1)
        next = "/admin-panel/users/?page=" + str(page + 1)
    print(users)
    return render_template('users.html', users=users, prev=prev, next=next)


# devices
@app.route('/admin-panel/gadgets/', methods=['GET','POST'])
@required_login
def gadgets():
    gadgets =get_gadgets()
    print(gadgets)
    last = math.ceil(len(gadgets)/int(params['no_of_gadgets']))
    print(last)

    page = request.args.get('page')
    if(not str(page).isnumeric()):
        page = 1
    
    page= int(page)
    gadgets = gadgets[(page-1)*int(params['no_of_gadgets']): (page-1)*int(params['no_of_gadgets'])+ int(params['no_of_gadgets'])]
    #pagination logic
    # first
    if(page==1):
        prev= "#"
        next = "/admin-panel/gadgets/?page=" + str(page+1)
    # last
    elif(page==last):
        prev = "/admin-panel/gadgets/?page=" + str(page-1)
        next= "#"
        # middel
    else:
        prev = "/admin-panel/gadgets/?page=" + str(page-1)
        next = "/admin-panel/gadgets/?page=" + str(page + 1)
        

    return render_template('gadgets.html', gadgets=gadgets, prev=prev, next=next )


# add device
@app.route('/admin-panel/add-gadget', methods=['GET','POST'])
@required_login
def add_gadget():
    if request.method == 'POST':
        model_name = request.form.get('model_name')
        print(model_name)
        brand = request.form.get('brand') 
        print(brand)
        price = request.form.get('price')

        # create cursor
        cur, conn = connection()

        cur.execute("INSERT INTO mobile (model_name, brand, price) VALUES ('%s', '%s','%s')" % (model_name, brand, price))

        # commit
        conn.commit()

        # close connection
        cur.close()
        flash('Gadget added successfully...', 'success')
        return redirect(url_for('upload_img', brand=brand, model_name=model_name))

    return render_template('addGadget.html')


# file uploader
@app.route("/admin-panel/uploader/<brand>/<model_name>", methods=['GET','POST'])
@required_login
def upload_img(brand, model_name):
    
    if request.method == 'POST':
        model_name = request.form.get('model_name')
        brand = request.form.get('brand')
        f = request.files.getlist('img_file')
        print(f)

        for img in f:
            img_url = img.filename
            print(img_url)
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(img.filename)))
            # create cursor
            cur, conn = connection()

            cur.execute("INSERT INTO images (model_name, img_url) VALUES ('%s','%s')" % (model_name,img_url))

            # commit
            conn.commit()

            # close connection
            cur.close()


        print(brand)
        print(model_name)
       
        
        flash('Image uploaded successfully...', 'success')
        return redirect(url_for('add_specs', brand=brand, model_name=model_name))

    return render_template('uploader.html', brand=brand, model_name=model_name)



# add device
@app.route('/admin-panel/add-specs/<brand>/<model_name>', methods=['GET','POST'])
@required_login
def add_specs(brand, model_name):
    if request.method == 'POST':
        model_name = request.form.get('model_name')
        brand = request.form.get('brand')
        print(brand)
        print(model_name)
        processor = request.form.get('processor')
        graphics = request.form.get('graphics')
        os = request.form.get('os')
        battery_cap = request.form.get('battery_cap')
        quick_charge = request.form.get('quick_charge')
        front_camera = request.form.get('front_camera')
        rear_camera = request.form.get('rear_camera')
        display_type = request.form.get('display_type')
        display_size = request.form.get('display_size')
        aspect_ratio = request.form.get('aspect_ratio')
        weight = request.form.get('weight')
        build = request.form.get('build')
        dimensions = request.form.get('dimensions')
        colours = request.form.get('colours').split(",")
        print(colours)

        # inserting colors
        for colour in colours:
             # create cursor
            cur, conn = connection()

            cur.execute("INSERT INTO colours (model_name, colour) VALUES ('%s','%s')" % (model_name,colour))

            # commit
            conn.commit()

            # close connection
            cur.close()
     

         # create cursor
        cur, conn = connection()

        # inserting specs
        cur.execute("""INSERT INTO specifications(model_name, processor, graphics, os, battery_cap, quick_charge, front_camera, rear_camera, display_type, display_size, aspect_ratio,dimensions, weight, build) 
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (model_name, processor, graphics, os, battery_cap, quick_charge, front_camera, rear_camera, display_type, display_size, aspect_ratio, dimensions, weight, build))

        # commit
        conn.commit()

        # close connection
        cur.close()
     

        flash('Specs are saved successfully...')
        return redirect(url_for('add_variants', brand=brand, model_name=model_name))

    return render_template('addSpecs.html', brand=brand, model_name=model_name)


# add variant
@app.route('/admin-panel/add-variants/<brand>/<model_name>', methods=['GET','POST'])
@required_login
def add_variants(brand, model_name):
    if request.method == 'POST':
        model_name = request.form.get('model_name')
        brand = request.form.get('brand')
        print("inside variants")
        print(brand)
        print(model_name)
        variant = request.form.get('variant')
        price = request.form.get('price')

        # creating cursor
        cur,conn = connection()

        cur.execute("""INSERT INTO variants (model_name, variant, price) VALUES (%s,%s,%s)""", (model_name, variant, price))
        
        # commit
        conn.commit()

        # close cursor
        cur.close()

        flash("A new variant is added successfully...", 'success')
        return redirect(url_for('add_variants', brand=brand, model_name=model_name))

    return render_template('addVariants.html', brand=brand, model_name=model_name)


# view gadget
@app.route('/admin-panel/gadgets/view/<brand>/<model_name>', methods=['GET','POST'])
@required_login
def view(brand,model_name):

    print(brand)
    print(model_name)

    # create cursor
    cur, conn = connection()

    # specs query
    result = cur.execute("""SELECT mobile.model_name,brand,processor,graphics,os,battery_cap,quick_charge,front_camera,
                rear_camera,display_type,display_size,aspect_ratio,weight,build,dimensions FROM mobile 
                JOIN specifications ON mobile.model_name=specifications.model_name WHERE mobile.model_name=%s""", (model_name,))

    # fetching specs
    if result > 0:
        specs = cur.fetchone()
        print(specs)

    # colours query
    result = cur.execute("""SELECT colour FROM colours WHERE model_name = %s""", (model_name,))

    # fetching colors
    if result > 0:
        colours = cur.fetchall()
        print(colours)

    # images query
    result = cur.execute("""SELECT img_url FROM images WHERE model_name = %s""", (model_name,))

    # fetching images
    if result > 0:
        images = cur.fetchall()
        print(images)

    # variants query
    result = cur.execute("""SELECT variant,price FROM variants WHERE model_name = %s""", (model_name,))

    # fetching variants
    if result > 0:
        variants = cur.fetchall()
        print(variants)

    # reviews query
    result = cur.execute("""SELECT name,users.email,rating,title,comment FROM reviews JOIN users ON users.email=reviews.email WHERE model_name = %s""", (model_name,))

    # fetching reviews   
    reviews = cur.fetchall()
    print(reviews)


    # close connection
    cur.close()

    return render_template("view.html", specs=specs, colours=colours, images=images, variants=variants, reviews=reviews)



# delete gadget
@app.route('/admin-panel/gadgets/delete/<brand>/<model_name>', methods=['GET','POST'])
@required_login
def delete_gadget(brand,model_name):
    # create cursor
    cur,conn = connection()

    cur.execute("""DELETE FROM mobile WHERE model_name=%s""", (model_name,))

    # commit
    conn.commit()

    # close cursor
    cur.close()
    
    return redirect(url_for('gadgets'))


# delete a user
@app.route('/admin-panel/users/delete/<email>', methods=['GET','POST'])
@required_login
def delete_user(email):
    # create cursor
    cur,conn = connection()

    cur.execute("""DELETE FROM users WHERE email=%s""", (email,))

    # commit
    conn.commit()

    # close cursor
    cur.close()
    
    return redirect(url_for('users'))


# delete comment
@app.route('/admin-panel/gadgets/view/delete-comment/<brand>/<model_name>/<email>', methods=['GET','POST'])
@required_login
def delete_comment(brand,model_name,email):
    # create cursor
    cur,conn = connection()

    cur.execute("""DELETE FROM reviews WHERE model_name=%s AND email=%s""", (model_name,email))

    # commit
    conn.commit()

    # close cursor
    cur.close()
    
    return redirect(url_for('view', brand=brand, model_name=model_name))


# search gadget
@app.route('/admin-panel/gadgets/search', methods=['GET','POST'])
@required_login
def search_gadget():
    if request.method ==  'POST': 
        search_key = request.form.get('search_key')
        print(search_key)
        # create cursor
        cur,conn = connection()

        result = cur.execute("""SELECT * FROM mobile WHERE model_name = %s""", (search_key,))

        # fetch data
        gadget = cur.fetchone()

        # close cursor
        cur.close()
        print(gadget)
        
        return render_template('searchGadget.html', gadget=gadget)
    return render_template('searchGadget.html', gadget=gadget)






if __name__ == "__main__":
    app.run(debug=True)
