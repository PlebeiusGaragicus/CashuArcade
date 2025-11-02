import os
import platform
import time
import logging
logger = logging.getLogger()

from dataclasses import dataclass
import subprocess


import pygame

from lnarcade.app import App, APP_SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT
from lnarcade.config import APP_FOLDER, MY_DIR, MISSING_SCREENSHOT
from lnarcade.colors import *
from lnarcade.utilities.find_games import load_game_manifests
from lnarcade.utilities.manifest import GameManifest
from lnarcade.view import ViewState
from lnarcade.view.error import ErrorModalView



@dataclass
class GameListItem:
    game_dir_name: str  # Directory name of the game
    manifest: GameManifest  # Full manifest object
    image: pygame.Surface = None

    def __post_init__(self):
        """Load the game screenshot image."""
        screenshot_path = self.manifest.get_screenshot_path()
        
        try:
            if os.path.exists(screenshot_path):
                self.image = pygame.image.load(screenshot_path)
            else:
                logger.warning(f"Screenshot not found: {screenshot_path}, using default")
                self.image = pygame.image.load(MISSING_SCREENSHOT)
        except pygame.error as e:
            logger.error(f"Error loading screenshot {screenshot_path}: {e}")
            self.image = pygame.image.load(MISSING_SCREENSHOT)
    
    @property
    def game_name(self) -> str:
        """Get the display name of the game."""
        return self.manifest.launcher.name
    
    @property
    def game_type(self) -> str:
        """Get the type of the game."""
        return self.manifest.launcher.type
    
    @property
    def description(self) -> str:
        """Get the game description."""
        return self.manifest.launcher.description




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

        # Load game manifests using new system
        manifests = load_game_manifests()
        logger.info(f"Loaded {len(manifests)} game manifests")

        for game_dir_name, manifest in manifests.items():
            try:
                game_item = GameListItem(game_dir_name, manifest)
                self.menu_items.append(game_item)
                logger.debug(f"Added game: {game_item.game_name}")
            except Exception as e:
                logger.error(f"Error creating GameListItem for {game_dir_name}: {e}")
                continue

        if not self.menu_items:
            logger.warning("No games found!")


    def setup(self):
        APP_SCREEN.fill(BLACK)
        
        if not self.menu_items:
            logger.warning("No games found! Add games to ~/CashuArcade/")
            # TODO: Implement error modal view for pygame


    def update(self):
        # simulate keypress
        if time.time() - self.last_input_time > int(os.getenv("AFK_SCROLL_TIME", 300)):
            # TODO: untested
            key_down_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN})
            pygame.event.post(key_down_event)


    def draw(self):
        # Handle no games case
        if not self.menu_items:
            APP_SCREEN.fill(BLACK)
            font = pygame.font.SysFont(None, 60)
            text = font.render("No games found!", True, RED)
            text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
            APP_SCREEN.blit(text, text_rect)
            
            font_small = pygame.font.SysFont(None, 40)
            text2 = font_small.render("Add games to ~/CashuArcade/", True, WHITE)
            text2_rect = text2.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 20))
            APP_SCREEN.blit(text2, text2_rect)
            
            pygame.display.flip()
            return
        
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
        game_type = self.menu_items[self.selected_index].game_type
        if game_type:
            text = font_30.render(game_type, True, (255, 0, 0))  # RED
            APP_SCREEN.blit(text, (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.05))



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
                if self.menu_items:
                    self.launch()

            elif event.key == pygame.K_UP:
                if self.menu_items:
                    self.selected_index = (self.selected_index + 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                if self.menu_items:
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
        """Debug function to show mouse position (deprecated arcade code removed)."""
        if self.show_mouse_pos is False:
            return
        
        # TODO: Reimplement with pygame if needed
        font = pygame.font.SysFont(None, 20)
        text = font.render(f"{self.mouse_pos}", True, (255, 255, 255))
        APP_SCREEN.blit(text, (self.mouse_pos[0] + 10, self.mouse_pos[1] + 10))


    def launch(self):
        """Launch the selected game with proper venv support."""
        selected_item = self.menu_items[self.selected_index]
        manifest = selected_item.manifest
        game_name = selected_item.game_name
        
        logger.info(f"Launching game: {game_name}")

        # Check for sufficient 'coins'
        if not os.getenv("FREE_PLAY", "True").lower() == "true":
            logger.error("FREE_PLAY is disabled and no coin system implemented")
            # TODO: Implement coin/credit system
            return

        # Build launch command
        launch_config = manifest.launcher.launch
        cwd = manifest.get_launch_cwd()
        
        # Check if we need to use a venv
        venv_python = manifest.get_venv_python()
        if venv_python:
            command = venv_python
            logger.debug(f"Using venv Python: {venv_python}")
        else:
            command = launch_config.command
            logger.debug(f"Using system Python: {command}")
        
        # Build full command with args
        args = [command] + launch_config.args
        
        logger.info(f"Launching: {' '.join(args)}")
        logger.debug(f"Working directory: {cwd}")

        try:
            # Launch the game (blocking call)
            result = subprocess.run(
                args,
                cwd=cwd,
                capture_output=False,  # Let game output go to console
                text=True
            )
            
            ret_code = result.returncode
            
            if ret_code != 0:
                logger.error(f"Game '{game_name}' exited with code {ret_code}")
                # TODO: Show error modal
            else:
                logger.info(f"Game '{game_name}' exited normally")
        
        except FileNotFoundError as e:
            logger.error(f"Failed to launch game: {e}")
            logger.error(f"Command not found: {command}")
            # TODO: Show error modal
        
        except Exception as e:
            logger.error(f"Error launching game: {e}")
            # TODO: Show error modal
        
        # Restore display after game exits
        logger.debug("Restoring display after game exit")
        global APP_SCREEN
        if platform.system() == 'Darwin':
            APP_SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.NOFRAME)
        else:
            APP_SCREEN = pygame.display.set_mode(flags=pygame.FULLSCREEN | pygame.NOFRAME)
        
        pygame.display.set_caption("Lightning Arcade")



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
        """Show configuration info (deprecated arcade code removed)."""
        if self.A_held is False:
            return
        
        # TODO: Reimplement with pygame if needed
        # For now, just log that the feature is disabled
        pass