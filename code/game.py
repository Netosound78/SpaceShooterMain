#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from code.menu import Menu


from const import WIN_HEIGHT, WIN_WIDTH




class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((800, 600))

    def run(self):


        while True:
            menu = Menu(self.window)
            menu.run()
            pass 


