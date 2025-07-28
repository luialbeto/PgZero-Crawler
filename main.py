import math
import random
from pygame import Rect

GRID_SIZE = 32
WIDTH = 800
HEIGHT = 600
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"

class SpriteAnimator:
    """Handles sprite animation with multiple frames"""
    def __init__(self, frames, frame_duration=0.2):
        self.frames = frames
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.time_since_last_frame = 0
        
    def update(self, dt):
        self.time_since_last_frame += dt
        if self.time_since_last_frame >= self.frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.time_since_last_frame = 0
    
    def get_current_frame(self):
        return self.frames[self.current_frame]

class Character:
    """Base class for all game characters"""
    def __init__(self, grid_x, grid_y, sprite_name):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.target_x = grid_x
        self.target_y = grid_y
        self.world_x = grid_x * GRID_SIZE
        self.world_y = grid_y * GRID_SIZE
        self.sprite_name = sprite_name
        self.is_moving = False
        self.move_speed = 4.0
        
        self.idle_animator = SpriteAnimator([f"{sprite_name}_idle1", f"{sprite_name}_idle2"], 0.5)
        self.move_animator = SpriteAnimator([f"{sprite_name}_move1", f"{sprite_name}_move2"], 0.3)
        
    def start_move_to(self, new_grid_x, new_grid_y):
        """Start smooth movement to new grid position"""
        if not self.is_moving:
            self.target_x = new_grid_x
            self.target_y = new_grid_y
            self.is_moving = True
    
    def update(self, dt):
        """Update character position and animation"""
        if self.is_moving:
            target_world_x = self.target_x * GRID_SIZE
            target_world_y = self.target_y * GRID_SIZE
            
            dx = target_world_x - self.world_x
            dy = target_world_y - self.world_y
            
            move_distance = self.move_speed * GRID_SIZE * dt
            
            if abs(dx) < move_distance and abs(dy) < move_distance:
                self.world_x = target_world_x
                self.world_y = target_world_y
                self.grid_x = self.target_x
                self.grid_y = self.target_y
                self.is_moving = False
            else:
                if abs(dx) > 0:
                    self.world_x += move_distance if dx > 0 else -move_distance
                if abs(dy) > 0:
                    self.world_y += move_distance if dy > 0 else -move_distance
        
        if self.is_moving:
            self.move_animator.update(dt)
        else:
            self.idle_animator.update(dt)
    
    def get_current_sprite(self):
        """Get current sprite name for animation"""
        if self.is_moving:
            return self.move_animator.get_current_frame()
        else:
            return self.idle_animator.get_current_frame()

class Player(Character):
    """Player character class"""
    def __init__(self, grid_x, grid_y):
        super().__init__(grid_x, grid_y, "hero")
        self.health = 100
        self.alive = True

class Enemy(Character):
    """Enemy character class"""
    def __init__(self, grid_x, grid_y, enemy_type="skeleton"):
        super().__init__(grid_x, grid_y, enemy_type)
        self.patrol_center_x = grid_x
        self.patrol_center_y = grid_y
        self.patrol_radius = 3
        self.move_timer = 0
        self.move_interval = random.uniform(1.0, 3.0)
        
    def update(self, dt, game_grid, player):
        """Update enemy AI and movement"""
        super().update(dt)
        
        if not self.is_moving:
            self.move_timer += dt
            if self.move_timer >= self.move_interval:
                self.move_timer = 0
                self.move_interval = random.uniform(1.0, 3.0)
                self.try_random_move(game_grid)
    
    def try_random_move(self, game_grid):
        """Try to move to a random valid position within patrol area"""
        possible_moves = []
        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                
                new_x = self.grid_x + dx
                new_y = self.grid_y + dy
                
                distance = math.sqrt((new_x - self.patrol_center_x)**2 + (new_y - self.patrol_center_y)**2)
                if distance <= self.patrol_radius:
                    if self.is_valid_position(new_x, new_y, game_grid):
                        possible_moves.append((new_x, new_y))
        
        if possible_moves:
            new_x, new_y = random.choice(possible_moves)
            self.start_move_to(new_x, new_y)
    
    def is_valid_position(self, x, y, game_grid):
        """Check if position is valid for movement"""
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
            return False
        if game_grid[y][x] == 1:  
            return False
        return True

