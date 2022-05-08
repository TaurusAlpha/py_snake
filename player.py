from enum import Enum
from typing import Tuple

import pygame


class Direction(Enum):
    UP = pygame.Vector2(0,-1)
    DOWN = pygame.Vector2(0,1)
    RIGHT = pygame.Vector2(1,0)
    LEFT = pygame.Vector2(-1,0)


class PlayerSegment:
    def __init__(self, position: pygame.Vector2) -> None:
        self.segment_position = position


class Player:
    def __init__(self, posX, posY) -> None:
        self.color = (45,86,191)
        self.head_position = pygame.Vector2(posX, posY)
        self.player_segments = [PlayerSegment(self.head_position)]
        self.speed = 300
        self.lives = 2
        self.score = 0
        self.direction = Direction.RIGHT
        self.speed_accum = 0

    
    @property
    def position(self) -> pygame.Vector2:
        return self.head_position


    def get_player_segments(self) -> Tuple[PlayerSegment]:
        return self.player_segments


    def move(self, delta_time: int) -> None:
        self.speed_accum += delta_time
        if self.speed_accum >= self.speed:
            last_segment = self.player_segments.pop().segment_position
            last_segment = self.head_position + self.direction.value
            self.head_position = last_segment
            self.player_segments = [PlayerSegment(self.head_position)] + self.player_segments
            self.speed_accum -= self.speed


    def set_direction(self, direction: Direction) -> None:
        if not self.direction.value + direction.value == (0,0):
            self.direction = direction


    def add_tail(self, segment: pygame.Vector2) -> None:
        self.head_position = segment
        self.player_segments = [PlayerSegment(self.head_position)] + self.player_segments


    def on_reset(self, posX: int, posY: int, live: int) -> None:
        self.head_position = pygame.Vector2(posX, posY)
        self.player_segments = [PlayerSegment(self.head_position)]
        self.lives = live
        