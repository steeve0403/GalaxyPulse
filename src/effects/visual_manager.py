# src/effects/visual_manager.py
import random

from kivy.graphics import Line, Color, Quad
from kivy.properties import NumericProperty

from src.utils.transforms import transform
from src.utils.constants import *


class VisualManager():
    from src.utils.transforms import transform
    def __init__(self, widget, **kwargs):
        super(VisualManager).__init__(**kwargs)
        self.widget = widget


        self.vertical_lines = []

        self.horizontal_lines = []

        self.tiles = []
        self.tiles_coordinates = []

        # self.init_vertical_lines()
        # self.init_horizontal_lines()
        # self.init_tiles()

    def init_tiles(self):
        with self.widget.canvas:
            Color(1, 1, 1)
            for i in range(0, NB_TILES):
                self.tiles.append(Quad())

    def pre_fill_tiles_coordinates(self):
        for i in range(0, 10):
            self.tiles_coordinates.append((0, i))

    def generate_tiles_coordinates(self):
        last_y = 0
        last_x = 0

        for i in range(len(self.tiles_coordinates) - 1, -1, -1):
            if self.tiles_coordinates[i][1] < self.widget.current_y_loop:
                del self.tiles_coordinates[i]

        if len(self.tiles_coordinates) > 0:
            last_coordinates = self.tiles_coordinates[-1]
            last_x = last_coordinates[0]
            last_y = last_coordinates[1] + 1

        for i in range(len(self.tiles_coordinates), NB_TILES):
            r = random.randint(0, 2)
            # 0 -> all right
            # 1 -> right
            # 2 -> left
            start_index = -int(V_NB_LINES / 2) + 1
            end_index = start_index + V_NB_LINES - 1
            if last_x <= start_index:
                r = 1
            if last_x >= end_index:
                r = 2
            self.tiles_coordinates.append((last_x, last_y))
            if r == 1:
                last_x += 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
            if r == 2:
                last_x -= 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
            last_y += 1

    def init_vertical_lines(self):
        """Initialiser les lignes verticales."""
        with self.widget.canvas:
            for _ in range(V_NB_LINES):
                self.vertical_lines.append(Line())

    def init_horizontal_lines(self):
        """Initialiser les lignes horizontales."""
        with self.widget.canvas:
            for _ in range(H_NB_LINES):
                self.horizontal_lines.append(Line())

    def get_line_x_from_index(self, index):
        """Calculer la position X d'une ligne basée sur son index."""
        central_line_x = self.widget.point_perspective_x
        spacing = V_LINES_SPACING * self.widget.width
        offset = index - 0.5
        line_x = central_line_x + offset * spacing + self.widget.current_offset_x
        return line_x

    def get_line_y_from_index(self, index):
        spacing_y = H_LINES_SPACING * self.widget.height
        line_y = index * spacing_y - self.widget.current_offset_y
        return line_y

    def get_tile_coordinates(self, tile_x, tile_y):
        tile_y = tile_y - self.widget.current_y_loop
        x = self.get_line_x_from_index(tile_x)
        y = self.get_line_y_from_index(tile_y)
        return x, y

    def update_tiles(self):
        for i in range(0, NB_TILES):
            tile = self.tiles[i]
            tile_coordinates = self.tiles_coordinates[i]

            x_min, y_min = self.get_tile_coordinates(tile_coordinates[0], tile_coordinates[1])
            x_max, y_max = self.get_tile_coordinates(tile_coordinates[0] + 1, tile_coordinates[1] + 1)

            #   2   3
            #
            #   1   4
            x1, y1 = transform(self, x_min, y_min)
            x2, y2 = transform(self, x_min, y_max)
            x3, y3 = transform(self, x_max, y_max)
            x4, y4 = transform(self, x_max, y_min)

            tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]

    def update_vertical_lines(self):
        """Mettre à jour la position des lignes verticales."""
        start_index = -int(V_NB_LINES / 2) + 1
        for i in range(start_index, start_index + V_NB_LINES):
            line_x = self.get_line_x_from_index(i)
            x1, y1 = transform(self, line_x, 0)
            x2, y2 = transform(self, line_x, self.widget.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]

    def update_horizontal_lines(self):
        """Mettre à jour la position des lignes horizontales."""
        start_index = -int(V_NB_LINES / 2) + 1
        end_index = start_index + V_NB_LINES - 1

        x_min = self.get_line_x_from_index(start_index)
        x_max = self.get_line_x_from_index(end_index)

        for i in range(0, H_NB_LINES):
            line_y = self.get_line_y_from_index(i)
            x1, y1 = transform(self, x_min, line_y)
            x2, y2 = transform(self, x_max, line_y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]
