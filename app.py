"""
檔名：app.py
功能：拼字遊戲

這個程式使用 Flask 框架來建立一個網頁應用程式。
使用者可以透過瀏覽器訪問首頁("/")，並在首頁上開始遊戲。
分別為教師和學生功能，教師可以註冊帳號密碼，並且登入以建立或更新專屬題庫。
學生輸入教師帳號名稱後，即可進入專屬題庫作答。
當使用者提交答案時，程式會檢查答案是否正確，並根據結果更新使用者的分數。
程式會顯示每個回合的單字題目，並將單字的字母順序打亂後顯示給使用者。
若使用者答對，分數將增加；若答錯，將錯誤的單字加入錯誤列表。
遊戲結束後，使用者可以查看最終分數、遊戲結果訊息和答錯的單字列表。
如果使用者選擇重新開始遊戲，分數和錯誤列表將被重置。
"""
from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 設置一個隨機的密鑰用於 Flask 的 session

questions = 10
used_words = []  # 已使用的單字列表
wrong_words = []  # 答錯的單字列表

conn = sqlite3.connect('users.db')
c = conn.cursor()

# 資料庫初始化函式
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                (username TEXT PRIMARY KEY, password TEXT, input_data TEXT)''')
    conn.commit()
    conn.close()

# 首頁
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'student_login' in request.form:
            return redirect(url_for('welcome'))
        elif 'teacher_login' in request.form:
            return redirect(url_for('login'))
    else:
        session.clear()
        return render_template('index.html')
    
# 教師註冊頁面
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        # 檢查帳號是否已經存在
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = c.fetchone()
        if existing_user:
            flash('The account already exists.')
            return render_template('register.html', error_message='The account already exists.')

        # 寫入新的使用者到資料庫
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

        flash('Registration successful.')
        return redirect(url_for('login'))

    return render_template('register.html', back_url=url_for('index'), login_url=url_for('login'))

# 教師登入頁面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        # 檢查帳號是否存在
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = c.fetchone()
        if not existing_user:
            flash('The account does not exist.')
            return render_template('login.html', error_message='The account does not exist.')

        # 檢查密碼是否正確
        if password != existing_user[1]:
            flash('Incorrect password.')
            return render_template('login.html', error_message='Incorrect password.')

        # 登入成功，設置 session
        session['username'] = username
        
        # 讓 dashboard 在使用者尚未重新輸入資料前就能吃到資料庫中該使用者 input_data 的資料內容
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT input_data FROM users WHERE username=?", (username,))
        result = c.fetchone()
        input_data = result[0] if result else ''
        conn.close()

        flash('Login successful.')
        return render_template('dashboard.html', logout_url=url_for('index'), input_data=input_data)

    return render_template('login.html', back_url=url_for('index'))

# 檢查輸入是否為英文單字並以逗號隔開
def validate_input(input_data):
    words = input_data.split(',')
    for word in words:
        if not word.isalpha():
            return False
    return True

# 將輸入訊息存入資料庫中對應的使用者記錄
def save_input_to_database(input_data, username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # 檢查使用者是否已輸入過訊息
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    existing_user = c.fetchone()

    if existing_user:
        # 更新資料庫中的訊息
        c.execute("UPDATE users SET input_data=? WHERE username=?", (input_data, username))
    else:
        flash('User does not exist.', 'error')

    conn.commit()
    conn.close()

# 教師管理介面
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # 檢查使用者是否已登入
    if 'username' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        input_data = request.form.get('input_data')

        # 檢查輸入是否為英文單字並以逗號隔開
        if input_data and validate_input(input_data):
            # 獲取使用者名稱
            username = session['username']

            # 將輸入訊息存入資料庫
            save_input_to_database(input_data, username)

            flash('Question bank saved successfully!')
        else:
            flash('Please enter English words separated by commas.', 'error')
        
        # 取得目前使用者資料庫中的 input_data
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT input_data FROM users WHERE username=?", (session['username'],))
        result = c.fetchone()
        input_data = result[0] if result else ''
        conn.close()

        return render_template('dashboard.html', logout_url=url_for('index'), input_data=input_data)

    return render_template('dashboard.html', logout_url=url_for('index'))


# 學生登入驗證
def authenticate_teacher(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    return result is not None

@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        username = request.form.get('username')

        if authenticate_teacher(username):
            session['username'] = username
            return redirect(url_for('game'))
        else:
            return redirect(url_for('welcome', error_message='Account error.'))
        
    return render_template('welcome.html', back_url=url_for('index'))

def get_teacher_input_data(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT input_data FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    if result:
        input_data = result[0]
        return input_data.split(',')  # 將 input_data 字串以逗號分隔並轉為陣列
    return []

def get_random_word(input_data):
    if input_data:
        used_words = session.get('used_words', [])  # 獲取已經使用過的單字列表
        available_words = [word for word in input_data if word not in used_words]  # 過濾掉已使用的單字
        if not available_words:
            # 如果所有單字都已經使用過，則重新初始化已使用單字列表
            used_words = []
            available_words = input_data.copy()  # 使用副本，避免修改原始的 input_data
        random_word = random.choice(available_words)
        used_words.append(random_word)  # 將選中的單字加入已使用列表
        session['used_words'] = used_words  # 更新已使用單字列表到 session 中
        input_data.remove(random_word)  # 從 input_data 中移除已使用的單字
        return random_word
    return None

@app.route('/game', methods=['GET', 'POST'])
def game():
    if 'score' not in session:
        wrong_words.clear()
        session['score'] = 0
        session['current_round'] = 1
        session['used_words'] = []  # 初始化已使用單字列表
    
    if 'username' in session:
        username = session['username']
        input_data = session.get('input_data')  # 從 session 中獲取 input_data
        if input_data is None:
            input_data = get_teacher_input_data(username)
            session['input_data'] = input_data
        
        used_words = session['used_words']  # 獲取已經使用過的單字列表
        
        if 'current_word' not in session:
            session['current_word'] = get_random_word(input_data)  # 獲取一個新的單字題目
            session['shuffled_word'] = list(session['current_word'])  # 將單字打亂作為題目展示
            random.shuffle(session['shuffled_word'])
            session['shuffled_word'] = ''.join(session['shuffled_word'])

    if request.method == 'POST':
        user_word = request.form['word'].lower()
        if user_word == session['current_word']:
            session['score'] += 1  # 答對了，增加分數
        else:
            wrong_words.append(session['current_word'])  # 答錯了，將錯誤的單字加入錯誤列表

        if session['current_round'] < questions:
            session['current_round'] += 1
            session['current_word'] = get_random_word(input_data)  # 獲取一個新的單字題目
            session['shuffled_word'] = list(session['current_word'])  # 將單字打亂作為題目展示
            random.shuffle(session['shuffled_word'])
            session['shuffled_word'] = ''.join(session['shuffled_word'])
        else:
            session['used_words'] = []  # 重新初始化已使用單字列表
            session.modified = True  # 標記 session 物件已被修改
            return redirect(url_for('score'))  # 遊戲結束，跳轉到結果頁面

    return render_template('game.html', shuffled_word=session['shuffled_word'], question=session['current_round'])

@app.route('/score', methods=['GET', 'POST'])
def score():
    used_words.clear()  # 清空已使用的單字列表
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('welcome'))

    score = session['score']
    if score >= 6:
        message = "You Pass!"
    else:
        message = "You Failed"
    return render_template('score.html', score=score, questions=questions, message=message, wrong_words=wrong_words)

if __name__ == '__main__':
    init_db()  # 初始化資料庫
    app.run()
