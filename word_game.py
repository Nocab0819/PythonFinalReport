import pygame
import random

# 初始化 Pygame
pygame.init()

# 設定遊戲視窗大小
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("拼字遊戲")

# 定義顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 設定字體
FONT_SIZE = 48
font = pygame.font.Font(None, FONT_SIZE)

# 定義遊戲參數
rounds = 3  # 遊戲回合數
score = 0  # 分數
current_round = 1  # 目前回合數

def generate_word():
    # 從單字清單中隨機選擇一個單字
    word_list = ["apple", "banana", "cherry", "date", "elderberry"]
    word = random.choice(word_list)
    
    # 打亂單字的字母順序
    word_letters = list(word)
    random.shuffle(word_letters)
    scrambled_word = "".join(word_letters)
    
    return word, scrambled_word

def display_message(text):
    # 在視窗中心顯示一則訊息
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
    window.blit(text_surface, text_rect)
    pygame.display.update()

def game_loop():
    global score, current_round
    
    while current_round <= rounds:
        # 遊戲迴圈
        
        # 重設遊戲狀態
        word, scrambled_word = generate_word()
        input_text = ""
        
        while True:
            # 處理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # 確認輸入是否正確
                        if input_text.lower() == word:
                            score += 1
                        break
                    elif event.key == pygame.K_BACKSPACE:
                        # 刪除最後一個輸入的字母
                        input_text = input_text[:-1]
                    else:
                        # 添加輸入的字母到輸入文字串
                        input_text += event.unicode
            
            # 更新遊戲畫面
            window.fill(WHITE)
            input_surface = font.render(input_text, True, BLACK)
            window.blit(input_surface, (20, 20))
            word_surface = font.render(scrambled_word, True, BLACK)
            window.blit(word_surface, (20, 100))
            pygame.display.update()
            
            if input_text.lower() == word:
                break
        
        # 進入下一回合
        current_round += 1
    
    # 顯示最終分數
    display_message("遊戲結束，你的分數為: {}".format(score))
    
    # 顯示再玩一次或結束的選項
    display_message("再玩一次（R）或結束（Q）？")
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # 重新開始遊戲
                    score = 0
                    current_round = 1
                    game_loop()
                elif event.key == pygame.K_q:
                    # 結束遊戲
                    pygame.quit()
                    quit()

# 開始遊戲
game_loop()