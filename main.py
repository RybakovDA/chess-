import board_data
from game_config import *
from chess_item import *
from menu import *

clock = pg.time.Clock()
screen = pg.display.set_mode(WINDOW_SIZE)
menu = Menu()
chessboard = Chessboard(screen, 7, 70)
menu.append_option('PLAY', chessboard.make_board)
menu.append_option('RESTART', chessboard.make_new_board)
menu.append_option('QUIT', pg.quit)
run = True
flag = True
while run:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            run = False
            exit()
        if flag:
            key = pg.key.get_pressed()
            if key[pg.K_UP]:
                menu.switch(-1)
            if key[pg.K_DOWN]:
                menu.switch(1)
            if key[pg.K_RETURN] or key[pg.K_SPACE]:
                flag = False
                menu.select()
                continue
            screen.fill(BLACK)
            menu.draw(screen, (screen.get_width() - menu.get_max_width()) // 2, menu.get_max_height(),
                      2 * menu.get_max_height())
        else:
            key = pg.key.get_pressed()
            if event.type == pg.MOUSEBUTTONDOWN:
                chessboard.btn_down(event.button, event.pos)
            if event.type == pg.MOUSEBUTTONUP:
                chessboard.btn_up(event.button, event.pos)
            if event.type == pg.MOUSEMOTION:
                chessboard.drag(event.pos)
            if key[pg.K_BACKSPACE]:
                flag = True
                screen.fill(BLACK)
                menu.draw(screen, (screen.get_width() - menu.get_max_width()) // 2, menu.get_max_height(),
                          2 * menu.get_max_height())
    pg.display.update()
