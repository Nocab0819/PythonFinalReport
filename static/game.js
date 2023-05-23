// 遊戲相關變數
var words = ["apple", "banana", "cherry"];  // 單字庫
var currentWordIndex = 0;  // 目前單字的索引
var currentWord = "";  // 目前的單字
var scrambledWord = "";  // 打亂順序後的單字
var score = 0;  // 分數
var rounds = 3;  // 回合數
var currentRound = 1;  // 目前回合

// 獲取隨機單字
function getRandomWord() {
    return words[Math.floor(Math.random() * words.length)];
}

// 打亂單字的順序
function scrambleWord(word) {
    var letters = word.split('');
    for (var i = letters.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var temp = letters[i];
        letters[i] = letters[j];
        letters[j] = temp;
    }
    return letters.join('');
}

// 遊戲初始化
function initializeGame() {
    currentWord = getRandomWord();
    scrambledWord = scrambleWord(currentWord);
    score = 0;
    currentRound = 1;
}

// 顯示遊戲畫面
function displayGameScreen() {
    // 在這裡設計您的遊戲畫面
    // 可以使用 HTML 元素和 JavaScript 操控 DOM 元素來顯示單字、輸入框、按鈕等
}

// 處理用戶提交答案
function handleAnswerSubmit() {
    // 獲取用戶輸入的答案
    var userAnswer = document.getElementById('answerInput').value;

    // 比對答案
    if (userAnswer.toLowerCase() === currentWord.toLowerCase()) {
        score++;
    }

    // 進入下一題或下一回合
    if (currentRound < rounds) {
        currentRound++;
        currentWord = getRandomWord();
        scrambledWord = scrambleWord(currentWord);
        displayGameScreen();
    } else {
        // 遊戲結束，顯示分數和再玩一次選項
        // 可以使用彈出視窗、警示框或修改 DOM 元素來顯示分數和再玩一次選項
    }
}

// 遊戲初始化
initializeGame();

// 顯示遊戲畫面
displayGameScreen();
