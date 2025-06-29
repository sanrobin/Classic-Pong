import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Game constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
BALL_SIZE = 15
PADDLE_SPEED = 7
BALL_SPEED_X = 6
BALL_SPEED_Y = 4

# Colors (retro black and white theme)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Difficulty settings
DIFFICULTY_SETTINGS = {
    'easy': {
        'ai_speed': 0.5,
        'ai_reaction': 0.6,
        'ball_speed_multiplier': 0.8,
        'color': GREEN
    },
    'medium': {
        'ai_speed': 0.8,
        'ai_reaction': 0.8,
        'ball_speed_multiplier': 1.0,
        'color': YELLOW
    },
    'hard': {
        'ai_speed': 1.2,
        'ai_reaction': 0.95,
        'ball_speed_multiplier': 1.3,
        'color': RED
    }
}

class Paddle:
    """Represents a paddle in the Pong game"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = PADDLE_SPEED
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def move_up(self):
        """Move paddle up, ensuring it stays within screen bounds"""
        if self.y > 0:
            self.y -= self.speed
            self.rect.y = self.y
    
    def move_down(self):
        """Move paddle down, ensuring it stays within screen bounds"""
        if self.y < WINDOW_HEIGHT - self.height:
            self.y += self.speed
            self.rect.y = self.y
    
    def draw(self, screen):
        """Draw the paddle on the screen"""
        pygame.draw.rect(screen, WHITE, self.rect)

class Ball:
    """Represents the ball in the Pong game"""
    
    def __init__(self, x, y, sound_manager, difficulty='medium'):
        self.x = x
        self.y = y
        self.size = BALL_SIZE
        self.base_speed_x = BALL_SPEED_X
        self.base_speed_y = BALL_SPEED_Y
        self.sound_manager = sound_manager
        self.set_difficulty(difficulty)
        self.rect = pygame.Rect(x, y, self.size, self.size)
        
        # Randomize initial direction
        if random.choice([True, False]):
            self.speed_x *= -1
        if random.choice([True, False]):
            self.speed_y *= -1
    
    def set_difficulty(self, difficulty):
        """Set ball speed based on difficulty"""
        multiplier = DIFFICULTY_SETTINGS[difficulty]['ball_speed_multiplier']
        self.speed_x = int(self.base_speed_x * multiplier)
        self.speed_y = int(self.base_speed_y * multiplier)
    
    def move(self):
        """Move the ball and handle wall collisions"""
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Bounce off top and bottom walls
        if self.y <= 0 or self.y >= WINDOW_HEIGHT - self.size:
            self.speed_y *= -1
            self.sound_manager.play_sound('wall_hit')
    
    def reset(self, difficulty='medium'):
        """Reset ball to center with random direction"""
        self.x = WINDOW_WIDTH // 2 - self.size // 2
        self.y = WINDOW_HEIGHT // 2 - self.size // 2
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Reset speed based on difficulty
        self.set_difficulty(difficulty)
        
        # Randomize direction
        self.speed_x = self.speed_x if random.choice([True, False]) else -self.speed_x
        self.speed_y = self.speed_y if random.choice([True, False]) else -self.speed_y
    
    def draw(self, screen):
        """Draw the ball on the screen"""
        pygame.draw.rect(screen, WHITE, self.rect)

class SoundManager:
    """Handles all game sound effects"""
    
    def __init__(self):
        self.sounds = {}
        self.load_sounds()
    
    def load_sounds(self):
        """Load or create sound effects"""
        try:
            # Try to load sound files if they exist
            if os.path.exists('paddle_hit.wav'):
                self.sounds['paddle_hit'] = pygame.mixer.Sound('paddle_hit.wav')
            else:
                # Create a simple beep sound programmatically
                self.sounds['paddle_hit'] = self.create_beep_sound(440, 0.1)
            
            if os.path.exists('wall_hit.wav'):
                self.sounds['wall_hit'] = pygame.mixer.Sound('wall_hit.wav')
            else:
                # Create a different beep for wall hits
                self.sounds['wall_hit'] = self.create_beep_sound(220, 0.1)
            
            if os.path.exists('score.wav'):
                self.sounds['score'] = pygame.mixer.Sound('score.wav')
            else:
                # Create a score sound
                self.sounds['score'] = self.create_beep_sound(880, 0.3)
                
        except pygame.error:
            print("Warning: Could not load sound effects")
            # Create silent sounds as fallback
            for sound_name in ['paddle_hit', 'wall_hit', 'score']:
                self.sounds[sound_name] = self.create_silent_sound()
    
    def create_beep_sound(self, frequency, duration):
        """Create a simple beep sound programmatically"""
        try:
            sample_rate = 22050
            frames = int(duration * sample_rate)
            arr = []
            for i in range(frames):
                wave = 4096 * pygame.math.sin(frequency * 2 * pygame.math.pi * i / sample_rate)
                arr.append([int(wave), int(wave)])
            sound = pygame.sndarray.make_sound(pygame.array.array('i', arr))
            return sound
        except:
            return self.create_silent_sound()
    
    def create_silent_sound(self):
        """Create a silent sound as fallback"""
        try:
            arr = [[0, 0] for _ in range(100)]
            return pygame.sndarray.make_sound(pygame.array.array('i', arr))
        except:
            return None
    
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if sound_name in self.sounds and self.sounds[sound_name]:
            try:
                self.sounds[sound_name].play()
            except:
                pass  # Silently fail if sound can't play

class AIPlayer:
    """AI controller for the computer paddle with difficulty levels"""
    
    def __init__(self, paddle, ball, difficulty='medium'):
        self.paddle = paddle
        self.ball = ball
        self.set_difficulty(difficulty)
    
    def set_difficulty(self, difficulty):
        """Set AI difficulty level"""
        self.difficulty_name = difficulty
        settings = DIFFICULTY_SETTINGS[difficulty]
        self.speed_multiplier = settings['ai_speed']
        self.reaction_chance = settings['ai_reaction']
        self.paddle.speed = int(PADDLE_SPEED * self.speed_multiplier)
    
    def update(self):
        """Update AI paddle position based on ball position and difficulty"""
        paddle_center = self.paddle.y + self.paddle.height // 2
        ball_center = self.ball.y + self.ball.size // 2
        
        # Only move if ball is coming toward AI paddle
        if self.ball.speed_x > 0:
            # Add difficulty-based randomness
            if random.random() < self.reaction_chance:
                if paddle_center < ball_center - 15:
                    self.paddle.move_down()
                elif paddle_center > ball_center + 15:
                    self.paddle.move_up()

class ScoreBoard:
    """Handles score display and management"""
    
    def __init__(self):
        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        self.tiny_font = pygame.font.Font(None, 24)
    
    def update_score(self, player_scored):
        """Update the score when a point is scored"""
        if player_scored:
            self.player_score += 1
        else:
            self.ai_score += 1
    
    def draw(self, screen, difficulty='medium'):
        """Draw the scoreboard on screen"""
        # Draw scores
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        
        # Position scores in upper portion of screen
        screen.blit(player_text, (WINDOW_WIDTH // 4 - player_text.get_width() // 2, 50))
        screen.blit(ai_text, (3 * WINDOW_WIDTH // 4 - ai_text.get_width() // 2, 50))
        
        # Draw center line
        for i in range(0, WINDOW_HEIGHT, 20):
            pygame.draw.rect(screen, GRAY, (WINDOW_WIDTH // 2 - 2, i, 4, 10))
        
        # Draw labels
        player_label = self.small_font.render("PLAYER", True, WHITE)
        ai_label = self.small_font.render("AI", True, WHITE)
        
        screen.blit(player_label, (WINDOW_WIDTH // 4 - player_label.get_width() // 2, 100))
        screen.blit(ai_label, (3 * WINDOW_WIDTH // 4 - ai_label.get_width() // 2, 100))
        
        # Draw difficulty indicator
        difficulty_color = DIFFICULTY_SETTINGS[difficulty]['color']
        difficulty_text = self.tiny_font.render(f"Difficulty: {difficulty.upper()}", True, difficulty_color)
        screen.blit(difficulty_text, (WINDOW_WIDTH // 2 - difficulty_text.get_width() // 2, 130))

class PongGame:
    """Main game class that handles game logic and rendering"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pong Game - Select Difficulty")
        self.clock = pygame.time.Clock()
        
        # Initialize sound manager
        self.sound_manager = SoundManager()
        
        # Game state
        self.game_state = 'menu'  # 'menu', 'playing'
        self.difficulty = 'medium'
        
        # Initialize game objects
        self.player_paddle = Paddle(30, WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.ai_paddle = Paddle(WINDOW_WIDTH - 30 - PADDLE_WIDTH, WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.ball = Ball(WINDOW_WIDTH // 2 - BALL_SIZE // 2, WINDOW_HEIGHT // 2 - BALL_SIZE // 2, 
                        self.sound_manager, self.difficulty)
        self.ai_player = AIPlayer(self.ai_paddle, self.ball, self.difficulty)
        self.scoreboard = ScoreBoard()
        
        self.running = True
    
    def handle_menu_events(self):
        """Handle events in the difficulty selection menu"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.start_game('easy')
                elif event.key == pygame.K_2:
                    self.start_game('medium')
                elif event.key == pygame.K_3:
                    self.start_game('hard')
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def start_game(self, difficulty):
        """Start the game with selected difficulty"""
        self.difficulty = difficulty
        self.game_state = 'playing'
        pygame.display.set_caption(f"Pong Game - {difficulty.capitalize()} Mode")
        
        # Reset game objects with new difficulty
        self.ball.set_difficulty(difficulty)
        self.ball.reset(difficulty)
        self.ai_player.set_difficulty(difficulty)
        self.scoreboard.player_score = 0
        self.scoreboard.ai_score = 0
    
    def handle_game_events(self):
        """Handle pygame events and keyboard input during gameplay"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = 'menu'
                    pygame.display.set_caption("Pong Game - Select Difficulty")
        
        # Handle continuous key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player_paddle.move_up()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player_paddle.move_down()
    
    def update_game_logic(self):
        """Update game state and handle collisions"""
        # Move ball
        self.ball.move()
        
        # Update AI
        self.ai_player.update()
        
        # Check paddle collisions
        if self.ball.rect.colliderect(self.player_paddle.rect):
            if self.ball.speed_x < 0:  # Only bounce if ball is moving toward paddle
                self.ball.speed_x *= -1
                self.sound_manager.play_sound('paddle_hit')
                # Add some angle based on where ball hits paddle
                hit_pos = (self.ball.y - self.player_paddle.y) / self.player_paddle.height
                self.ball.speed_y = (hit_pos - 0.5) * 8
        
        if self.ball.rect.colliderect(self.ai_paddle.rect):
            if self.ball.speed_x > 0:  # Only bounce if ball is moving toward paddle
                self.ball.speed_x *= -1
                self.sound_manager.play_sound('paddle_hit')
                # Add some angle based on where ball hits paddle
                hit_pos = (self.ball.y - self.ai_paddle.y) / self.ai_paddle.height
                self.ball.speed_y = (hit_pos - 0.5) * 8
        
        # Check for scoring
        if self.ball.x < 0:
            # AI scores
            self.scoreboard.update_score(False)
            self.sound_manager.play_sound('score')
            self.ball.reset(self.difficulty)
        elif self.ball.x > WINDOW_WIDTH:
            # Player scores
            self.scoreboard.update_score(True)
            self.sound_manager.play_sound('score')
            self.ball.reset(self.difficulty)
    
    def render_menu(self):
        """Render the difficulty selection menu"""
        self.screen.fill(BLACK)
        
        # Title
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("PONG", True, WHITE)
        self.screen.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, 150))
        
        # Subtitle
        subtitle_font = pygame.font.Font(None, 36)
        subtitle_text = subtitle_font.render("Select Difficulty", True, WHITE)
        self.screen.blit(subtitle_text, (WINDOW_WIDTH // 2 - subtitle_text.get_width() // 2, 220))
        
        # Difficulty options
        option_font = pygame.font.Font(None, 48)
        options = [
            ("1 - Easy", GREEN, 300),
            ("2 - Medium", YELLOW, 350),
            ("3 - Hard", RED, 400)
        ]
        
        for text, color, y_pos in options:
            option_text = option_font.render(text, True, color)
            self.screen.blit(option_text, (WINDOW_WIDTH // 2 - option_text.get_width() // 2, y_pos))
        
        # Instructions
        instruction_font = pygame.font.Font(None, 24)
        instructions = [
            "Press 1, 2, or 3 to select difficulty",
            "Press ESC to quit"
        ]
        
        for i, instruction in enumerate(instructions):
            text = instruction_font.render(instruction, True, GRAY)
            self.screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, 480 + i * 30))
        
        pygame.display.flip()
    
    def render_game(self):
        """Render all game objects to the screen"""
        # Clear screen with black background
        self.screen.fill(BLACK)
        
        # Draw game objects
        self.player_paddle.draw(self.screen)
        self.ai_paddle.draw(self.screen)
        self.ball.draw(self.screen)
        self.scoreboard.draw(self.screen, self.difficulty)
        
        # Draw instructions at bottom
        font = pygame.font.Font(None, 24)
        instructions = [
            "Use UP/DOWN arrows or W/S keys to move",
            "Press ESC to return to menu"
        ]
        
        for i, instruction in enumerate(instructions):
            text = font.render(instruction, True, GRAY)
            self.screen.blit(text, (10, WINDOW_HEIGHT - 50 + i * 25))
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        print("Starting Pong Game!")
        print("Select difficulty: 1=Easy, 2=Medium, 3=Hard")
        print("Controls: UP/DOWN arrows or W/S keys to move your paddle")
        print("Press ESC to quit or return to menu")
        
        while self.running:
            if self.game_state == 'menu':
                self.handle_menu_events()
                self.render_menu()
            elif self.game_state == 'playing':
                self.handle_game_events()
                self.update_game_logic()
                self.render_game()
            
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()

# Main execution
if __name__ == "__main__":
    game = PongGame()
    game.run()
