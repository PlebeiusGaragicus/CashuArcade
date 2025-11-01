import time
import logging
logger = logging.getLogger("lnarcade")

import pygame

from lnarcade.app import APP_SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT
from lnarcade.colors import *
from lnarcade.view import ViewState

def show_error(error_msg: str):
    # window = arcade.get_window()
    # window.show_view(ErrorView(error_msg))
    pass


class ErrorView(ViewState):
    def __init__(self, error_msg: str):
        self.error_msg = error_msg

        # None uses the default font
        self.font = pygame.font.SysFont(None, 15)
        self.text_surface = self.font.render(self.error_msg, True, pygame.Color('white'))
        # self.text_rect = self.text_surface.get_rect()

    def setup(self):
        pass

    def update(self, delta_time):
        pass

    def draw(self):
        APP_SCREEN.fill(RED)
        APP_SCREEN.blit(self.text_surface, (10, 15))
    
    def handle_event(self, event):
        pass



class ErrorModalView(ViewState):
    def __init__(self, toast_message: str, return_view: ViewState):
        super().__init__()
        self.message = toast_message
        self.start_time = None
        self.return_view = return_view

    def setup(self):
        self.start_time = time.time()

        self.font = pygame.font.SysFont(None, 15)

        self.txt_error = self.font.render("ERROR", True, pygame.Color('yellow'))
        self.txt_continue = self.font.render("PRESS <ENTER> TO CONTINUE", True, pygame.Color('blue'))
        self.txt_message = self.font.render(self.message, True, pygame.Color('white'))

    def update(self, delta_time):
        pass

    def draw(self):
        APP_SCREEN.fill(RED)

        APP_SCREEN.blit(self.txt_error, (SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.8))
        APP_SCREEN.blit(self.txt_continue, (SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.1))
        APP_SCREEN.blit(self.txt_message, (10, SCREEN_HEIGHT // 3))

        # arcade.draw_text("ERROR", self.width // 2, self.height * 0.8, arcade.color.YELLOW, font_size=30, anchor_x="center")
        # arcade.draw_text("PRESS <ENTER> TO CONTINUE", self.width // 2, self.height * 0.1, arcade.color.BLUE, font_size=30, anchor_x="center")
        # arcade.draw_text(self.message, 10, self.height // 3, arcade.color.WHITE, font_size=15, anchor_x="left")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.return_view is None:
                    pygame.quit()
                else:
                    from lnarcade.app import App
                    App.get_instance().manager.change_state(self.return_view)





# class ToastErrorView(ViewState):
#     def __init__(self, toast_message: str, return_view: arcade.View, time_limit: float = 5.0):
#         super().__init__()
#         self.message = toast_message
#         self.start_time = None
#         self.return_view = return_view
#         self.time_limit = time_limit

#     def on_show_view(self):
#         self.start_time = time.time()
#         # arcade.set_background_color(arcade.color.RED)

#         arcade.draw_ellipse_filled( arcade.get_window().width // 2, 50, arcade.get_window().width * 0.8, 60, arcade.color.RED)
#         arcade.draw_text(self.message, 10, 15, arcade.color.WHITE, font_size=15, anchor_x="left")

#     def on_update(self, delta_time):
#         if time.time() > self.start_time + self.time_limit:
#             App.get_instance().window.show_view( self.return_view )

#     def on_draw(self):
#         pass
