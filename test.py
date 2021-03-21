# from PIL import Image
#
# with Image.open('bullet.png') as image:
#     img=image.resize((30,30))
#     img.save('data/bullet.png')

import pygame
import random

SCREENRECT = pygame.Rect(0, 0, 800, 600).move_ip(10,20)

print(SCREENRECT.top)