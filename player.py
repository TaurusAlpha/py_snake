from enum import Enum
from typing import List, Tuple

import pygame

from entity import Apple


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
        self.speed = 1
        self.direction = Direction.RIGHT

    
    @property
    def position(self) -> pygame.Vector2:
        return self.head_position


    def get_player_segments(self) -> List[PlayerSegment]:
        return self.player_segments


    def move(self) -> None:
        last_segment = self.player_segments.pop().segment_position
        last_segment = self.head_position + self.direction.value
        self.head_position = last_segment
        self.player_segments = [PlayerSegment(self.head_position)] + self.player_segments


    def set_direction(self, direction: Direction) -> None:
        if not self.direction.value + direction.value == (0,0):
            self.direction = direction


    def add_tail(self, segment: pygame.Vector2) -> None:
        #self.player_segments.append(self.head_position)
        self.head_position = segment
        self.player_segments = [PlayerSegment(self.head_position)] + self.player_segments
