from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app1 = Flask(__name__)


def create_connection():
    myclient = MongoClient("mongodb://localhost:27017")
    db = myclient["sensei"]
    stud_tab = db["student"]
    teach_tab = db["teacher"]
    book_hist = db["booking_history"]
    return [stud_tab,teach_tab,book_hist]


def create_teacher(username,email,password,experience,subjects,phone,academic_level,img_url):
    conn = create_connection()[1]
    hashed_password = generate_password_hash(password)
    subjects_s = {"physics":0,"music":0,"maths":0,"biology":0,"english":0}
    for ele in subjects.split():
        if ele in subjects:
            subjects_s[ele] = 1
    print(conn.insert_one({"name":username,"email":email,"password":hashed_password,"exp":experience,
                     "subjects":subjects_s,"phone_no":phone,"academic_level":academic_level,"img_url":img_url}))

def create_student(username, email, password, phone):  
    conn = create_connection()[0]
    hashed_password = generate_password_hash(password, method='pbkdf2:sha512', salt_length=16)
    print(conn.insert_one({"name":username,"email":email,"password":hashed_password,
                     "phone_no":phone}))

@app1.route("/chkpwd" , methods = ['POST'])
def checkpwd():
    data = request.json
    print(data)
    conn = create_connection()[0]
    input_pss = data['password']
    print(input_pss)
    compare_hash = conn.find_one({'email':data['email']})
    
     #check if null is retuned, if yes, then return only false
    if(not(compare_hash == None)):
        res = check_password_hash(compare_hash['password'],input_pss)
        print(res)
        # ratings = create_connection()[1]
        # bookings = ratings.find({"__id":})
        return [compare_hash['name'],res]
    else:
        return ["NoName",False]

@app1.route('/signup', methods=['GET','POST'])
def signup():
    data = request.json
    print(data)
    create_student(data['username'], data['email'], data['password'], data['phone'])
    return "ok"

@app1.route('/signup_t', methods=['GET','POST'])
def signup_t():
    data = request.json
    name = data['username'].split()
    nname = ''
    if(len(name) >1 ):
        data['img_url'] = name[0] + "_" + name[1]+".png"
    else:
        data['img_url'] = name[0] +".png"
    print(data)
    create_teacher(data['username'], data['email'], data['password'], data['experience'],data['subjects'],data['phone'] ,data['education_level'],data['img_url'])
    return "ok"

if __name__ == '__main__':
    app1.run(debug=True)