from flask import Flask, render_template, request, redirect, session, url_for
import os
import random

app = Flask(__name__)
# 生成一個 24 個字節的隨機字串作為密鑰
app.secret_key = os.urandom(24)

questions = 10
used_words = []

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
        session['score'] = 0
        session['current_round'] = 1
        session['current_word'] = get_random_word()
        session['shuffled_word'] = list(session['current_word'])
        random.shuffle(session['shuffled_word'])
        session['shuffled_word'] = ''.join(session['shuffled_word'])

    if request.method == 'POST':
        user_word = request.form['word'].lower()
        if user_word == session['current_word']:
            session['score'] += 1

        if session['current_round'] < questions:
            session['current_round'] += 1
            session['current_word'] = get_random_word()
            session['shuffled_word'] = list(session['current_word'])
            random.shuffle(session['shuffled_word'])
            session['shuffled_word'] = ''.join(session['shuffled_word'])
        else:
            return redirect('/score/result')

    return render_template('game.html', shuffled_word=session['shuffled_word'], question=session['current_round'])

@app.route('/score/result', methods=['GET', 'POST'])
def show_score():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('game'))

    score = session['score']
    if score >= 6:
        message = "You Pass!"
    else:
        message = "You Failed"
    return render_template('score.html', score=score, questions=questions, message=message)


def get_words():
    words = [
        'apple', 'banana', 'cherry', 'orange', 'mango',
        'strawberry', 'kiwi', 'pineapple', 'grape',
        'blueberry', 'pear', 'peach', 'avocado',
        'coconut', 'papaya', 'guava', 'watermelon'
    ]
    return words

def get_random_word():
    available_words = [word for word in get_words() if word not in used_words]
    if len(available_words) == 0:
        # 若所有單字都已經用過，則重新開始遊戲並重置已用單字列表
        global used_words
        used_words = []
        return random.choice(get_words())
    else:
        word = random.choice(available_words)
        used_words.append(word)
        return word


if __name__ == '__main__':
    app.run()
