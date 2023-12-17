import pygame
import asyncio

pygame.init()
window = pygame.display.set_mode((640, 480))
font = pygame.font.Font(None, 36)

async def main():
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                text = font.render(f"Pressed: {pygame.key.name(event.key)}", True,(255, 255, 255) )
                window.fill((0, 0, 0))
                window.blit(text, (320, 240))
                pygame.display.flip()

        await asyncio.sleep(0)

asyncio.run(main())