import os
script_path = os.path.realpath(__file__)
script_directory = os.path.dirname(script_path)


import datetime
import pygame

pygame.init() 
SCREEN_IPHONE=(360,640)
myscreen = pygame.display.set_mode(SCREEN_IPHONE) 
myfont = pygame.font.SysFont(None,25) 

pygame.display.set_caption('simple clock')            


SCREEN = pygame.Rect(0, 0, 360, 640)
# バドルのクラス
class Paddle(pygame.sprite.Sprite):
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load(filename).convert()  #fileから画像をゲット
        self.rect = self.image.get_rect()               #画像から大きさゲット
        self.rect.bottom = SCREEN.bottom - 20           # パドルのy座標は固定で下から20pixel
    def update(self):
        self.rect.centerx = pygame.mouse.get_pos()[0]       # マウスのx座標をパドルのx座標に
        self.rect.clamp_ip(SCREEN)                      # ゲーム画面内のみで移動

def maincore():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SCREEN.size)
    group = pygame.sprite.RenderUpdates()               # 描画用のスプライトグループ
    Paddle.containers = group
    paddle = Paddle(script_directory+"\paddle.png")                   # パドルの作成
    while 1:
        clock.tick(120)      # フレームレート(120fps)
        screen.fill((0,20,0))#全消し
        group.update()        # 全てのスプライトグループを更新
        group.draw(screen)    # 全てのスプライトグループを描画
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                


############################# 下記はpygbag用コード（固定）
import asyncio # step1

async def main(): # step2
	while 1:  	
		maincore()
		await asyncio.sleep(0) # step3

asyncio.run(main()) # step4