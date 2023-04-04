import pygame as pg
from game_config import *
pg.init()

class Chessboard:
    def __init__(self, parent_surface: pg.Surface,
                 cell_qty: int = CELL_QTY, cell_size: int = CELL_SIZE):
        self.__screen = parent_surface
