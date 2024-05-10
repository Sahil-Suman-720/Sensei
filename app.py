from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

class ContentBasedFiltering:
    def __init__(self, user_preferences, item_matrix):
        self.user_preferences = user_preferences
        self.item_matrix = item_matrix
        self.similarity_scores = cosine_similarity(user_preferences, item_matrix)

    def recommend(self, unrated_teachers):
        # Compute similarity scores between the user's preferences and all unrated teachers
        similarity_to_unrated_teachers = cosine_similarity(self.user_preferences, unrated_teachers)

        # Combine the similarity scores with the existing scores for all unrated teachers
        combined_scores = self.similarity_scores * similarity_to_unrated_teachers.T

        # Calculate the recommendation scores for each teacher
        recommendation_scores = np.mean(combined_scores, axis=0)

        # Sort the teachers based on recommendation scores
        sorted_indices = np.argsort(recommendation_scores)[::-1]

        return sorted_indices

# Example user preferences (only one user)
user_preferences = np.array([
    [5, 4, 0, 0, 3]  # User 1 preferences
])

# Example item matrix (items as rows, features as columns)
item_matrix = np.array([
    [1, 1, 0, 1, 0],  # Teacher 1: Physics, Math, Music
    [1, 1, 1, 0, 0],  # Teacher 2: Physics, Math, Music, Filmmaking
    [0, 1, 0, 0, 1],  # Teacher 3: Math, Filmmaking
    [1, 0, 1, 0, 1],  # Teacher 4: Physics, Music, Filmmaking
    [0, 0, 1, 1, 0]   # Teacher 5: Music, Filmmaking
])

# Unrated teachers (each row represents features of an unrated teacher)
unrated_teachers = np.array([
    [1, 1, 0, 0, 0],  # Unrated Teacher 1: Physics, Math
    [0, 0, 1, 1, 0],  # Unrated Teacher 2: Music, Filmmaking
    [1, 0, 0, 0, 1],  # Unrated Teacher 3: Physics, Filmmaking
    [0, 1, 1, 0, 0],  # Unrated Teacher 4: Math, Music
    [0, 1, 0, 1, 0]   # Unrated Teacher 5: Math, Filmmaking
])

cbf = ContentBasedFiltering(user_preferences, item_matrix)

recommended_order = cbf.recommend(unrated_teachers)

print("Recommended order of teachers based on similarity for all unrated teachers:")
for idx in recommended_order:
    print(f"Teacher {idx+1}")


def create_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='ss_2024',
        password='Yuiop@7890',
        database='sensei'
    )
    return conn

def create_user(username, email, password, interests, academic_level,phone):
    conn = create_connection()
    cur = conn.cursor()
    hashed_password = generate_password_hash(password)
    cur.execute("INSERT INTO student (StudentName, Education_level, Interest,Phone,Email, Password) VALUES (%s, %s, %s, %s, %s,%s)",
                (username,academic_level,interests,phone, email, hashed_password))
    conn.commit()
    conn.close()

def get_user_by_email(email):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    conn.close()
    return user

@app.route('/recommendations')
def recc():
    pass

@app.route('/show',methods = ["POST"])
def display():
    conn = create_connection()
    print(conn)
    cur = conn.cursor()
    cur.execute("select * from student")
    data = cur.fetchall()
    for x in data:
        print("data:",x)
    return data
    # print(data)
    # return data

@app.route('/signup', methods=['GET','POST'])
def signup():
    data = request.json
    print(data)
    create_user(data['username'], data['email'], data['password'], data['interests'], data['Education_level'],data['phone'])
    return "ok"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = get_user_by_email(email)
        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            return redirect(url_for('profile'))
        else:
            error = 'Invalid email or password'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'user_id' in session:
        user_id = session['user_id']
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        conn.close()
        return render_template('profile.html', user=user)
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    display()
    