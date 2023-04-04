import pygame as pg
from game_config import *

pg.init()
FNT = pg.font.SysFont('arial', 18)


class Chessboard:
    def __init__(self, parent_surface: pg.Surface,
                 cell_qty: int = CELL_QTY, cell_size: int = CELL_SIZE):
        self.__cell_qty = cell_qty
        self.__cell_size = cell_size
        self.__all_cells = pg.sprite.Group()
        self.__screen = parent_surface
        self.__prepare_screen()
        self.__draw_playboard()
        pg.display.update()

    def __draw_playboard(self):
        total_width = self.__cell_qty * self.__cell_size
        num_fields = self.__create_num_fields()
        self.__all_cells = self.__create_all_cells()
        num_fields_depth = num_fields[0].get_width()
        playboard_view = pg.Surface((
            2 * num_fields_depth + total_width,
            2 * num_fields_depth + total_width
        )).convert_alpha()

        back_img = pg.image.load(IMG_PATH + BOARD_BG_IMG)
        back_img = pg.transform.scale(back_img, (playboard_view.get_width(), playboard_view.get_height()))
        playboard_view.blit(back_img, (0, 0))

        playboard_view.blit(num_fields[0], (0, num_fields_depth))
        playboard_view.blit(num_fields[0], (num_fields_depth + total_width, num_fields_depth))
        playboard_view.blit(num_fields[1], (num_fields_depth, 0))
        playboard_view.blit(num_fields[1], (num_fields_depth, num_fields_depth + total_width))

        playboard_rect = playboard_view.get_rect()
        playboard_rect.x += (self.__screen.get_width() - playboard_rect.width) // 2
        playboard_rect.y += (self.__screen.get_height() - playboard_rect.height) // 2
        self.__screen.blit(playboard_view, playboard_rect)
        cells_offset = (
            playboard_rect.x + num_fields_depth,
            playboard_rect.y + num_fields_depth
        )
        self.__draw_cells_on_playboard(cells_offset)

    def __create_num_fields(self):
        n_lines = pg.Surface((self.__cell_size * self.__cell_qty, self.__cell_size // 2)).convert_alpha()
        n_rows = pg.Surface((self.__cell_size // 2, self.__cell_size * self.__cell_qty)).convert_alpha()
        for i in range(self.__cell_qty):
            letter = FNT.render(LTTRS[i], True, BLUE)
            number = FNT.render(str(self.__cell_qty - i), True, BLUE)
            n_lines.blit(letter, (i * self.__cell_size + (self.__cell_size - letter.get_rect().width) // 2,
                                  (n_lines.get_height() - letter.get_rect().height) // 2))
            n_rows.blit(number, ((n_rows.get_width() - number.get_rect().height) // 2,
                                 i * self.__cell_size + (self.__cell_size - letter.get_rect().height) // 2))
        return n_rows, n_lines

    def __create_all_cells(self):
        group = pg.sprite.Group()
        color_index = 1 if self.__cell_qty % 2 == 0 else 0
        for y in range(self.__cell_qty):
            for x in range(self.__cell_qty):
                cell = Cell(
                    color_index,
                    self.__cell_size,
                    (x, y),
                    LTTRS[x] + str(self.__cell_qty - y)
                )
                group.add(cell)
                color_index ^= True
            color_index ^= True
        return group

    def __prepare_screen(self):
        back_img = pg.image.load(IMG_PATH + WIN_BG_IMG)
        self.__screen.blit(back_img, (0, 0))

    def __draw_cells_on_playboard(self, cells_offset):
        for cell in self.__all_cells:
            cell.rect.x += cells_offset[0]
            cell.rect.y += cells_offset[1]
        self.__all_cells.draw(self.__screen)


class Cell(pg.sprite.Sprite):
    def __init__(self, color_index: int, size: int, coords: tuple, name: str):
        super().__init__()
        x, y = coords
        self.color = COLORS[color_index]
        self.field_name = name
        self.image = pg.image.load(IMG_PATH + CELL_BG_IMG)
        self.image = pg.transform.scale(self.image, (size, size))
        self.rect = pg.Rect(x * size, y * size, size, size)
