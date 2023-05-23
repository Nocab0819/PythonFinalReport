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
GRAY = (200, 200, 200)

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

# 創建 "再玩一次" 和 "結束" 按鈕的矩形
replay_button_rect = pygame.Rect(20, 300, 200, 50)
exit_button_rect = pygame.Rect(20, 350, 200, 50)

while True:
    replay_button_color = GRAY if replay_button_rect.collidepoint(pygame.mouse.get_pos()) else WHITE
    exit_button_color = GRAY if exit_button_rect.collidepoint(pygame.mouse.get_pos()) else WHITE

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if replay_button_rect.collidepoint(mouse_pos):
                score = 0  # 重置分數
                for _ in range(rounds):  # 再玩一次
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
            elif exit_button_rect.collidepoint(mouse_pos):
                pygame.quit()
                quit()

    # 重新設定結束畫面
    window.fill(WHITE)
    replay_button_surface = font.render("Play Again", True, BLACK)
    exit_button_surface = font.render("Exit", True, BLACK)
    window.blit(replay_button_surface, (replay_button_rect.x + 10, replay_button_rect.y + 10))
    window.blit(exit_button_surface, (exit_button_rect.x + 10, exit_button_rect.y + 10))
    score_surface = font.render("Score: " + str(score), True, BLACK)
    window.blit(score_surface, (20, 250))
    pygame.draw.rect(window, replay_button_color, replay_button_rect)
    pygame.draw.rect(window, exit_button_color, exit_button_rect)
    window.blit(replay_button_surface, (replay_button_rect.x + 10, replay_button_rect.y + 10))
    window.blit(exit_button_surface, (exit_button_rect.x + 10, exit_button_rect.y + 10))
    pygame.display.update()