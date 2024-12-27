import pygame
import sys
from chain_reaction import ChainReaction  # Assuming your previous implementation is in chain_reaction.py

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

class ChainReactionUI:
    def __init__(self, length, width, cell_size=100):
        pygame.init()
        
        # Game setup
        self.length = length
        self.width = width
        self.cell_size = cell_size
        
        # Screen dimensions
        self.screen_width = width * cell_size
        self.screen_height = length * cell_size + 50  # Extra space for turn display
        
        # Pygame setup
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Chain Reaction')
        
        # Game logic
        self.game = ChainReaction(length, width)
        
        # Player turn
        self.current_player = 1
        self.moves_count = 0  # Count moves to skip winner check on the first move
        
        # Font for turn display
        self.font = pygame.font.Font(None, 36)
    
    def draw_grid(self):
        # Clear screen
        self.screen.fill(WHITE)
        
        # Draw grid lines
        for x in range(0, self.screen_width, self.cell_size):
            pygame.draw.line(self.screen, GRAY, (x, 50), (x, self.screen_height))
        for y in range(50, self.screen_height, self.cell_size):
            pygame.draw.line(self.screen, GRAY, (0, y), (self.screen_width, y))
        
        # Draw atoms
        for y in range(self.length):
            for x in range(self.width):
                dot = self.game.grid[y][x]
                
                # Determine color based on owner
                if dot.owner == 1:
                    color = RED
                elif dot.owner == 2:
                    color = BLUE
                else:
                    continue
                
                # Draw atoms
                center_x = x * self.cell_size + self.cell_size // 2
                center_y = y * self.cell_size + self.cell_size // 2 + 50
                
                for i in range(dot.atoms):
                    angle = (360 / dot.atoms) * i
                    radius = min(self.cell_size // 4, 15)
                    offset_x = int(radius * 1.5 * pygame.math.Vector2(1, 0).rotate(angle).x)
                    offset_y = int(radius * 1.5 * pygame.math.Vector2(1, 0).rotate(angle).y)
                    pygame.draw.circle(self.screen, color, 
                                       (center_x + offset_x, center_y + offset_y), 
                                       radius // 2)
    
    def draw_turn(self):
        # Display current player's turn
        turn_text = f"Player {self.current_player}'s Turn"
        text_surface = self.font.render(turn_text, True, BLACK)
        text_rect = text_surface.get_rect(center=(self.screen_width // 2, 25))
        self.screen.blit(text_surface, text_rect)
    
    def display_winner(self, winner):
        # Display the winner
        winner_text = f"Player {winner} Wins!"
        text_surface = self.font.render(winner_text, True, BLACK)
        text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.fill(WHITE)
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

    def handle_click(self, pos):
        # Adjust for top margin
        adjusted_y = pos[1] - 50
    
        # Convert screen coordinates to grid coordinates
        x = pos[0] // self.cell_size
        y = adjusted_y // self.cell_size
    
        # Validate click is within grid
        if 0 <= x < self.width and 0 <= y < self.length:
            dot = self.game.grid[y][x]
        
            # Check if cell is either:
            # 1. Unoccupied (owner == 0)
            # 2. Owned by the current player
            if dot.owner == 0 or dot.owner == self.current_player:
                try:
                    # Attempt to add dot
                    self.game.add_dot(y, x, self.current_player)
                    self.moves_count += 1

                    # Check if the game is over (skip check for the first move)
                    if self.moves_count > 1:
                        winner = self.game.check_game_over()
                        if winner != -1:
                            self.display_winner(winner)
                    
                    # Switch players if move was valid
                    self.current_player = 3 - self.current_player
                except Exception:
                    # If move is invalid for any reason, keep same player's turn
                    pass
    
    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        self.handle_click(event.pos)
            
            # Draw everything
            self.draw_grid()
            self.draw_turn()
            
            # Update display
            pygame.display.flip()
            
            # Control game speed
            clock.tick(30)

# Run the game
if __name__ == "__main__":
    game_ui = ChainReactionUI(5, 9)
    game_ui.run()
