from game_config import *
from chess_item import *

clock = pg.time.Clock()
screen = pg.display.set_mode(WINDOW_SIZE)

chessboard = Chessboard(screen)

run = True
while run:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            run = False
            exit()
    pg.display.update()
