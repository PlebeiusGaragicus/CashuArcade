import time
import logging
logger = logging.getLogger()

import pygame

from lnarcade.app import APP_SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT
from lnarcade.view import ViewState
from lnarcade.colors import *

FONT_SIZE = 30

class SplashScreen(ViewState):
    def __init__(self):
        super().__init__()


    def setup(self):
        print(f"{self.__class__.__name__} setup")
        self.alpha = 0
        self.font = pygame.font.Font(None, 74)
        self.text = self.font.render('Loading screen...', True, RED)
        self.text_rect = self.text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
        self.start_text = self.font.render('Press Space to Start', True, GREEN)
        self.start_text_rect = self.start_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))


    def update(self):
        pass


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                from lnarcade.app import App
                App.get_instance().manager.change_state("game_select")



    def draw(self):
        APP_SCREEN.fill(DARK)

        self.start_text.set_alpha(self.alpha)
        self.alpha = min(self.alpha + 15, 255)

        APP_SCREEN.blit(self.text, self.text_rect)
        APP_SCREEN.blit(self.start_text, self.start_text_rect)
