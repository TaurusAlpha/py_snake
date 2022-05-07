from typing import Tuple

import pygame


class Apple:
    def __init__(self, posX, posY) -> None:
        self.color = (183,36,43)
        self.apple_position = pygame.Vector2(posX, posY)


    @property
    def position(self) -> pygame.Vector2:
        return self.apple_position