class Game:
    """Main game class"""
    def __init__(self):
        self.state = MENU
        self.sound_enabled = True
        self.music_enabled = True
        
        self.menu_buttons = {
            "start": Rect(300, 200, 200, 50),
            "sound": Rect(300, 270, 200, 50),
            "exit": Rect(300, 340, 200, 50)
        }
        
        self.player = None
        self.enemies = []
        self.game_grid = []
        self.init_game()
    
    def init_game(self):
        """Initialize game world"""
        self.game_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        
        for i in range(GRID_WIDTH):
            self.game_grid[0][i] = 1  
            self.game_grid[GRID_HEIGHT-1][i] = 1  
        for i in range(GRID_HEIGHT):
            self.game_grid[i][0] = 1  
            self.game_grid[i][GRID_WIDTH-1] = 1 
        
        for _ in range(20):
            x = random.randint(2, GRID_WIDTH-3)
            y = random.randint(2, GRID_HEIGHT-3)
            self.game_grid[y][x] = 1
        
        self.player = Player(5, 5)
        
        self.enemies = []
        for _ in range(6):
            while True:
                x = random.randint(2, GRID_WIDTH-3)
                y = random.randint(2, GRID_HEIGHT-3)
                if self.game_grid[y][x] == 0 and (x != 5 or y != 5):
                    enemy_type = random.choice(["skeleton", "orc", "goblin"])
                    self.enemies.append(Enemy(x, y, enemy_type))
                    break
    
    def handle_click(self, pos):
        """Handle mouse clicks"""
        if self.state == MENU:
            if self.menu_buttons["start"].collidepoint(pos):
                self.state = PLAYING
                self.init_game()
            elif self.menu_buttons["sound"].collidepoint(pos):
                self.sound_enabled = not self.sound_enabled
            elif self.menu_buttons["exit"].collidepoint(pos):
                exit()
        
    def handle_key(self, key):
        """Handle keyboard input"""
        if self.state == PLAYING and not self.player.is_moving and self.player.alive:
            new_x, new_y = self.player.grid_x, self.player.grid_y
            
            if key in [key.UP, key.W]:
                new_y -= 1
            elif key in [key.DOWN, key.S]:
                new_y += 1
            elif key in [key.LEFT, key.A]:
                new_x -= 1
            elif key in [key.RIGHT, key.D]:
                new_x += 1
            
            if self.is_valid_move(new_x, new_y):
                self.player.start_move_to(new_x, new_y)
                
                for enemy in self.enemies:
                    if enemy.grid_x == new_x and enemy.grid_y == new_y:
                        self.player.health -= 20
                        if self.player.health <= 0:
                            self.player.alive = False
                            self.state = GAME_OVER
        
        elif self.state == GAME_OVER:
            if key == key.SPACE:
                self.state = MENU
    
    def is_valid_move(self, x, y):
        """Check if move is valid"""
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
            return False
        if self.game_grid[y][x] == 1:
            return False
        return True
    
    def update(self, dt):
        """Update game state"""
        if self.state == PLAYING:
            self.player.update(dt)
            for enemy in self.enemies:
                enemy.update(dt, self.game_grid, self.player)
    
    def draw(self, screen):
        """Draw game"""
        screen.clear()
        screen.fill((20, 20, 40))
        
        if self.state == MENU:
            self.draw_menu(screen)
        elif self.state == PLAYING:
            self.draw_game(screen)
        elif self.state == GAME_OVER:
            self.draw_game_over(screen)
    
    def draw_menu(self, screen):
        """Draw main menu"""
        screen.draw.text("DUNGEON CRAWLER", center=(400, 100), 
                        fontsize=48, color="white")
        
        for button_name, rect in self.menu_buttons.items():
            color = (60, 60, 100) if button_name != "sound" else (60, 100, 60) if self.sound_enabled else (100, 60, 60)
            screen.draw.filled_rect(rect, color)
            screen.draw.rect(rect, "white")
            
            text = button_name.upper()
            if button_name == "sound":
                text = f"SOUND: {'ON' if self.sound_enabled else 'OFF'}"
            
            screen.draw.text(text, center=(rect.centerx, rect.centery),
                           fontsize=24, color="white")
    
    def draw_game(self, screen):
        """Draw game world"""
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                if self.game_grid[y][x] == 1:
                    screen.draw.filled_rect(rect, (100, 50, 30))  
                else:
                    screen.draw.filled_rect(rect, (40, 40, 60))   
                screen.draw.rect(rect, (80, 80, 100))
        
        for enemy in self.enemies:
            x = int(enemy.world_x + GRID_SIZE // 2)
            y = int(enemy.world_y + GRID_SIZE // 2)
            screen.draw.filled_circle((x, y), 12, "red")
            if enemy.is_moving:
                screen.draw.filled_circle((x, y), 8, "orange")
        
        if self.player.alive:
            x = int(self.player.world_x + GRID_SIZE // 2)
            y = int(self.player.world_y + GRID_SIZE // 2)
            screen.draw.filled_circle((x, y), 14, "blue")
            if self.player.is_moving:
                screen.draw.filled_circle((x, y), 10, "cyan")
        
        screen.draw.text(f"Health: {self.player.health}", (10, 10), fontsize=24, color="white")
    
    def draw_game_over(self, screen):
        """Draw game over screen"""
        screen.fill((40, 20, 20))
        screen.draw.text("GAME OVER", center=(400, 250), 
                        fontsize=64, color="red")
        screen.draw.text("Press SPACE to return to menu", center=(400, 350),
                        fontsize=32, color="white")

game = Game()

def on_mouse_down(pos):
    game.handle_click(pos)

def on_key_down(key):
    game.handle_key(key)

def update(dt):
    game.update(dt)

def draw():
    game.draw(screen)