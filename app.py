"""
檔名：app.py
功能：拼字遊戲

這個程式使用 Flask 框架來建立一個網頁應用程式。
使用者可以透過瀏覽器訪問首頁("/")，並在首頁上開始遊戲。
當使用者提交答案時，程式會檢查答案是否正確，並根據結果更新使用者的分數。
程式會顯示每個回合的單字題目，並將單字的字母順序打亂後顯示給使用者。
若使用者答對，分數將增加；若答錯，將錯誤的單字加入錯誤列表。
遊戲結束後，使用者可以查看最終分數、遊戲結果訊息和答錯的單字列表。
如果使用者選擇重新開始遊戲，分數和錯誤列表將被重置。
"""
from flask import Flask, render_template, request, redirect, session, url_for
import os
import random
from setmode.config import get_words

app = Flask(__name__)
# 生成一個 24 個字節的隨機字串作為密鑰
app.secret_key = os.urandom(24)

questions = 10
used_words = []  # 已使用的單字列表
wrong_words = []  # 答錯的單字列表

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('game'))
    else:
        session.clear()
        return render_template('welcome.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    if 'score' not in session:
        wrong_words.clear()
        session['score'] = 0
        session['current_round'] = 1
        session['current_word'] = get_random_word()  # 獲取一個新的單字題目
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
            session['current_word'] = get_random_word()  # 獲取一個新的單字題目
            session['shuffled_word'] = list(session['current_word'])  # 將單字打亂作為題目展示
            random.shuffle(session['shuffled_word'])
            session['shuffled_word'] = ''.join(session['shuffled_word'])
        else:
            return redirect('/score/result')  # 遊戲結束，跳轉到結果頁面

    return render_template('game.html', shuffled_word=session['shuffled_word'], question=session['current_round'])

@app.route('/score/result', methods=['GET', 'POST'])
def show_score():
    used_words.clear()  # 清空已使用的單字列表
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('game'))

    score = session['score']
    if score >= 6:
        message = "You Pass!"
    else:
        message = "You Failed"
    return render_template('score.html', score=score, questions=questions, message=message, wrong_words=wrong_words)

def get_random_word():
    available_words = [word for word in get_words() if word not in used_words]  # 過濾掉已使用的單字
    if len(available_words) == 0:
        global used_words
        used_words = []  # 若所有單字都已經用過，則重新開始遊戲並重置已使用的單字列表
        return random.choice(get_words())
    else:
        word = random.choice(available_words)
        used_words.append(word)  # 將選擇的單字加入已使用的單字列表
        return word


if __name__ == '__main__':
    app.run()
