from game_config import *
import pygame as pg

FNT = pg.font.SysFont('arial', 100)


class Menu:
    def __init__(self):
        self._option_surfaces = []
        self._call_backs = []
        self._current_option_index = 0

    def append_option(self, option, callback):
        self._option_surfaces.append(FNT.render(option, True, (255, 255, 255)))
        self._call_backs.append(callback)

    def switch(self, direction):
        self._current_option_index = max(0, min(self._current_option_index + direction, len(self._option_surfaces) - 1))

    def select(self):
        self._call_backs[self._current_option_index]()

    def draw(self, surf, x, y, option_y_pudding):
        for i, option in enumerate(self._option_surfaces):
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * option_y_pudding)
            if i == self._current_option_index:
                pg.draw.rect(surf, (0, 100, 0), option_rect)
            surf.blit(option, option_rect)

    def get_max_width(self):
        max_width = 0
        for option in self._option_surfaces:
            if max_width < option.get_width():
                max_width = option.get_width()
        return max_width

    def get_max_height(self):
        return self._option_surfaces[0].get_height()