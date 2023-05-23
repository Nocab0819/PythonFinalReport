from flask import Flask, render_template, request
import random

app = Flask(__name__)

words = ["apple", "banana", "cherry"]  # 單字庫
rounds = 3  # 回合數

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/play', methods=['GET', 'POST'])
def play_game():
    score = 0  # 分數
    current_round = 1  # 目前回合
    current_word = ""  # 目前的單字
    scrambled_word = ""  # 打亂順序後的單字

    def get_random_word():
        return random.choice(words)

    def scramble_word(word):
        letters = list(word)
        random.shuffle(letters)
        return ''.join(letters)

    def check_answer(user_answer):
        return user_answer.lower() == current_word.lower()

    def update_game_state():
        nonlocal score, current_round, current_word, scrambled_word
        if current_round <= rounds:
            current_word = get_random_word()
            scrambled_word = scramble_word(current_word)
        else:
            current_word = ""
            scrambled_word = ""
        score += 1

    if request.method == 'POST':
        user_answer = request.form['answer']
        if check_answer(user_answer):
            update_game_state()

    return render_template('game.html', score=score, word=current_word, scrambled_word=scrambled_word)

if __name__ == '__main__':
    app.run()
