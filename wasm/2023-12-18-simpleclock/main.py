
import datetime
import pygame

pygame.init() 
SCREEN_IPHONE=(360,640)
myscreen = pygame.display.set_mode(SCREEN_IPHONE) 
myfont = pygame.font.SysFont(None,25) 

pygame.display.set_caption('simple clock')            

def maincore():
    mytext = myfont.render(str(datetime.datetime.now()), True, (255,255,255)) 
    myscreen.fill((0,0,0)) 
    myscreen.blit(mytext, [20, 8])
    pygame.display.update()

############################# 下記はpygbag用コード（固定）
import asyncio # step1

async def main(): # step2
	while 1:  	
		maincore()
		await asyncio.sleep(0) # step3

asyncio.run(main()) # step4