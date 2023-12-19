# reference https://stackoverflow.com/questions/69593109/how-to-use-pygame-touch-events-in-a-mobile-game

import pygame

pygame.init() 
SCREEN_IPHONE=(360,640)
myscreen = pygame.display.set_mode(SCREEN_IPHONE) 
myfont = pygame.font.SysFont(None,25)   
clock = pygame.time.Clock()

buttons = [
    pygame.Rect(25, 25, 100, 100),
    pygame.Rect(175, 25, 100, 100),
    pygame.Rect(25, 175, 100, 100),
    pygame.Rect(175, 175, 100, 100)]

colors = [(64, 0, 0), (64, 64, 0), (0, 64, 0), (0, 0, 64)]
colorsH = [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255)]

fingers = {}

# Create a player object
player = pygame.Surface((50, 50))
# Set the initial position of the player
player_pos = [175, 175]

player.fill((255, 0, 0))
greencolor=0

def mainloop():
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.FINGERDOWN:
            x = event.x * myscreen.get_height()
            y = event.y * myscreen.get_width()
            fingers[event.finger_id] = x, y
        if event.type == pygame.FINGERUP:
            fingers.pop(event.finger_id, None)

    highlight = []  
    for i, rect in enumerate(buttons): 
        touched = False
        for finger, pos in fingers.items():       
            if rect.collidepoint(pos):
                touched = True
        highlight.append(touched)   

    myscreen.fill(0)
    for rect, color, colorH, h in zip(buttons, colors, colorsH, highlight):
        c = colorH if h else color
        pygame.draw.rect(myscreen, c, rect)
    pygame.display.flip()

if __name__=='__main__':
    while 1:mainloop()





