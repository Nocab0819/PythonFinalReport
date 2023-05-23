import pygame
import random

# 初始化 Pygame
pygame.init()

# 設置視窗大小和標題
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("拼字遊戲")

# 定義顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 定義字型和字型大小
FONT_SIZE = 40
font = pygame.font.Font(None, FONT_SIZE)

# 單字庫
word_list = ["apple", "banana", "cherry", "durian", "elderberry", "fig", "grape"]

# 生成單字和打亂字母順序
def generate_word():
    word = random.choice(word_list)
    word_letters = list(word)
    random.shuffle(word_letters)
    scrambled_word = "".join(word_letters)
    return word, scrambled_word

# 遊戲迴圈
score = 0
rounds = 3

for _ in range(rounds):
    word, scrambled_word = generate_word()
    input_text = ""
    confirmed = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not confirmed:
                        if input_text.strip().lower() == word:
                            score += 1
                        confirmed = True
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
        
        window.fill(WHITE)
        input_surface = font.render(input_text, True, BLACK)
        window.blit(input_surface, (20, 20))
        word_surface = font.render(scrambled_word, True, BLACK)
        window.blit(word_surface, (20, 100))
        pygame.display.update()
        
        if confirmed and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            input_text = ""
            confirmed = False
            break

# 顯示最終分數
final_score_surface = font.render("Final Score: " + str(score), True, BLACK)
window.blit(final_score_surface, (20, 200))
pygame.display.update()

# 等待使用者選擇再玩一次或結束
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    
    # 這裡可以顯示再玩一次或結束的選項，例如按鈕或文字
    # 這裡只是一個示例，你可以根據需要進行修改
    replay_surface = font.render("Play Again", True, BLACK)
    exit_surface = font.render("Exit", True, BLACK)
    window.blit(replay_surface, (20, 300))
    window.blit(exit_surface, (20, 350))
    pygame.display.update()
