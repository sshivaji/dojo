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
    floatingPiecePos = ListProperty([0, 0])
    floatingPiece = '.'
    floatingPieceFrom = -1
    floatingpieceAnimateFromOrigin = False

    def set_position(self, fen):
        self.fen = fen
        self.position = fen.split(' ')[0].replace('/', '')
        for i in range(1, 9):
            self.position = self.position.replace(str(i), '.' * i)

    def to_square(self, touch):
        f = int((touch.x - self.bottomLeft[0]) / self.squareSize)
        r = 7 - int((touch.y - self.bottomLeft[1]) / self.squareSize)
        return -1 if (touch.x - self.bottomLeft[0]) < 0 or f > 7 or (
            touch.y - self.bottomLeft[1]) < 0 or r > 7 else f + r * 8

    def to_coordinates(self, square):
        return (square % 8) * self.squareSize + self.bottomLeft[0], (7 - (square / 8)) * self.squareSize + \
                                                                    self.bottomLeft[1]

    def highlight_square(self, square):
        with self.canvas:
            Color(*self.highlightColor)
            left, bottom = self.to_coordinates(square)
            Line(points=[left, bottom, left + self.squareSize, bottom, left + self.squareSize, bottom + self.squareSize,
                         left, bottom + self.squareSize], width=2, close=True)

    def draw_piece(self, piece, position):
        with self.canvas:
            Color(*self.white)
            label = self.pieceTextures[self.backgroundTextures[piece]]
            Rectangle(texture=label.texture, pos=position, size=label.texture_size)
            Color(*self.black)
            label = self.pieceTextures[piece]
            Rectangle(texture=label.texture, pos=position, size=label.texture_size)

    def draw_pieces(self, skip=-1):
        i = 0
        for p in self.position:
            if p != '.' and i != skip:
                self.draw_piece(p, self.to_coordinates(i))
            i += 1

    def draw_board(self):
        with self.canvas:
            self.canvas.clear()
            Color(*self.dark)
            Rectangle(pos=self.bottomLeft, size=(self.boardSize, self.boardSize))
            Color(*self.light)
            for row in range(8):
                for file in range(8):
                    if (row + file) & 0x1:
                        Rectangle(pos=(
                            self.bottomLeft[0] + file * self.squareSize, self.bottomLeft[1] + row * self.squareSize),
                                  size=(self.squareSize, self.squareSize))

    def resize(self, instance, value):
        self.squareSize = (min(self.size) / 8)
        self.boardSize = self.squareSize * 8
        self.bottomLeft = ((self.width - self.boardSize) / 2, (self.height - self.boardSize) / 2)
        # Generate textures
        self.pieceTextures = {}
        for piece in 'pPnNbBrRqQkKUVWXYZ':
            self.pieceTextures[piece] = Label(text=piece, font_name='fonts/kivychess.ttf', font_size=self.squareSize)
            self.pieceTextures[piece].texture_update()
        self.draw_board()
        self.draw_pieces()

    def animate_piece(self, touch, pos):
        self.draw_board()
        self.draw_pieces(skip=self.floatingPieceFrom)
        self.draw_piece(self.floatingPiece, pos)

    def __init__(self):
        super(ChessBoardWidget, self).__init__()
        self.light = (1, 0.808, 0.620)
        self.dark = (0.821, 0.545, 0.278)
        self.black = (0, 0, 0)
        self.white = (1, 1, 1)
        self.highlightColor = (0.2, 0.710, 0.898)
        self.bind(size=self.resize)
        self.set_position('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        self.backgroundTextures = {'p': 'U', 'P': 'U', 'n': 'V', 'N': 'V', 'b': 'W', 'B': 'W', 'r': 'X', 'R': 'X',
                                   'q': 'Y', 'Q': 'Y', 'k': 'Z', 'K': 'Z'}
        self.bind(floatingPiecePos=self.animate_piece)

    def on_touch_down(self, touch):
        square = self.to_square(touch)
        if self.position[square] == '.' or (
            self.floatingPiece.isupper() if self.position[square].islower() else self.floatingPiece.islower()):
            self.floatingpieceAnimateFromOrigin = True
            return
        else:
            self.floatingpieceAnimateFromOrigin = False

        if square == -1:
            self.floatingPiece = '.'
            return
        else:
            self.floatingPiece = self.position[square]
        self.floatingPieceFrom = square
        self.draw_board()
        self.draw_pieces()
        self.highlight_square(square)

    def on_touch_move(self, touch):
        if self.floatingPiece == '.':
            return
        self.draw_board()
        self.draw_pieces(skip=self.floatingPieceFrom)
        self.highlight_square(self.floatingPieceFrom)
        self.draw_piece(self.floatingPiece, (touch.x - self.squareSize / 2, touch.y - self.squareSize / 2))

    @staticmethod
    def square_name(i):
        return 'abcdefgh'[i % 8] + str(8 - i / 8)

    def on_touch_up(self, touch):
        square = self.to_square(touch)
        if square == -1 or self.floatingPiece == '.' or square == self.floatingPieceFrom:
            return
        move = self.square_name(self.floatingPieceFrom) + self.square_name(square)
        if move in sf.legalMoves(self.fen):
            self.floatingPiecePos[0], self.floatingPiecePos[1] = self.to_coordinates(
                self.floatingPieceFrom) if self.floatingpieceAnimateFromOrigin else (
                touch.x - self.squareSize / 2, touch.y - self.squareSize / 2)
            anim = Animation(floatingPiecePos=self.to_coordinates(square), duration=0.1, t='in_out_sine')
            anim.start(self)
            print('MOVE : ' + move)
        else:
            if (self.floatingPiece == 'P' and square < 8) or (self.floatingPiece == 'p' and square > 55):
                #Show a popup for promotions
                layout = GridLayout(cols=2)

                def choose(piece):
                    popup.dismiss()
                    move = self.square_name(self.floatingPieceFrom) + self.square_name(square) + piece
                    if move in sf.legalMoves(self.fen):
                        print('MOVE : ' + move + piece)
                    else:
                        self.draw_board()
                        self.draw_pieces()

                for p in 'qrbn':
                    btn = Button(text=p, font_name='fonts/kivychess.ttf', font_size=self.boardSize / 3)
                    btn.bind(on_release=lambda btn: choose(p))
                    layout.add_widget(btn)
                popup = Popup(title='Promote to', content=layout)
                popup.open()
            else:  # Illegal move
                self.floatingPiecePos[0] = touch.x - self.squareSize / 2
                self.floatingPiecePos[1] = touch.y - self.squareSize / 2
                anim = Animation(floatingPiecePos=self.to_coordinates(self.floatingPieceFrom), duration=0.3,
                                 t='in_out_sine')
                anim.start(self)
        return


class MyApp(App):
    def build(self):
        self.title = sf.info().split(' by ')[0]
        return ChessBoardWidget()


if __name__ == '__main__':
    MyApp().run()