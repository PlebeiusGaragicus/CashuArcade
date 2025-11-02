"""
Casino Slots Game - Emoji Edition
A classic slot machine game with emoji symbols
"""

import pygame
import random
import time
import sys

class SlotsGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("🎰 Casino Slots")
        
        # Game state
        self.state = "IDLE"  # IDLE, SPINNING, RESULT
        self.credits = 10  # Start with 10 credits for demo
        self.bet = 1
        
        # Slot symbols - using text that renders reliably
        self.symbols = ["CHERRY", "LEMON", "ORANGE", "GRAPE", "BELL", "DIAMOND", "SEVEN", "STAR"]
        
        # Symbol colors for visual variety
        self.symbol_colors = {
            "CHERRY": (255, 50, 50),
            "LEMON": (255, 255, 50),
            "ORANGE": (255, 165, 0),
            "GRAPE": (147, 112, 219),
            "BELL": (255, 215, 0),
            "DIAMOND": (0, 191, 255),
            "SEVEN": (255, 0, 0),
            "STAR": (255, 215, 0)
        }
        
        # Symbol display characters
        self.symbol_chars = {
            "CHERRY": "C",
            "LEMON": "L",
            "ORANGE": "O",
            "GRAPE": "G",
            "BELL": "B",
            "DIAMOND": "D",
            "SEVEN": "7",
            "STAR": "*"
        }
        
        # Reel positions (3 reels)
        self.reels = [
            [random.choice(self.symbols) for _ in range(20)],
            [random.choice(self.symbols) for _ in range(20)],
            [random.choice(self.symbols) for _ in range(20)]
        ]
        
        # Current visible positions (top of each reel)
        self.reel_positions = [0, 0, 0]
        
        # Spinning animation
        self.spin_start_time = 0
        self.spin_speeds = [0, 0, 0]  # Speed for each reel
        self.stop_times = [0, 0, 0]  # When each reel should stop
        self.reel_spinning = [False, False, False]  # Track which reels are spinning
        self.reel_slowdown_start = [0, 0, 0]  # When to start slowing down
        self.target_positions = [0, 0, 0]  # Final positions for each reel
        
        # Result
        self.last_result = []
        self.last_win = 0
        
        # Colors
        self.BG_COLOR = (20, 40, 20)
        self.REEL_BG = (40, 60, 40)
        self.REEL_BORDER = (255, 215, 0)
        self.TEXT_COLOR = (255, 255, 255)
        self.WIN_COLOR = (255, 215, 0)
        
    def spin_reels(self):
        """Start spinning the reels"""
        if self.credits < self.bet:
            return  # Not enough credits
        
        self.credits -= self.bet
        self.state = "SPINNING"
        self.spin_start_time = time.time()
        
        # Randomize reel contents and set final positions
        for i in range(3):
            self.reels[i] = [random.choice(self.symbols) for _ in range(20)]
            self.reel_spinning[i] = True
            self.spin_speeds[i] = 1.0  # Start at full speed
            
            # Stagger stop times - left to right
            # First reel stops at 1.5s, second at 2.5s, third at 3.5s
            self.reel_slowdown_start[i] = time.time() + 1.0 + (i * 1.0)
            self.stop_times[i] = self.reel_slowdown_start[i] + 0.8  # Slowdown duration
            
            # Set target position
            self.target_positions[i] = random.randint(0, len(self.reels[i]) - 1)
        
        self.last_win = 0
    
    def update_spinning(self):
        """Update reel positions during spin with gradual slowdown"""
        current_time = time.time()
        all_stopped = True
        
        for i in range(3):
            if self.reel_spinning[i]:
                if current_time < self.reel_slowdown_start[i]:
                    # Full speed spinning
                    self.reel_positions[i] = (self.reel_positions[i] + 1) % len(self.reels[i])
                    all_stopped = False
                elif current_time < self.stop_times[i]:
                    # Slowing down phase
                    slowdown_progress = (current_time - self.reel_slowdown_start[i]) / \
                                       (self.stop_times[i] - self.reel_slowdown_start[i])
                    
                    # Gradually reduce speed (quadratic easing)
                    speed_factor = (1.0 - slowdown_progress) ** 2
                    
                    # Only advance position occasionally as we slow down
                    if random.random() < speed_factor * 0.3:
                        self.reel_positions[i] = (self.reel_positions[i] + 1) % len(self.reels[i])
                    
                    all_stopped = False
                else:
                    # Reel has stopped - set to target position
                    if self.reel_spinning[i]:  # Only set once
                        self.reel_positions[i] = self.target_positions[i]
                        self.reel_spinning[i] = False
        
        if all_stopped and self.state == "SPINNING":
            self.state = "RESULT"
            self.check_win()
    
    def check_win(self):
        """Check if player won"""
        # Get the symbols at current positions
        result = [
            self.reels[0][self.reel_positions[0]],
            self.reels[1][self.reel_positions[1]],
            self.reels[2][self.reel_positions[2]]
        ]
        self.last_result = result
        
        # Check for wins
        if result[0] == result[1] == result[2]:
            # Three of a kind!
            symbol = result[0]
            
            # Different payouts for different symbols
            payouts = {
                "CHERRY": 5,
                "LEMON": 5,
                "ORANGE": 5,
                "GRAPE": 10,
                "BELL": 15,
                "STAR": 20,
                "DIAMOND": 50,
                "SEVEN": 100
            }
            
            self.last_win = payouts.get(symbol, 5) * self.bet
            self.credits += self.last_win
        elif result[0] == result[1] or result[1] == result[2]:
            # Two of a kind - small win
            self.last_win = 2 * self.bet
            self.credits += self.last_win
    
    def adjust_bet(self, amount):
        """Adjust bet amount"""
        new_bet = self.bet + amount
        if 1 <= new_bet <= min(10, self.credits):
            self.bet = new_bet
    
    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.state == "IDLE":
                        self.spin_reels()
                    elif event.key == pygame.K_RETURN and self.state == "RESULT":
                        self.state = "IDLE"
                    elif event.key == pygame.K_UP:
                        self.adjust_bet(1)
                    elif event.key == pygame.K_DOWN:
                        self.adjust_bet(-1)
                    elif event.key == pygame.K_ESCAPE:
                        running = False
            
            # Update game state
            if self.state == "SPINNING":
                self.update_spinning()
            
            # Render
            self.render()
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()
    
    def render(self):
        """Render the game"""
        self.screen.fill(self.BG_COLOR)
        
        # Title
        title_font = pygame.font.Font(None, 72)
        title = title_font.render("🎰 CASINO SLOTS 🎰", True, self.WIN_COLOR)
        title_rect = title.get_rect(center=(400, 60))
        self.screen.blit(title, title_rect)
        
        # Draw reels
        self.draw_reels()
        
        # Credits and bet info
        info_font = pygame.font.Font(None, 40)
        credits_text = info_font.render(f"Credits: {self.credits}", True, self.TEXT_COLOR)
        bet_text = info_font.render(f"Bet: {self.bet}", True, self.TEXT_COLOR)
        
        self.screen.blit(credits_text, (50, 500))
        self.screen.blit(bet_text, (50, 540))
        
        # Instructions
        inst_font = pygame.font.Font(None, 28)
        if self.state == "IDLE":
            instructions = [
                "SPACE - Spin",
                "↑/↓ - Adjust Bet",
                "ESC - Quit"
            ]
            y_pos = 500
            for inst in instructions:
                text = inst_font.render(inst, True, (200, 200, 200))
                self.screen.blit(text, (550, y_pos))
                y_pos += 30
        elif self.state == "SPINNING":
            spinning_text = info_font.render("SPINNING...", True, self.WIN_COLOR)
            self.screen.blit(spinning_text, (550, 520))
        elif self.state == "RESULT":
            if self.last_win > 0:
                win_text = info_font.render(f"WIN: {self.last_win}!", True, self.WIN_COLOR)
                self.screen.blit(win_text, (550, 500))
            else:
                lose_text = info_font.render("No Win", True, (200, 100, 100))
                self.screen.blit(lose_text, (550, 500))
            
            continue_text = inst_font.render("ENTER - Continue", True, (200, 200, 200))
            self.screen.blit(continue_text, (550, 545))
        
        # Paytable
        self.draw_paytable()
    
    def draw_reels(self):
        """Draw the three reels with symbols"""
        reel_width = 150
        reel_height = 200
        spacing = 20
        start_x = 150
        start_y = 150
        
        char_font = pygame.font.Font(None, 140)
        name_font = pygame.font.Font(None, 28)
        
        for i in range(3):
            # Reel background
            reel_x = start_x + i * (reel_width + spacing)
            
            # Highlight spinning reels with brighter background
            if self.state == "SPINNING" and self.reel_spinning[i]:
                bg_color = (60, 80, 60)
            else:
                bg_color = self.REEL_BG
            
            pygame.draw.rect(self.screen, bg_color, 
                           (reel_x, start_y, reel_width, reel_height))
            
            # Border color changes when reel stops
            if self.state == "SPINNING" and not self.reel_spinning[i]:
                border_color = (100, 255, 100)  # Green when stopped
            else:
                border_color = self.REEL_BORDER
            
            pygame.draw.rect(self.screen, border_color, 
                           (reel_x, start_y, reel_width, reel_height), 3)
            
            # Draw symbol
            pos = self.reel_positions[i]
            symbol = self.reels[i][pos]
            symbol_char = self.symbol_chars[symbol]
            symbol_color = self.symbol_colors[symbol]
            
            # Draw large character
            char_surface = char_font.render(symbol_char, True, symbol_color)
            char_rect = char_surface.get_rect(center=(reel_x + reel_width // 2, 
                                                       start_y + reel_height // 2 - 20))
            self.screen.blit(char_surface, char_rect)
            
            # Draw symbol name below
            name_surface = name_font.render(symbol, True, (200, 200, 200))
            name_rect = name_surface.get_rect(center=(reel_x + reel_width // 2,
                                                      start_y + reel_height - 30))
            self.screen.blit(name_surface, name_rect)
    
    def draw_paytable(self):
        """Draw paytable on the side"""
        font = pygame.font.Font(None, 22)
        title = font.render("PAYTABLE:", True, self.WIN_COLOR)
        self.screen.blit(title, (50, 120))
        
        payouts = [
            ("7-7-7", "100x", (255, 0, 0)),
            ("D-D-D", "50x", (0, 191, 255)),
            ("*-*-*", "20x", (255, 215, 0)),
            ("B-B-B", "15x", (255, 215, 0)),
            ("G-G-G", "10x", (147, 112, 219)),
            ("C/L/O", "5x", (255, 165, 0)),
            ("Any 2", "2x", (200, 200, 200)),
        ]
        
        y_pos = 150
        for combo, payout, color in payouts:
            text = font.render(f"{combo} = {payout}", True, color)
            self.screen.blit(text, (50, y_pos))
            y_pos += 28


def main():
    game = SlotsGame()
    game.run()


if __name__ == "__main__":
    main()
