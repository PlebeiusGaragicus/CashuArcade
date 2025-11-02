"""
Casino Slots Game - Emoji Edition
A classic slot machine game with emoji symbols
"""

import pygame
import random
import time
import sys
import math

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
        
        # Vertical scrolling animation
        self.reel_offsets = [0.0, 0.0, 0.0]  # Pixel offset for smooth scrolling
        self.reel_speeds = [0.0, 0.0, 0.0]  # Current speed in pixels per frame
        self.symbol_height = 80  # Height of each symbol in pixels
        
        # Spinning animation
        self.spin_start_time = 0
        self.stop_times = [0, 0, 0]  # When each reel should stop
        self.reel_spinning = [False, False, False]  # Track which reels are spinning
        self.reel_slowdown_start = [0, 0, 0]  # When to start slowing down
        self.slowdown_start_offset = [0.0, 0.0, 0.0]  # Offset at start of slowdown
        self.slowdown_distance = [0.0, 0.0, 0.0]  # Total distance to travel during slowdown
        self.decel_a = [0.0, 0.0, 0.0]
        self.decel_traveled = [0.0, 0.0, 0.0]
        self.decel_steps_total = [0, 0, 0]
        self.decel_steps_done = [0, 0, 0]
        self.slowdown_duration = [0.0, 0.0, 0.0]
        self.reel_phase = ["IDLE", "IDLE", "IDLE"]
        self.max_spin_speed = 36.0
        
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
            self.reel_speeds[i] = self.max_spin_speed
            self.reel_offsets[i] = 0.0
            self.slowdown_start_offset[i] = 0.0
            self.slowdown_distance[i] = 0.0
            
            # Stagger stop times - left to right
            # First reel stops at 1.5s, second at 2.5s, third at 3.5s
            self.reel_slowdown_start[i] = 0.0
            self.stop_times[i] = 0.0
            self.slowdown_duration[i] = 0.0
            self.decel_a[i] = 0.0
            self.decel_traveled[i] = 0.0
            self.decel_steps_total[i] = 0
            self.decel_steps_done[i] = 0
            self.reel_phase[i] = "SPIN"
        
        self.last_win = 0
    
    def update_spinning(self):
        """Update reel positions during spin with gradual slowdown"""
        current_time = time.time()
        all_stopped = True
        for i in range(3):
            if self.reel_phase[i] != "STOP":
                all_stopped = False
            if not self.reel_spinning[i]:
                continue
            if self.reel_phase[i] == "SPIN":
                self.reel_speeds[i] = self.max_spin_speed
                self.reel_offsets[i] += self.reel_speeds[i]
                while self.reel_offsets[i] >= self.symbol_height:
                    self.reel_offsets[i] -= self.symbol_height
                    self.reel_positions[i] = (self.reel_positions[i] + 1) % len(self.reels[i])
                can_start_slowdown = False
                if i == 0:
                    if current_time - self.spin_start_time >= 0.9:
                        can_start_slowdown = True
                else:
                    if self.reel_phase[i - 1] == "STOP":
                        can_start_slowdown = True
                if can_start_slowdown:
                    self.reel_phase[i] = "DECEL"
                    self.reel_slowdown_start[i] = current_time
                    self.slowdown_start_offset[i] = self.reel_offsets[i]
                    align_remainder = (self.symbol_height - self.reel_offsets[i]) % self.symbol_height
                    self.decel_traveled[i] = 0.0
                    v0 = max(self.reel_speeds[i], 0.0)
                    # Search for a suitable (N, k) so v_end in [0, v0] and S aligns to grid,
                    # with v_end small to avoid any visual snap.
                    found = False
                    chosen_N = None
                    chosen_k = None
                    for N in range(100, 151):
                        k_min = math.ceil((N * v0 / 2.0 - align_remainder) / float(self.symbol_height))
                        k_max = math.floor((N * v0 - align_remainder) / float(self.symbol_height))
                        lo = max(12, int(k_min))
                        hi = min(40, int(k_max))
                        if lo <= hi:
                            # Target a tiny end speed
                            v_end_target = 0.8
                            desired_D = (N * (v0 + v_end_target)) / 2.0
                            k_desired = int(round((desired_D - align_remainder) / float(self.symbol_height)))
                            k = max(lo, min(hi, k_desired))
                            chosen_N = N
                            chosen_k = k
                            found = True
                            break
                    if not found:
                        chosen_N = 130
                        # compute a k at mid of allowed range to keep v_end reasonable
                        k_min = math.ceil((chosen_N * v0 / 2.0 - align_remainder) / float(self.symbol_height))
                        k_max = math.floor((chosen_N * v0 - align_remainder) / float(self.symbol_height))
                        lo = max(12, int(k_min))
                        hi = min(40, int(k_max))
                        if lo <= hi:
                            chosen_k = (lo + hi) // 2
                        else:
                            chosen_k = 30
                    N = chosen_N
                    k = chosen_k
                    D_target = align_remainder + k * self.symbol_height
                    # Solve exact v_end from S = N*(v0 + v_end)/2 = D_target
                    v_end = (2.0 * D_target) / float(N) - v0
                    # Compute per-step acceleration to reach v_end in N steps (N velocities)
                    self.decel_a[i] = (v_end - v0) / float(max(1, N - 1))
                    self.slowdown_distance[i] = D_target
                    self.decel_steps_total[i] = N
                    self.decel_steps_done[i] = 0
            elif self.reel_phase[i] == "DECEL":
                v = self.reel_speeds[i]
                # Use exact residual on the last frame to avoid any float-induced snap
                if self.decel_steps_done[i] + 1 >= self.decel_steps_total[i]:
                    step = max(self.slowdown_distance[i] - self.decel_traveled[i], 0.0)
                else:
                    step = max(v, 0.0)
                new_offset = self.reel_offsets[i] + step
                while new_offset >= self.symbol_height:
                    new_offset -= self.symbol_height
                    self.reel_positions[i] = (self.reel_positions[i] + 1) % len(self.reels[i])
                self.reel_offsets[i] = new_offset
                self.decel_traveled[i] += step
                self.decel_steps_done[i] += 1
                if self.decel_steps_done[i] >= self.decel_steps_total[i]:
                    self.reel_speeds[i] = 0.0
                    self.reel_offsets[i] = 0.0
                    self.reel_spinning[i] = False
                    self.reel_phase[i] = "STOP"
                else:
                    self.reel_speeds[i] = max(v + self.decel_a[i], 0.0)
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
        """Draw the three reels with vertical scrolling symbols"""
        reel_width = 150
        reel_height = 240  # Taller to show 3 symbols
        spacing = 20
        start_x = 150
        start_y = 130
        
        char_font = pygame.font.Font(None, 100)
        name_font = pygame.font.Font(None, 22)
        
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
            
            # Create a clipping region for the reel
            clip_rect = pygame.Rect(reel_x, start_y, reel_width, reel_height)
            self.screen.set_clip(clip_rect)
            
            # Draw multiple symbols vertically with scrolling offset
            pos = self.reel_positions[i]
            offset = self.reel_offsets[i]
            
            # Draw 4 symbols to ensure smooth scrolling (one above, center, and two below)
            for j in range(-1, 4):
                symbol_index = (pos + j) % len(self.reels[i])
                symbol = self.reels[i][symbol_index]
                symbol_char = self.symbol_chars[symbol]
                symbol_color = self.symbol_colors[symbol]
                
                # Calculate Y position with scrolling offset
                symbol_y = start_y + (j * self.symbol_height) - offset + self.symbol_height // 2
                
                # Draw large character
                char_surface = char_font.render(symbol_char, True, symbol_color)
                char_rect = char_surface.get_rect(center=(reel_x + reel_width // 2, symbol_y - 10))
                self.screen.blit(char_surface, char_rect)
                
                # Draw symbol name below
                name_surface = name_font.render(symbol, True, (200, 200, 200))
                name_rect = name_surface.get_rect(center=(reel_x + reel_width // 2, symbol_y + 25))
                self.screen.blit(name_surface, name_rect)
            
            # Remove clipping
            self.screen.set_clip(None)
            
            # Draw center line to show winning position
            center_y = start_y + reel_height // 2
            pygame.draw.line(self.screen, (255, 255, 100), 
                           (reel_x, center_y), (reel_x + reel_width, center_y), 2)
            
            # Border color changes when reel stops
            if self.state == "SPINNING" and not self.reel_spinning[i]:
                border_color = (100, 255, 100)  # Green when stopped
            else:
                border_color = self.REEL_BORDER
            
            pygame.draw.rect(self.screen, border_color, 
                           (reel_x, start_y, reel_width, reel_height), 3)
    
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
