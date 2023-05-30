from flask import Flask, render_template, request, redirect, session, url_for
import os
import random

app = Flask(__name__)
app.secret_key = os.urandom(24)

# 可自行設定回合數和文字內容
rounds = 3
words = ['apple', 'banana', 'cherry', 'orange', 'mango']

@app.route('/', methods=['GET', 'POST'])
def index():
    # 如果收到 POST 請求，將使用者導向遊戲頁面
    if request.method == 'POST':
        return redirect(url_for('game'))
    else:
        session.clear()
        return render_template('welcome.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    # 檢查是否有計分的會話，若無則初始化相關會話變數
    if 'score' not in session:
        session['score'] = 0
        session['current_round'] = 1
        session['current_word'] = random.choice(words)
        session['shuffled_word'] = list(session['current_word'])
        random.shuffle(session['shuffled_word'])
        session['shuffled_word'] = ''.join(session['shuffled_word'])

    if request.method == 'POST':
        # 取得使用者輸入的單字並轉換為小寫
        user_word = request.form['word'].lower()
        if user_word == session['current_word']:
            session['score'] += 1

        if session['current_round'] < rounds:
            # 若還有回合，則更新相關會話變數
            session['current_round'] += 1
            session['current_word'] = random.choice(words)
            session['shuffled_word'] = list(session['current_word'])
            random.shuffle(session['shuffled_word'])
            session['shuffled_word'] = ''.join(session['shuffled_word'])
        else:
            # 若回合結束，導向分數結果頁面
            return redirect('/score/result')

    return render_template('game.html', shuffled_word=session['shuffled_word'], round=session['current_round'])

@app.route('/score/result', methods=['GET', 'POST'])
def show_score():
    if request.method == 'POST':
        # 若收到 POST 請求，則清除會話並重新導向遊戲頁面
        session.clear()
        return redirect(url_for('game'))

    score = session['score']
    return render_template('score.html', score=score, rounds=rounds)


if __name__ == '__main__':
    app.run()
