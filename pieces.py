import board_data
from game_config import *
import pygame as pg


class Piece(pg.sprite.Sprite):
    def __init__(self, cell_size: int, color: str, field_name: tuple, file_postfix: str):
        super().__init__()
        self._color = color
        self.field_name = field_name
        pic = pg.image.load(IMG_PATH + color + file_postfix)
        self.image = pg.transform.scale(pic, (cell_size, cell_size))
        self.rect = self.image.get_rect()

    def move_piece(self, cell):
        self.rect = cell.rect.copy()
        self.field_name = cell.field_name


class Rook(Piece):
    def __init__(self, cell_size: int, color: str, field: str):
        super().__init__(cell_size, color, field, '_Rook')