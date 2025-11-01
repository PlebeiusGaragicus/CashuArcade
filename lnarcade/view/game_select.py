import os
import platform
import time
import logging
logger = logging.getLogger()

from dataclasses import dataclass
import subprocess


import pygame

from lnarcade.app import App, APP_SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT
from lnarcade.config import APP_FOLDER, MY_DIR
from lnarcade.colors import *
from lnarcade.utilities.find_games import get_app_manifests
from lnarcade.view import ViewState
from lnarcade.view.error import ErrorModalView



@dataclass
class GameListItem:
    module_name: str
    game_name: str
    manifest_dict: dict
    image_path: str
    image: pygame.Surface = None

    def __post_init__(self):  # This method is automatically called after `__init__`
        try:
            self.image = pygame.image.load(self.image_path)
        except pygame.error:  # Pygame raises a generic error for file not found
            image_path = os.path.expanduser(f"{MY_DIR}/resources/img/missing.jpg")
            self.image = pygame.image.load(image_path)




class GameSelectView(ViewState):
    def __init__(self):
        super().__init__()
        # self.screen = APP_SCREEN
        self.alpha = 0  # initialize alpha to 0 (fully transparent)
        self.mouse_pos = (0, 0)
        self.selected_index = 0
        self.last_input_time = time.time()
        self.menu_items: list = []
        self.credits: int = 0

        self.A_held = False
        self.show_mouse_pos = False

        manifests = get_app_manifests()
        logger.debug("manifests: %s", manifests)

        for (app_folder_name, manifest_dict) in manifests.items():
            image_path = os.path.expanduser(f"~/{APP_FOLDER}/{app_folder_name}/image.png")

            try:
                game_name = f"{manifest_dict['name']}"

                self.menu_items.append( GameListItem(app_folder_name, game_name, manifest_dict, image_path) )
            except KeyError:
                logger.error(f"KeyError in {app_folder_name} manifest.json")
                continue

        logger.debug("self.menu_items: %s", self.menu_items)


    def setup(self):
        # arcade.set_background_color(arcade.color.BLACK)
        APP_SCREEN.fill(BLACK)

        # TODO - clean this up...
        if self.menu_items == []:
            App.get_instance().window.show_view( ErrorModalView("No manifests found!", None) )


    def update(self):
        # simulate keypress
        if time.time() - self.last_input_time > int(os.getenv("AFK_SCROLL_TIME", 300)):
            # TODO: untested
            key_down_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN})
            pygame.event.post(key_down_event)


    def draw(self):
        # SHOW GAME ARTWORK
        image = self.menu_items[self.selected_index].image
        scaled_image = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        APP_SCREEN.blit(scaled_image, (0, 0))  # Drawing the image

        # Define the coordinates for the gradient effect.
        left = 0
        right = int(SCREEN_WIDTH * 0.5)
        top = SCREEN_HEIGHT
        bottom = 0

        # Gradient Effect
        gradient_strength = 1
        gradient_rect_width = 5
        for i in range(0, SCREEN_WIDTH // 2, gradient_rect_width):
            alpha = int(255 * gradient_strength * ((SCREEN_WIDTH // 2 - i) / (SCREEN_WIDTH // 2)))
            gradient_surface = pygame.Surface((gradient_rect_width, SCREEN_HEIGHT), pygame.SRCALPHA)
            gradient_surface.fill((0, 0, 0, alpha))
            APP_SCREEN.blit(gradient_surface, (i, 0))


        # Drawing Texts
        font_30 = pygame.font.SysFont(None, 50)
        font_45 = pygame.font.SysFont(None, 80)
        x, y = SCREEN_WIDTH * 0.02, SCREEN_HEIGHT // 2
        offset = y + self.selected_index * 55


        for i, menu_item in enumerate(self.menu_items):
            color = (173, 173, 239)  # arcade.color.BLUE_BELL
            if i == self.selected_index:
                color = (255, 255, 255)  # arcade.color.WHITE
                text = font_45.render(menu_item.game_name, True, color)
            else:
                text = font_30.render(menu_item.game_name, True, color)

            APP_SCREEN.blit(text, (x, offset - i * 55))

        # Drawing game type
        try:
            game_type = self.menu_items[self.selected_index].manifest_dict["type"]
            text = font_30.render(game_type, True, (255, 0, 0))  # arcade.color.RED
            APP_SCREEN.blit(text, (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.05))
        except KeyError:
            pass



        self.flash_free_play()
        # self.show_configuration()

        # SHOW MOUSE POSITION
        # if os.getenv("DEBUG", False):
            # self.show_mouse_position()

        pygame.display.flip()


    def handle_event(self, event):
        self.last_input_time = time.time()

        if event.type == pygame.KEYDOWN:

            # QUIT
            if event.key == pygame.K_ESCAPE:
                App.get_instance().stop()
            
            # LAUNCH APP
            elif event.key == pygame.K_RETURN:
                self.launch()

            elif event.key == pygame.K_UP:
                self.selected_index = (self.selected_index + 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index - 1) % len(self.menu_items)

            # show IP address
            elif event.key == pygame.K_a:
                self.A_held = True

            # toggle mouse coordinates
            elif event.key == pygame.K_b:
                self.show_mouse_pos = not self.show_mouse_pos

        elif event.type == pygame.KEYUP:

            if event.key == pygame.K_a:
                self.A_held = False
        
        elif event.type == pygame.MOUSEMOTION:
            x, y = event.pos            # event.pos gives the new position of the mouse
            # rel_x, rel_y = event.rel    # event.rel gives the relative motion from the last position
            self.mouse_pos = (x, y)
            # logger.debug(f"Mouse moved to ({x}, {y}) with relative motion ({rel_x}, {rel_y})")


    

    def show_mouse_position(self):
        if self.show_mouse_pos is False:
            return

        anchor_x = "left"
        offset = 20

        if self.mouse_pos[0] > SCREEN_WIDTH * 0.5:
            anchor_x = "right"

        if self.mouse_pos[1] > SCREEN_HEIGHT * 0.5:
            offset -= offset * 2

        arcade.draw_text(f"{self.mouse_pos}", self.mouse_pos[0], self.mouse_pos[1] + offset, arcade.color.WHITE, font_size=16, anchor_x=anchor_x)
        arcade.draw_text(f"{round(self.mouse_pos[0] / SCREEN_WIDTH * 100, 0)}%  {round(self.mouse_pos[1] / SCREEN_HEIGHT * 100, 0)}%", self.mouse_pos[0], self.mouse_pos[1] + offset * 2, arcade.color.GREEN, font_size=16, anchor_x=anchor_x)
        arcade.draw_point(self.mouse_pos[0], self.mouse_pos[1], arcade.color.RED, 5)


    def launch(self):
        selected_app = self.menu_items[self.selected_index].module_name
        logger.debug("Launching python module: %s", selected_app)

        # check for sufficient 'coins'
        logger.debug("Checking for sufficient coins")
        if not os.getenv("FREE_PLAY", False):
            # toast("Excuse me... YOU NEED TO PAY UP!!") #TODO
            logger.error("You don't have enough coins")
            return


        # doesn't do anything...?  Is it because I'm no in a draw loop or something????
        # arcade.set_background_color(arcade.color.BLACK)
        # arcade.start_render()
        
        # DEPRECATED:
        # if FULLSCREEN:
            # self.window.set_fullscreen(False)
        # self.window.set_visible(False) # doesn't do anything...?
        # self.window.minimize()

        args = ["python3", "-m", selected_app]
        cwd = os.path.expanduser(f"~/{APP_FOLDER}")
        logger.debug(f"subprocess.run({args=}, {cwd=})")

        # pygame.display.toggle_fullscreen()
        ret_code = subprocess.run(args, cwd=cwd).returncode # This is a blocking call - wait for game to run and exit

        # self.process = subprocess.Popen(args, cwd=cwd)
        # App.get_instance().process = subprocess.Popen(args, cwd=cwd)
        # # This is a blocking call - wait for game to run and exit
        # ret_code = self.process.wait()

        if ret_code != 0:
            logger.error(f"app '{selected_app}' returned non-zero! {ret_code=}")
            # TODO - show error modal here
            # self.window.show_view( ErrorModalView("App crashed!", self) )

        # arcade.set_background_color(arcade.color.BLACK)
        # self.window.set_visible(True) # doesn't do anything...?
        # self.window.maximize()

        # DEPRECATED:
        # if FULLSCREEN:
        #     self.window.set_fullscreen(True)
        # pygame.init()
        # pygame.display.toggle_fullscreen()

        # pygame.display.get_active
        # pygame.display.flip()

        global APP_SCREEN
        if platform.system() == 'Darwin':
            APP_SCREEN = pygame.display.set_mode(flags=pygame.NOFRAME)
        else:
            APP_SCREEN = pygame.display.set_mode(flags=pygame.FULLSCREEN | pygame.NOFRAME)



    def flash_free_play(self):
        font = pygame.font.SysFont(None, 26)
        alpha = abs((time.time() % 2) - 1)  # calculate alpha value for fade in/out effect

        if os.getenv("FREE_PLAY", False):
            text_surface = font.render("FREE PLAY", True, pygame.Color("GREEN"))
        else:
            text_surface = font.render(f"CREDITS: {self.credits}", True, pygame.Color("RED"))  # RGB tuple for RED

        text_surface.set_alpha(int(alpha * 255))
        APP_SCREEN.blit(text_surface, (10, 10))


    def show_configuration(self):
        if self.A_held is False:
            return

        ip = App.get_instance().get_ip_addr()
        arcade.draw_text(f"IP: {ip}:8080", SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.05, arcade.color.GRAPE, font_size=16, anchor_x="center")