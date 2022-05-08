from random import randint
from time import sleep
import pygame
from entity import Apple
from grid import Grid
from hud import UserInterface
from player import Direction, Player


class Core:
    def __init__(self) -> None:
        pygame.init()
        self.running = False
        self.grid = Grid(30, 30)
        self.snake = Player(self.grid.grid_block_size//2, self.grid.grid_block_size//2)
        self.apple = Apple(10,10)
        self.display = pygame.display
        self.display_surface = self.display.set_mode(self.grid.get_size() , pygame.HWSURFACE | pygame.DOUBLEBUF )
        self.display.set_caption("PySnake_v2")
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.display_bg = pygame.image.load("./assets/field_bg.jpg")
        self.display_bg = pygame.transform.scale(self.display_bg, self.grid.get_size())
        self.display_empty = pygame.Color(0, 0, 0, 0)
        self.user_hud = UserInterface()
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])
        self.start_ticks=pygame.time.get_ticks()
        self.timer = 0
        self.elapsed_time = 0
        self.update_interval = 300


    def events(self, event) -> None:
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.snake.set_direction(Direction.LEFT)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.snake.set_direction(Direction.RIGHT)
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                self.snake.set_direction(Direction.UP)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.snake.set_direction(Direction.DOWN)


    def render(self) -> None:
        self.grid.fill(self.display_empty)
        self.grid.convert_alpha()
        self.grid.draw_grid(self.snake, self.apple)
        self.display_surface.blit(self.display_bg, (0,0))
        self.display_surface.blit(self.grid, (0,0))
        self.display_surface.blit(self.user_hud.hud_message("Lives: " + str(self.snake.lives)), (100, 20))
        self.display_surface.blit(self.user_hud.hud_message("Score: " + str(self.snake.score)), (600, 20))
        # self.display_surface.blit(self.user_hud.hud_message("Timer: %.2f" % self.timer), (350, 20))
        self.display.update()


    def update(self, delta_time: int) -> None:
        self.check_apple_collision()
        self.check_collision()
        self.snake.move(delta_time)
        self.timer=(pygame.time.get_ticks()-self.start_ticks)/1000
        # self.clock.tick(self.fps)
    
    
    def on_cleanup(self) -> None:
        pygame.quit()


    def reset(self) -> None:
        if self.snake.lives > 0:
            self.snake.on_reset(self.grid.grid_block_size//2, self.grid.grid_block_size//2, self.snake.lives-1)
            self.init_apple()
        else:
            self.running = False


    def run(self):
        self.running = True

        while self.running:
            #Process keyboard events 
            delta_time = self.clock.tick(self.fps)
            for event in pygame.event.get():
                self.events(event)
            #Update logic
            self.update(delta_time)
            #Render/Draw
            self.render()
        #Clean stuff after quit
        self.on_cleanup()


    def init_apple(self):
        self.apple = Apple(randint(0, self.grid.grid_size), randint(0, self.grid.grid_size))
        for segment in self.snake.get_player_segments():
            if self.apple.apple_position == segment.segment_position:
                self.init_apple()
        if self.snake.score % 5 == 0:
            self.snake.speed -= 20


    def check_apple_collision(self) -> None:
        if self.apple.position == (self.snake.position + self.snake.direction.value):
            self.snake.add_tail(self.apple.position)
            self.snake.score += 1
            self.init_apple()


    def check_collision(self) -> None:
        if not (self.snake.position.x in range(0, self.grid.grid_size + 1)) \
            or not (self.snake.position.y in range(0, self.grid.grid_size + 1)):
            self.reset()
        if len(self.snake.get_player_segments()) > 4:
            for segment in self.snake.player_segments[3:]:
                if self.snake.position == segment.segment_position:
                    self.reset()
