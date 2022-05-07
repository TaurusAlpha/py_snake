import pygame

from entity import Apple
from player import Player, PlayerSegment


class Grid(pygame.surface.Surface):
    def __init__(self, grid_size, grid_block_size) -> None:
        super().__init__((grid_size*grid_block_size, grid_size*grid_block_size), pygame.SRCALPHA, 32)
        self.grid_size = grid_size - 1
        self.grid_block_size = grid_block_size


    def draw_grid(self, snake: Player, apple: Apple) -> None:
        self.fill(apple.color, self.position_to_rect(apple.position))
        for segment in snake.get_player_segments():
            self.fill(snake.color, self.position_to_rect(segment.segment_position))


    def position_to_rect(self, pos: pygame.Vector2) -> pygame.rect.Rect:
        return pygame.rect.Rect(pos.x*self.grid_block_size, pos.y*self.grid_block_size, self.grid_block_size, self.grid_block_size)
