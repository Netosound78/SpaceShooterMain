import pygame

print('Setup Start')
pygame.init()
screen = pygame.display.set_mode((800, 600))
print('Setup End')


print('Loop Start')
while True:
    pass
    # Check for all events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() # close window
            quit() # end pygame

