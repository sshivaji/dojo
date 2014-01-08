# Copyright (C) 2013-2014 Jean-Francois Romang (jromang@posteo.de)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import stockfish as sf
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.animation import Animation
from kivy.properties import ListProperty

#TODO PEP http://www.python.org/dev/peps/pep-0008/
#TODO PEP http://www.python.org/dev/peps/pep-0257/


class ChessBoardWidget(Widget):
    _moving_piece_pos = ListProperty([0, 0])
    _moving_piece = '.'
    _moving_piece_from = -1
    _animate_from_origin = False

    def set_position(self, fen):
        self.fen = fen
        self.position = fen.split(' ')[0].replace('/', '')
        for i in range(1, 9):
            self.position = self.position.replace(str(i), '.' * i)

    def _to_square(self, touch):
        f = int((touch.x - self.bottom_left[0]) / self.square_size)
        r = 7 - int((touch.y - self.bottom_left[1]) / self.square_size)
        return -1 if (touch.x - self.bottom_left[0]) < 0 or f > 7 or (
            touch.y - self.bottom_left[1]) < 0 or r > 7 else f + r * 8

    def _to_coordinates(self, square):
        return (square % 8) * self.square_size + self.bottom_left[0], (7 - (square / 8)) * self.square_size + self.bottom_left[1]

    def _highlight_square(self, square):
        with self.canvas:
            Color(*self.highlight_color)
            left, bottom = self._to_coordinates(square)
            Line(points=[left, bottom, left + self.square_size, bottom, left + self.square_size, bottom + self.square_size,
                         left, bottom + self.square_size], width=2, close=True)

    def _draw_piece(self, piece, position):
        with self.canvas:
            Color(*self.white)
            label = self.piece_textures[self._background_textures[piece]]
            Rectangle(texture=label.texture, pos=position, size=label.texture_size)
            Color(*self.black)
            label = self.piece_textures[piece]
            Rectangle(texture=label.texture, pos=position, size=label.texture_size)

    def _draw_pieces(self, skip=-1):
        i = 0
        for p in self.position:
            if p != '.' and i != skip:
                self._draw_piece(p, self._to_coordinates(i))
            i += 1

    def _draw_board(self):
        with self.canvas:
            self.canvas.clear()
            Color(*self.dark)
            Rectangle(pos=self.bottom_left, size=(self.board_size, self.board_size))
            Color(*self.light)
            for row in range(8):
                for file in range(8):
                    if (row + file) & 0x1:
                        Rectangle(pos=(
                            self.bottom_left[0] + file * self.square_size, self.bottom_left[1] + row * self.square_size), size=(self.square_size, self.square_size))

    def _resize(self, instance, value):
        self.square_size = (min(self.size) / 8)
        self.board_size = self.square_size * 8
        self.bottom_left = ((self.width - self.board_size) / 2, (self.height - self.board_size) / 2)
        # Generate textures
        self.piece_textures = {}
        for piece in 'pPnNbBrRqQkKUVWXYZ':
            self.piece_textures[piece] = Label(text=piece, font_name='fonts/kivychess.ttf', font_size=self.square_size)
            self.piece_textures[piece].texture_update()
        self._draw_board()
        self._draw_pieces()

    def _animate_piece(self, touch, pos):
        self._draw_board()
        self._draw_pieces(skip=self._moving_piece_from)
        self._draw_piece(self._moving_piece, pos)

    def __init__(self):
        super(ChessBoardWidget, self).__init__()
        self.light = (1, 0.808, 0.620)
        self.dark = (0.821, 0.545, 0.278)
        self.black = (0, 0, 0)
        self.white = (1, 1, 1)
        self.highlight_color = (0.2, 0.710, 0.898)
        self.bind(size=self._resize)
        self.set_position('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        self._background_textures = {'p': 'U', 'P': 'U', 'n': 'V', 'N': 'V', 'b': 'W', 'B': 'W', 'r': 'X', 'R': 'X',
                                    'q': 'Y', 'Q': 'Y', 'k': 'Z', 'K': 'Z'}
        self.bind(_moving_piece_pos=self._animate_piece)

    def on_touch_down(self, touch):
        square = self._to_square(touch)
        if self.position[square] == '.' or (self._moving_piece.isupper() if self.position[square].islower() else self._moving_piece.islower()):
            self._animate_from_origin = True
            return
        else:
            self._animate_from_origin = False

        if square == -1:
            self._moving_piece = '.'
            return
        else:
            self._moving_piece = self.position[square]
        self._moving_piece_from = square
        self._draw_board()
        self._draw_pieces()
        self._highlight_square(square)

    def on_touch_move(self, touch):
        if self._moving_piece == '.':
            return
        self._draw_board()
        self._draw_pieces(skip=self._moving_piece_from)
        self._highlight_square(self._moving_piece_from)
        self._draw_piece(self._moving_piece, (touch.x - self.square_size / 2, touch.y - self.square_size / 2))

    @staticmethod
    def square_name(i):
        return 'abcdefgh'[i % 8] + str(8 - i / 8)

    def on_touch_up(self, touch):
        square = self._to_square(touch)
        if square == -1 or self._moving_piece == '.' or square == self._moving_piece_from:
            return
        move = self.square_name(self._moving_piece_from) + self.square_name(square)
        if move in sf.legal_moves(self.fen):
            self._moving_piece_pos[0], self._moving_piece_pos[1] = self._to_coordinates(
                self._moving_piece_from) if self._animate_from_origin else (touch.x - self.square_size / 2, touch.y - self.square_size / 2)
            animation = Animation(_moving_piece_pos=self._to_coordinates(square), duration=0.1, t='in_out_sine')
            animation.start(self)
            print('MOVE : ' + move)
        else:
            if (self._moving_piece == 'P' and square < 8) or (self._moving_piece == 'p' and square > 55):
                #Show a popup for promotions
                layout = GridLayout(cols=2)

                def choose(piece):
                    popup.dismiss()
                    move = self.square_name(self._moving_piece_from) + self.square_name(square) + piece
                    if move in sf.legal_moves(self.fen):
                        print('MOVE : ' + move + piece)
                    else:
                        self._draw_board()
                        self._draw_pieces()

                for p in 'qrbn':
                    btn = Button(text=p, font_name='fonts/kivychess.ttf', font_size=self.board_size / 8)
                    btn.bind(on_release=lambda btn: choose(p))
                    layout.add_widget(btn)
                popup = Popup(title='Promote to', content=layout, size_hint=(.5, .5))
                popup.open()
            else:  # Illegal move
                self._moving_piece_pos[0] = touch.x - self.square_size / 2
                self._moving_piece_pos[1] = touch.y - self.square_size / 2
                animation = Animation(_moving_piece_pos=self._to_coordinates(self._moving_piece_from), duration=0.3,
                                      t='in_out_sine')
                animation.start(self)
        return


class MyApp(App):
    def build(self):
        self.title = sf.info().split(' by ')[0]
        return ChessBoardWidget()


if __name__ == '__main__':
    MyApp().run()