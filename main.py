from chess_item import *
from menu import *
import board_data

clock = pg.time.Clock()
screen = pg.display.set_mode(WINDOW_SIZE)
menu = Menu()
chessboard = Chessboard(screen, 7)
menu.append_option('PLAY', chessboard.make_board)
menu.append_option('RESTART', chessboard.make_new_board)
menu.append_option('QUIT', menu.quit)
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
            if key[pg.K_ESCAPE]:
                flag = True
                screen.fill(BLACK)
                menu.draw(screen, (screen.get_width() - menu.get_max_width()) // 2, screen.get_height() // 2,
                          2 * menu.get_max_height())
            if board_data.is_superking_killed != 0:
                flag = True
                screen.fill(BLACK)
                menu.draw(screen, (screen.get_width() - menu.get_max_width()) // 2, screen.get_height() // 2,
                          2 * menu.get_max_height())
        pg.display.flip()
