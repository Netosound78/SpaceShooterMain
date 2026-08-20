#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
import pygame.image
from pygame import Surface


class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./asset/Menu.png')
        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self, tex=None):

        pygame.mixer_music.load('./asset/Menu.mp3')
        pygame.mixer_music.play(-1)
        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            self.menu_text(50, tex:"Space Shooter", text_color=(255, 255, 255) text_center_pos:((WIN_WIDTH/2))

            pygame.display.flip()


            for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                       pygame.quit() # close window
                       quit()
    def menu(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont('Comic Sans MS', text_size)
        text_surf: Surface = text_font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(text_surf, text_rect)

    def menu_text(self, param, tex):
        pass