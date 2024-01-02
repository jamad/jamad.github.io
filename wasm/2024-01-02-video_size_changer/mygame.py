import tkinter as tk
from tkinter import filedialog
import pygame

def play_video(file_path):
    # ここでファイルパスを使って動画を再生するなどの処理を行う
    pass


def select_file():
    root = tk.Tk()
    root.withdraw()  # メインウィンドウを非表示にする

    file_path = filedialog.askopenfilename()
    if file_path:
        print("選択されたファイルパス:", file_path)
        play_video(file_path)  # ファイルパスを使って動画を再生するなどの処理を行う
    else:
        print("ファイルが選択されていません")
    
    return file_path

import asyncio # step1

import pygame
pygame.init() 

w=360
h=640
button_w=240
button_h=40
screen = pygame.display.set_mode((w,h) ) 
smallfont = pygame.font.SysFont('Corbel',35) 

async def main(): # step2
    selected_filename=''
    while True:
            x,y = pygame.mouse.get_pos() 
            hoverover=0 <= x-50 <= button_w and 0 <= y-50 <= button_h
            for ev in pygame.event.get(): 
                  if (ev.type == pygame.MOUSEBUTTONDOWN and hoverover): 
                        selected_filename=select_file()  # Tkinter を使用してファイルを選択する関数を呼び出す
            #画面クリア
            screen.fill((60,25,60)) 
            
            # ボタン描画
            pygame.draw.rect(screen,((100,100,100) ,(170,170,170) )[hoverover],[50,50,button_w,button_h]) 	
            
            # ボタン文字表示
            if selected_filename=='':
                text = smallfont.render('select movie file' , True , (255,255,255) )
            else:
                text = smallfont.render(selected_filename , True , (255,255,255) )
            screen.blit(text , (50+10,50)) 

            pygame.display.update() 
            
            await asyncio.sleep(0) # step3


if __name__ == "__main__":
    asyncio.run(main()) # step4