import pygame as pg
from game_config import *

pg.init()
clock = pg.time.Clock()

FNT = pg.font.SysFont('arial', 18)

screen = pg.display.set_mode(WINDOW_SIZE)
screen.fill(BACKGROUND)

n_lines = pg.Surface((CELL_SIZE * CELL_QTY, CELL_SIZE // 2))
n_rows = pg.Surface((CELL_SIZE // 2, CELL_SIZE * CELL_QTY))
fields = pg.Surface((CELL_SIZE * CELL_QTY, CELL_SIZE * CELL_QTY))
board = pg.Surface((2 * n_rows.get_width() + fields.get_width(), 2 * n_lines.get_height() + fields.get_height()))

for y in range(CELL_QTY):
    for x in range(CELL_QTY):
        cell = pg.Surface((CELL_SIZE, CELL_SIZE))
        cell.fill(COLORS[(x + y + 1) % 2])
        fields.blit(cell, (x*CELL_SIZE, y*CELL_SIZE))
for i in range(CELL_QTY):
    letter = FNT.render(LTTRS[i], True, BLUE)
    number = FNT.render(str(CELL_QTY - i), True, BLUE)

    n_lines.blit(letter, (i * CELL_SIZE + (CELL_SIZE - letter.get_rect().width) // 2,
                          (n_lines.get_height()-letter.get_rect().height) // 2))
    n_rows.blit(number, ((n_rows.get_width() - number.get_rect().height) // 2, i * CELL_SIZE + (CELL_SIZE - letter.get_rect().height) // 2))

board.blit(n_rows, (0, n_lines.get_height()))
board.blit(n_rows, (n_rows.get_width() + fields.get_width(), n_lines.get_height()))
board.blit(n_lines, (n_rows.get_width(), 0))
board.blit(n_lines, (n_rows.get_width(), n_rows.get_width() + fields.get_width()))
board.blit(fields, (n_rows.get_width(), n_lines.get_height()))

screen.blit(board, ((WINDOW_SIZE[0] - board.get_width()) // 2, (WINDOW_SIZE[1] - board.get_height()) // 2))
pg.display.update()

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            run = False
            exit()
    pg.display.update()
    clock.tick(FPS)
