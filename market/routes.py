from market import app
import base64
from market.new1 import display1
from PIL import Image 
import numpy as np
import cv2 as cv
from flask import render_template, redirect, url_for, flash, request, send_file,Response
from market.models import User,Upload,Logo
from market.forms import RegisterForm, LoginForm
from market import db
from flask_login import current_user, login_user, logout_user, login_required
from io import BytesIO

@app.route('/')

@app.route('/account', methods=["GET", "POST"])
@login_required
def account_img():
    query=Logo.query.filter_by(owner=current_user.username).all()
    IMG_LIST=[]
    for i in query:
        IMG_LIST.append(i.id)
    IMG_LIST.reverse()
    return render_template("account.html", imagelist=IMG_LIST)

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home_page():
    if request.method == 'POST':
        file = request.files['file']
        upload2 = Upload(filename=file.filename, data=file.read())
        db.session.add(upload2)
        db.session.commit()
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def index():
    uploads=-1
    number=-1
    img=""
    if request.method == 'POST':
        file = request.files['file']
        upload = Upload(filename=file.filename, data=file.read())
        number = request.form["number"]
        im_b64 = base64.b64encode(upload.data)
        im_bytes = base64.b64decode(im_b64)
        im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
        img = cv.imdecode(im_arr, flags=cv.IMREAD_COLOR)
        img=cv.cvtColor(img, cv.COLOR_RGB2BGR)
        
        query=Upload.query.all()
        im_b64 = base64.b64encode(query[-1].data)
        im_bytes = base64.b64decode(im_b64)
        im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
        logo= cv.imdecode(im_arr, flags=cv.IMREAD_COLOR)
        logo=cv.cvtColor(logo, cv.COLOR_RGB2BGR)
        if(not number):
                number=-1
        uploads4=Logo.query.all()
        uploads4=(uploads4[-1].id) +1
        img=display1(img,logo,number,current_user.username)
        pil_img = Image.fromarray(img)
        buff = BytesIO()
        pil_img.save(buff, format="JPEG")
        new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")

        img = np.frombuffer(base64.b64decode(new_image_string), np.uint8)
        img=img.tobytes()
        upload5 = Logo(filename=file.filename, data=img ,owner=current_user.username)
        db.session.add(upload5)
        db.session.commit()
        uploads=Logo.query.all()
        uploads=uploads[-1].id
    return render_template('index1.html',id=uploads)

@app.route('/download1')
def download_file():
      path="C:/Users/HP/Desktop/opencv/market/static/uploads/logo.jpg"
      return send_file(path,as_attachment=True)

@app.route('/download/<upload_id>',methods=["GET","POST"])
@login_required
def download_url(upload_id):
    upload = Logo.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(upload.data), attachment_filename=upload.filename, as_attachment=True)

@app.route('/<int:id>',methods=["GET","POST"])
def get_img(id):
    uploads=Logo.query.filter_by(id=id).first()
    if not uploads:
        return 'Img Not Found!', 404

    return Response(uploads.data, mimetype='application/octet-stream')

