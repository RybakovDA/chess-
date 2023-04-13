import pygame as pg
from pieces import *
import board_data
from game_config import *

pg.init()
FNT = pg.font.SysFont('arial', 18)


class Chessboard:
    def __init__(self, parent_surface: pg.Surface,
                 cell_qty: int = CELL_QTY, cell_size: int = CELL_SIZE, start_pos: list = board_data.board):
        self.__picked_piece = None
        self.__pressed_cell = None
        self.__dragged_piece = None

        self.__cell_qty = cell_qty
        self.__cell_size = cell_size

        self.__all_areas = pg.sprite.Group()
        self.__all_cells = pg.sprite.Group()
        self.__all_pieces = pg.sprite.Group()

        self.__screen = parent_surface
        self.__table = start_pos

        self.__pieces_types = PIECES_TYPES

        self.__prepare_screen()
        self.__draw_playboard()
        self.__draw_all_pieces()

        self.__clean_screen = self.__screen.copy()

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
        playboard_view.fill(WHITE)
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
        n_lines = pg.Surface((self.__cell_size * self.__cell_qty, self.__cell_size // 2), pg.SRCALPHA)
        n_rows = pg.Surface((self.__cell_size // 2, self.__cell_size * self.__cell_qty), pg.SRCALPHA)

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
                    (x, y)
                )
                group.add(cell)
                color_index ^= True
            color_index ^= True
        return group

    def __prepare_screen(self):
        back_img = pg.image.load(IMG_PATH + WIN_BG_IMG)
        back_img = pg.transform.scale(back_img, WINDOW_SIZE)
        self.__screen.blit(back_img, (0, 0))

    def __draw_cells_on_playboard(self, cells_offset):
        for cell in self.__all_cells:
            cell.rect.x += cells_offset[0]
            cell.rect.y += cells_offset[1]
        self.__all_cells.draw(self.__screen)

    def __draw_all_pieces(self):
        self.__setup_board()
        self.__all_pieces.draw(self.__screen)

    def __setup_board(self):
        for j, row in enumerate(self.__table):
            for i, field_value in enumerate(row):
                if field_value != 0:
                    piece = self.__create_piece(field_value, (j, i))
                    self.__all_pieces.add(piece)
        for piece in self.__all_pieces:
            for cell in self.__all_cells:
                if piece.field_name == cell.field_name:
                    piece.rect = cell.rect.copy()

    def __create_piece(self, piece_sym: str, cords: tuple):
        piece_description = self.__pieces_types[piece_sym]
        field = cords
        piece_name = globals()[piece_description[0]]
        return piece_name(self.__cell_size, piece_description[1], field)

    def __get_cell(self, position):
        for cell in self.__all_cells:
            if cell.rect.collidepoint(position):
                return cell
        return None

    def __get_cell_from_cords(self, position):
        for cell in self.__all_cells:
            if cell.field_name == position:
                return cell
        return None

    def btn_down(self, button_type: int, position: tuple):
        self.__pressed_cell = self.__get_cell(position)
        if self.__pressed_cell is not None:
            if button_type == 1:
                self.__unmark_all_cells()
                self.__dragged_piece = self.__get_piece_on_cell(self.__pressed_cell)
                if self.__dragged_piece is not None:
                    self.__dragged_piece.rect.center = position
                    self.__main_update()





    def btn_up(self, button_type: int, position: tuple):
        released_cell = self.__get_cell(position)
        if released_cell is not None and released_cell == self.__pressed_cell:
            if button_type == 1:
                self.__pick_cell(released_cell)
            if button_type == 3:
                # TODO
                if self.__get_piece_on_cell(released_cell) is None:
                    self.__mark_cell(released_cell)
                elif self.__get_piece_on_cell(released_cell).is_splash_atack() > 0:
                    self.__splash_attack(released_cell)
                else:  # TODO
                    pass

        if self.__dragged_piece is not None:
            if released_cell is not None:
                self.__want_to_move(self.__dragged_piece, released_cell)
            else:
                self.__return_to_cell(self.__dragged_piece)
            self.__dragged_piece = None
        self.__main_update()

    def __attack(self, piece, cell, type_attack: int):
        end_piece = self.__get_piece_on_cell(cell)
        if piece.can_bite(end_piece):
            end_piece.kill()
            if type_attack == 1:
                self.__change_board_data(piece, cell)
                piece.move_piece(cell)
            elif type_attack == 2:
                self.__change_board_data(None, cell)
                self.__return_to_cell(piece)
            else:  # TODO
                pass
        else:
            end_piece.hp -= piece.damage
            self.__return_to_cell(piece)

    def __splash_attack(self, cell):
        piece = self.__get_piece_on_cell(cell)
        radius = piece.radius_splash
        for i in range(-radius + 1, radius):
            for j in range(abs(i) - radius + 1, radius - abs(i)):
                if i == 0 and j == 0:
                    continue
                new_cell_coords = (cell.field_name[0] + i, cell.field_name[1] + j)
                new_cell = self.__get_cell_from_cords(new_cell_coords)
                if new_cell is not None and self.__get_piece_on_cell(new_cell) is not None:
                    self.__attack(piece, new_cell, 2)


    def __mark_cell(self, cell):
        if not cell.mark:
            mark = Area(cell)
            self.__all_areas.add(mark)
        else:
            for area in self.__all_areas:
                if area.field_name == cell.field_name:
                    area.kill()
                    break
        cell.mark ^= True

    def __main_update(self):
        self.__screen.blit(self.__clean_screen.copy(), (0, 0))
        self.__all_cells.draw(self.__screen)
        self.__all_areas.draw(self.__screen)
        self.__all_pieces.draw(self.__screen)
        pg.display.update()

    def __pick_cell(self, cell):
        self.__unmark_all_cells()
        self.__return_to_cell(self.__dragged_piece)
        if self.__picked_piece is None:
            piece = self.__get_piece_on_cell(cell)
            if piece is not None:
                pick = Area(cell, False)
                self.__all_areas.add(pick)
                self.__picked_piece = piece
        else:
            self.__want_to_move(self.__picked_piece, cell)
            self.__picked_piece = None

    def __get_piece_on_cell(self, cell):
        for piece in self.__all_pieces:
            if piece.field_name == cell.field_name:
                return piece
        return None

    def __unmark_all_cells(self):
        self.__all_areas.empty()
        for cell in self.__all_cells:
            cell.mark = False

    def drag(self, position: tuple):
        if self.__dragged_piece is not None:
            self.__dragged_piece.rect.center = position
            self.__main_update()

    def __change_board_data(self, piece, cell):
        cell_x, cell_y = cell.field_name
        if piece is None:
            self.__table[cell_x][cell_y] = 0
            return
        piece_x, piece_y = piece.field_name
        self.__table[cell_x][cell_y] = self.__table[piece_x][piece_y]
        self.__table[piece_x][piece_y] = 0
        print(self.__table)

    def __want_to_move(self, piece, end_cell):
        if self.__get_cell_from_cords(piece.field_name) is end_cell:
            self.__return_to_cell(piece)
            return
        end_piece = self.__get_piece_on_cell(end_cell)
        if piece.can_move(end_cell):
            if end_piece is None:
                self.__change_board_data(piece, end_cell)
                piece.move_piece(end_cell)
            else:
                self.__attack(piece, end_cell, 1)
        else:
            self.__return_to_cell(piece)

    def __return_to_cell(self, piece):
        if piece is not None:
            piece.move_piece(self.__get_cell_from_cords(piece.field_name))


class Cell(pg.sprite.Sprite):
    def __init__(self, color_index: int, size: int, cords: tuple, name: tuple):
        super().__init__()
        x, y = cords
        self.mark = False
        self.color = COLORS[color_index]
        self.field_name = name
        self.image = pg.image.load(IMG_PATH + CELL_BG_IMG)
        self.image = pg.transform.scale(self.image, (size, size))
        self.rect = pg.Rect(x * size, y * size, size, size)


class Area(pg.sprite.Sprite):
    def __init__(self, cell: Cell, type_of_area: bool = True):
        super().__init__()
        cords = (cell.rect.x, cell.rect.y)
        size = (cell.rect.width, cell.rect.height)
        if type_of_area:
            pic = pg.image.load(IMG_PATH + WIN_BG_IMG)
            self.image = pg.transform.scale(pic, size)
        else:
            pic = pg.image.load(IMG_PATH + BOARD_BG_IMG)
            self.image = pg.transform.scale(pic, size)
        self.rect = pg.Rect(cords, size)
        self.field_name = cell.field_name
