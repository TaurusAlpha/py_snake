import pygame


class UserInterface:
    def __init__(self) -> None:
        self.score = 0
        self.msg = pygame.font.Font('./assets/40KLcsfs.ttf', 24)


    def hud_message(self, message: str) -> pygame.Surface:
        return self.msg.render(message, False, 'Black')
