import pygame as pg


FPS = 15
BACKGROUND = (150, 90, 30)

BLACK = (0, 0, 0),
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

COLORS = [BLACK, WHITE]

CELL_QTY = 8

LTTRS = 'abcdefgh'
IMG_PATH = 'images/'
WIN_BG_IMG = 'flowers_background.jpg'
ROOK_IMG = 'w_Rook'
BOARD_BG_IMG = 'board_background.jpg'
CELL_BG_IMG = 'cell_background.jpeg'
TURN = ('w', 'b')
PIECES_TYPES = {
    'k': ('King', 'b'), 'K': ('King', 'w'),
    'q': ('Queen', 'b'), 'Q': ('Queen', 'w'),
    'r': ('Rook', 'b'), 'R': ('Rook', 'w'),
    'b': ('Bishop', 'b'), 'B': ('Bishop', 'w'),
    'n': ('Knight', 'b'), 'N': ('Knight', 'w'),
    'p': ('Pawn', 'b'), 'P': ('Pawn', 'w'),
    'Beer': ('Beer', 'w'), 'beer': ('Beer', 'b'),
    'Whisky': ('Whisky', 'w'), 'whisky': ('Whisky', 'b'),
    'SuperKing': ('SuperKing', 'w'), 'superking': ('SuperKing', 'b')
}

screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
screen.fill(WHITE)
WINDOW_SIZE = (screen.get_width(), screen.get_height())
CELL_SIZE = WINDOW_SIZE[1] // 10
