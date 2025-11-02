# arcade_game.py - Reflex Timer Game

import pygame
import asyncio
import qrcode
import random
import time
from io import BytesIO
from arcade_payments import (
    create_payment_request,
    check_payment_received,
    use_credit,
    payout_winnings_as_token,
    end_session
)

class ReflexGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("⚡ Lightning Reflex Game")
        self.state = "INSERT_COINS"  # INSERT_COINS, WAITING_PAYMENT, PLAYING, COUNTDOWN, GAME_OVER
        self.credits = 0
        self.invoice_qr = None
        
        # Game state
        self.round = 0
        self.max_rounds = 5
        self.reaction_times = []
        self.target_visible = False
        self.target_start_time = 0
        self.countdown_start = 0
        self.best_time = None
        
    async def show_payment_screen(self, num_credits=5):
        """Display QR code for payment"""
        self.state = "WAITING_PAYMENT"
        
        # Generate invoice
        payment_data = await create_payment_request(num_credits)
        
        # Create QR code (smaller size)
        qr = qrcode.QRCode(version=1, box_size=5, border=2)
        qr.add_data(payment_data['invoice'])
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to pygame surface
        qr_bytes = BytesIO()
        qr_img.save(qr_bytes, format='PNG')
        qr_bytes.seek(0)
        self.invoice_qr = pygame.image.load(qr_bytes)
        
        # Scale to reasonable size (250x250)
        self.invoice_qr = pygame.transform.scale(self.invoice_qr, (250, 250))
        
        # Store payment data for display
        self.payment_data = payment_data
    
    async def check_payment_loop(self):
        """Poll for payment in background"""
        while self.state == "WAITING_PAYMENT":
            paid, credits = await check_payment_received()
            if paid:
                self.credits = credits
                self.state = "PLAYING"
                break
            await asyncio.sleep(2)  # Check every 2 seconds
    
    async def start_game(self):
        """Start a reflex game (deduct credit)"""
        if self.credits < 1:
            self.state = "INSERT_COINS"
            return
        
        try:
            self.credits = use_credit()
            self.round = 0
            self.reaction_times = []
            self.state = "COUNTDOWN"
            self.countdown_start = time.time()
        except ValueError:
            self.state = "INSERT_COINS"
    
    def start_round(self):
        """Start a new round - wait random time then show target"""
        self.target_visible = False
        # Random delay between 1-3 seconds
        delay = random.uniform(1.0, 3.0)
        self.target_start_time = time.time() + delay
    
    def handle_click(self):
        """Handle player click"""
        if self.state == "PLAYING" and self.target_visible:
            # Calculate reaction time
            reaction_time = (time.time() - self.target_start_time) * 1000  # in ms
            self.reaction_times.append(reaction_time)
            self.round += 1
            
            if self.round >= self.max_rounds:
                self.state = "GAME_OVER"
                avg_time = sum(self.reaction_times) / len(self.reaction_times)
                self.best_time = min(self.reaction_times)
            else:
                self.start_round()
    
    async def handle_win(self, win_amount_sats=500):
        """Player won! Show payout QR"""
        # Generate Cashu token for winnings
        token = await payout_winnings_as_token(win_amount_sats)
        
        # Create QR code (smaller size)
        qr = qrcode.QRCode(version=1, box_size=5, border=2)
        qr.add_data(token)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        qr_bytes = BytesIO()
        qr_img.save(qr_bytes, format='PNG')
        qr_bytes.seek(0)
        qr_surface = pygame.image.load(qr_bytes)
        qr_surface = pygame.transform.scale(qr_surface, (250, 250))
        
        self.win_qr = qr_surface
        self.win_amount = win_amount_sats
    
    async def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.state == "INSERT_COINS":
                            # Player wants to insert coins
                            await self.show_payment_screen(num_credits=5)
                            asyncio.create_task(self.check_payment_loop())
                        elif self.state == "PLAYING":
                            # Player clicked for reflex test
                            self.handle_click()
                        elif self.state == "GAME_OVER":
                            # Return to playing or insert coins
                            if self.credits > 0:
                                await self.start_game()
                            else:
                                self.state = "INSERT_COINS"
                    elif event.key == pygame.K_RETURN and self.state == "PLAYING" and self.round == 0:
                        # Start first round
                        self.start_round()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == "PLAYING":
                        self.handle_click()
            
            # Update game state
            if self.state == "COUNTDOWN":
                # Show 3-2-1 countdown
                elapsed = time.time() - self.countdown_start
                if elapsed >= 3:
                    self.state = "PLAYING"
                    self.start_round()
            elif self.state == "PLAYING" and not self.target_visible:
                # Check if it's time to show target
                if time.time() >= self.target_start_time:
                    self.target_visible = True
                    self.target_start_time = time.time()  # Reset to actual show time
            
            # Render based on state
            if self.state == "WAITING_PAYMENT":
                self.render_payment_screen()
            elif self.state == "COUNTDOWN":
                self.render_countdown()
            elif self.state == "PLAYING":
                self.render_game()
            elif self.state == "GAME_OVER":
                self.render_game_over()
            elif self.state == "INSERT_COINS":
                self.render_insert_coins_screen()
            
            pygame.display.flip()
            clock.tick(60)
        
        end_session()
        pygame.quit()
    
    def render_payment_screen(self):
        """Display QR code for payment"""
        self.screen.fill((20, 20, 40))
        
        # Title
        font = pygame.font.Font(None, 48)
        title = font.render("⚡ Lightning Payment", True, (255, 215, 0))
        self.screen.blit(title, (220, 50))
        
        # QR Code
        if self.invoice_qr:
            qr_x = (800 - 250) // 2
            self.screen.blit(self.invoice_qr, (qr_x, 150))
        
        # Payment info
        small_font = pygame.font.Font(None, 32)
        amount_text = small_font.render(f"Amount: {self.payment_data['amount_sats']} sats", True, (255, 255, 255))
        credits_text = small_font.render(f"Credits: {self.payment_data['num_credits']}", True, (255, 255, 255))
        
        self.screen.blit(amount_text, (280, 420))
        self.screen.blit(credits_text, (310, 460))
        
        # Instructions
        tiny_font = pygame.font.Font(None, 24)
        instruction = tiny_font.render("Scan with Lightning wallet to pay", True, (180, 180, 180))
        waiting = tiny_font.render("Waiting for payment...", True, (100, 200, 100))
        
        self.screen.blit(instruction, (250, 520))
        self.screen.blit(waiting, (280, 550))
    
    def render_countdown(self):
        """Show countdown before game starts"""
        self.screen.fill((20, 20, 40))
        
        elapsed = time.time() - self.countdown_start
        remaining = 3 - int(elapsed)
        
        if remaining > 0:
            font = pygame.font.Font(None, 200)
            text = font.render(str(remaining), True, (255, 215, 0))
            text_rect = text.get_rect(center=(400, 300))
            self.screen.blit(text, text_rect)
        else:
            font = pygame.font.Font(None, 100)
            text = font.render("GO!", True, (0, 255, 0))
            text_rect = text.get_rect(center=(400, 300))
            self.screen.blit(text, text_rect)
    
    def render_game(self):
        """Render the reflex game"""
        # Background color changes when target is visible
        if self.target_visible:
            self.screen.fill((255, 50, 50))  # Red - CLICK NOW!
        else:
            self.screen.fill((20, 20, 40))  # Dark blue - wait
        
        # Credits display
        font = pygame.font.Font(None, 32)
        credits_text = font.render(f"Credits: {self.credits}", True, (255, 255, 255))
        self.screen.blit(credits_text, (10, 10))
        
        # Round counter
        round_text = font.render(f"Round: {self.round + 1}/{self.max_rounds}", True, (255, 255, 255))
        self.screen.blit(round_text, (650, 10))
        
        # Instructions
        if self.target_visible:
            big_font = pygame.font.Font(None, 120)
            text = big_font.render("CLICK!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(400, 300))
            self.screen.blit(text, text_rect)
        else:
            medium_font = pygame.font.Font(None, 60)
            text = medium_font.render("Wait for RED...", True, (150, 150, 150))
            text_rect = text.get_rect(center=(400, 300))
            self.screen.blit(text, text_rect)
        
        # Show previous reaction times
        if self.reaction_times:
            small_font = pygame.font.Font(None, 28)
            y_pos = 450
            for i, rt in enumerate(self.reaction_times[-3:], 1):  # Show last 3
                rt_text = small_font.render(f"Round {len(self.reaction_times) - 3 + i}: {rt:.0f}ms", True, (200, 200, 200))
                self.screen.blit(rt_text, (300, y_pos))
                y_pos += 35
    
    def render_game_over(self):
        """Show game over screen with results"""
        self.screen.fill((20, 20, 40))
        
        # Title
        big_font = pygame.font.Font(None, 72)
        title = big_font.render("GAME OVER", True, (255, 215, 0))
        title_rect = title.get_rect(center=(400, 80))
        self.screen.blit(title, title_rect)
        
        # Stats
        font = pygame.font.Font(None, 40)
        avg_time = sum(self.reaction_times) / len(self.reaction_times)
        
        stats = [
            f"Average: {avg_time:.0f}ms",
            f"Best: {self.best_time:.0f}ms",
            f"Worst: {max(self.reaction_times):.0f}ms"
        ]
        
        y_pos = 200
        for stat in stats:
            text = font.render(stat, True, (255, 255, 255))
            text_rect = text.get_rect(center=(400, y_pos))
            self.screen.blit(text, text_rect)
            y_pos += 60
        
        # All times
        small_font = pygame.font.Font(None, 28)
        times_title = small_font.render("All Rounds:", True, (180, 180, 180))
        self.screen.blit(times_title, (300, 400))
        
        y_pos = 430
        for i, rt in enumerate(self.reaction_times, 1):
            rt_text = small_font.render(f"Round {i}: {rt:.0f}ms", True, (200, 200, 200))
            self.screen.blit(rt_text, (320, y_pos))
            y_pos += 30
        
        # Instructions
        tiny_font = pygame.font.Font(None, 24)
        if self.credits > 0:
            instruction = tiny_font.render("Press SPACE to play again", True, (100, 255, 100))
        else:
            instruction = tiny_font.render("Press SPACE to insert coins", True, (255, 100, 100))
        
        instruction_rect = instruction.get_rect(center=(400, 570))
        self.screen.blit(instruction, instruction_rect)
    
    def render_insert_coins_screen(self):
        """Show insert coins screen"""
        self.screen.fill((20, 20, 40))
        
        # Title
        big_font = pygame.font.Font(None, 100)
        title = big_font.render("⚡ REFLEX GAME", True, (255, 215, 0))
        title_rect = title.get_rect(center=(400, 150))
        self.screen.blit(title, title_rect)
        
        # Subtitle
        font = pygame.font.Font(None, 48)
        subtitle = font.render("Test Your Lightning Reflexes!", True, (255, 255, 255))
        subtitle_rect = subtitle.get_rect(center=(400, 250))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Instructions
        medium_font = pygame.font.Font(None, 36)
        instructions = [
            "Click as fast as you can when the screen turns RED",
            "5 rounds per game",
            "Beat your best time!"
        ]
        
        y_pos = 330
        for instruction in instructions:
            text = medium_font.render(instruction, True, (200, 200, 200))
            text_rect = text.get_rect(center=(400, y_pos))
            self.screen.blit(text, text_rect)
            y_pos += 45
        
        # Payment prompt
        prompt_font = pygame.font.Font(None, 42)
        prompt = prompt_font.render("Press SPACE to pay with Lightning", True, (100, 255, 100))
        prompt_rect = prompt.get_rect(center=(400, 500))
        self.screen.blit(prompt, prompt_rect)
        
        # Price
        small_font = pygame.font.Font(None, 32)
        price = small_font.render("500 sats = 5 credits", True, (180, 180, 180))
        price_rect = price.get_rect(center=(400, 550))
        self.screen.blit(price, price_rect)

# Run the game
if __name__ == "__main__":
    game = ReflexGame()
    asyncio.run(game.run())