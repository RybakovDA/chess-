import board_data
from game_config import *
import pygame as pg


class Piece(pg.sprite.Sprite):
    def __init__(self, cell_size: int, color: str, field_name: tuple, file_postfix: str, hp: int, damage: int, area_damage_type: int, radius_splash: int = 0):
        super().__init__()
        self.color = color
        self.hp = hp
        self.damage = damage
        self.area_damage_type = area_damage_type
        self.radius_splash = radius_splash
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
    # Literally ладья
    def __init__(self, cell_size: int, color: str, field: tuple):
        super().__init__(cell_size, color, field, '_Rook', hp=3, damage=1, area_damage_type=1)

    def can_move(self, cell):
        if cell.field_name[0] == self.field_name[0]:
            sign = (cell.field_name[1] - self.field_name[1]) // abs(self.field_name[1] - cell.field_name[1])
            for i in range(self.field_name[1], cell.field_name[1], sign):
                if i != self.field_name[1] and board_data.board[cell.field_name[0]][i] != 0:
                    return False
            return True
        if cell.field_name[1] == self.field_name[1]:
            sign = (cell.field_name[0] - self.field_name[0]) // abs(self.field_name[0] - cell.field_name[0])
            for i in range(self.field_name[0], cell.field_name[0], sign):
                if i != self.field_name[0] and board_data.board[i][cell.field_name[1]] != 0:
                    return False
            return True
        return False


class Beer(Piece):
    # Фигура может наносить урон по площади радиусом в 3 клетки, имеет урон 2 и hp = 2, может ходить через другие фигуры,
    # хождение по принципу шахматного ферзя
    def __init__(self, cell_size: int, color: str, field: tuple):
        super().__init__(cell_size, color, field, '_Beer', hp=2, damage=2, area_damage_type=2, radius_splash=3)

    def can_move(self, cell):
        if cell.field_name[0] == self.field_name[0] or cell.field_name[1] == self.field_name[1]:
            return True
        if abs(cell.field_name[0] - self.field_name[0]) == abs(cell.field_name[1] - self.field_name[1]):
            return True
        return False

class Whisky(Piece):
    # Фигура имеет свойство дальнобойности, ходит по принципу шахматного короля и имеет показатели hp = 2, damage = 1,
    # может ходить через другие фигуры
    def __init__(self, cell_size: int, color: str, field: tuple):
        super().__init__(cell_size, color, field, '_Whisky', hp=2, damage=1, area_damage_type=3, radius_splash=0)

    def can_move(self, cell):
        if abs(cell.field_name[0] - self.field_name[0]) <= 1 and abs(cell.field_name[1] - self.field_name[1]) <= 1:
            return True
        return False

class SuperKing(Piece):
    def __init__(self, cell_size: int, color: str, field: tuple):
        super().__init__(cell_size, color, field, '_SuperKing', hp=10, damage=1, area_damage_type=1, radius_splash=0)

    def can_move(self, cell):
        if abs(cell.field_name[0] - self.field_name[0]) <= 1 and abs(cell.field_name[1] - self.field_name[1]) <= 1:
            return True
        return False