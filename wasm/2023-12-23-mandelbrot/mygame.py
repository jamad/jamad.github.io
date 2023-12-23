
import pygame
import numpy as np


# マンデルブロ集合を生成する関数
def mandelbrot(c, max_iterations):
    z = np.zeros_like(c)
    n = np.zeros(c.shape, dtype=int)
    mask = np.full(c.shape[:2], True, dtype=bool)

    for i in range(max_iterations):
        z[mask] = z[mask] * z[mask] + c[mask]
        mask = abs(z) <= 2
        n[mask] = i
        
    return n

# マンデルブロ集合を描画する関数
def draw_mandelbrot(screen, size, offset_x, offset_y, scale, max_iter):
    x = np.linspace(-size//2, size//2, size)
    y = np.linspace(-size//2, size//2, size)
    real, imaginary = np.meshgrid(x, y)

    real = real * scale + offset_x
    imaginary = imaginary * scale + offset_y
    c = real + 1j * imaginary

    mandelbrot_set = mandelbrot(c, max_iter)
    colors = np.uint8(mandelbrot_set * 255 / max_iter)

    # Pygameのピクセル配列に色を適用
    surfarray = pygame.surfarray.pixels3d(screen)
    surfarray[:SIZE, :SIZE] = np.stack((colors, colors, colors), axis=-1).transpose((1, 0, 2))  # 転置を追加


pygame.init()

# 画面サイズと画面オブジェクトの生成
SIZE= 512
screen = pygame.display.set_mode((SIZE, SIZE+200))
pygame.display.set_caption('Mandelbrot Set')

offset_x, offset_y = -0.5, 0  # 初期位置
scale = 0.01  # 初期スケール

INIT_ITER=16  # 初期のイテレーション数
max_iter = INIT_ITER 

def draw_buttons(screen):
    # ボタンの位置とサイズ
    button_up =         pygame.Rect(100, 25+SIZE+0, 50, 50)
    button_down =       pygame.Rect(100, 25+SIZE+100, 50, 50)
    button_left =       pygame.Rect( 50, 25+SIZE+50, 50, 50)
    button_right =      pygame.Rect(150, 25+SIZE+50, 50, 50)
    button_zoom_in =    pygame.Rect(400, 25+SIZE+0, 50, 50)
    button_zoom_out =   pygame.Rect(400, 25+SIZE+100, 50, 50)

    # ボタンの描画
    pygame.draw.rect(screen, (255, 0, 0), button_up)
    pygame.draw.rect(screen, (255, 0, 0), button_down)
    pygame.draw.rect(screen, (255, 0, 0), button_left)
    pygame.draw.rect(screen, (255, 0, 0), button_right)
    pygame.draw.rect(screen, (255, 0, 0), button_zoom_in)
    pygame.draw.rect(screen, (255, 0, 0), button_zoom_out)

    return button_up, button_down, button_left, button_right, button_zoom_in, button_zoom_out


def mainloop():
    global max_iter, scale, offset_x, offset_y, INIT_ITER
    
    # マンデルブロ集合を描画
    draw_mandelbrot(screen, SIZE, offset_x, offset_y, scale, max_iter)

    # ボタンを描画
    buttons = draw_buttons(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # マウスクリックがボタンの範囲内かチェック
            if   buttons[0].collidepoint(mouse_pos):                offset_y -= 10 * scale  # 上ボタン
            elif buttons[1].collidepoint(mouse_pos):                offset_y += 10 * scale  # 下ボタン
            elif buttons[2].collidepoint(mouse_pos):                offset_x -= 10 * scale  # 左ボタン
            elif buttons[3].collidepoint(mouse_pos):                offset_x += 10 * scale  # 右ボタン
            elif buttons[4].collidepoint(mouse_pos):
                scale *= 1.2  # ズームインボタン
                max_iter = INIT_ITER
            elif buttons[5].collidepoint(mouse_pos):
                scale /= 1.2  # ズームアウトボタン
                max_iter = INIT_ITER

    
    # 画面更新
    pygame.display.flip()

if __name__=='__main__':
    while 1:mainloop()