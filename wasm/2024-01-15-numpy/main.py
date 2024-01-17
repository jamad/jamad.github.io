import pygame
import numpy as np #  "soon as possible" but just after the first import pygame - ref : https://www.reddit.com/r/pygame/comments/162qefm/pygbag_stops_working_when_importing_numpy/
import asyncio # step1

pygame.init() 

w=360
h=640
screen = pygame.display.set_mode((w,h) ) 

def colorgen():
    r=np.random.randint(0,128)
    g=np.random.randint(0,128)
    b=np.random.randint(0,128)
    return (r,b,g)
    
async def main(): # step2
    
    A=np.array([[colorgen() for _ in range(64)] for _ in range(36)])
    
    while True:
            
            diff=np.random.randint(-8,8)# 全てのデータに同じランダムな値を追加する
            A=np.clip(A + diff, 0, 255)# 0-255 にクリッピングする

            #画面クリア
            screen.fill((60,25,60)) 
            
            # ボタン描画

            for i in range(len(A)):
                for j in range(len(A[i])):
                    col=A[i][j]
                    pygame.draw.rect(screen,col,[9*i+9,9*j+9,5,5]) 	
            
            pygame.display.update() 
            
            await asyncio.sleep(0) # step3


if __name__ == "__main__":
    asyncio.run(main()) # step4