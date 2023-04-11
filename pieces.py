import board_data
from game_config import *
import pygame as pg


class Piece(pg.sprite.Sprite):
    def __init__(self, cell_size: int, color: str, field_name: tuple, file_postfix: str, hp: int, damage: int, area_damage_type: int):
        super().__init__()
        self._color = color
        self.hp = hp
        self.damage = damage
        self.area_damage_type = area_damage_type
        self.field_name = field_name
        pic = pg.image.load(IMG_PATH + color + file_postfix)
        self.image = pg.transform.scale(pic, (cell_size, cell_size))
        self.rect = self.image.get_rect()



    def move_piece(self, cell):

        self.rect = cell.rect.copy()
        self.field_name = cell.field_name

    def can_move(self, cell):
        return False

    def can_bite(self, piece):
        if self.damage >= piece.hp:
            return True
        return False


class Rook(Piece):
    def __init__(self, cell_size: int, color: str, field: tuple):
        super().__init__(cell_size, color, field, '_Rook', hp=1, damage=1, area_damage_type=1)

    def can_move(self, cell):
        if cell.field_name[0] == self.field_name[0] or cell.field_name[1] == self.field_name[1]:
            return True
        return False

