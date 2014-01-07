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

    floatingPiecePos=ListProperty([0,0])
    floatingPiece='.'
    floatingPieceFrom=-1

    def setPosition(self, fen):
        self.fen=fen
        self.position=fen.split(' ')[0].replace('/','')
        for i in range (1,9):
            self.position=self.position.replace(str(i),'.'*i)

    def toSquare(self,touch):
        f=int((touch.x-self.bottomLeft[0])/self.squareSize)
        r=7-int((touch.y-self.bottomLeft[1])/self.squareSize)
        if (touch.x-self.bottomLeft[0])<0 or f>7 or (touch.y-self.bottomLeft[1])<0 or r>7 : return -1
        return f+r*8

    def toCoordinates(self, square):
        return (square%8)*self.squareSize+self.bottomLeft[0],(7-(square/8))*self.squareSize+self.bottomLeft[1]
            
    def highlightSquare(self, square, color):
        with self.canvas:
            Color(*color)
            left, bottom=self.toCoordinates(square)
            Line(points=[left, bottom, left+self.squareSize, bottom, left+self.squareSize, bottom+self.squareSize, left, bottom+self.squareSize], width=2, close=True)
        
    def drawPiece(self, piece, position):
        with self.canvas:
            Color(*self.white)
            label=self.pieceTextures[self.backgroundTextures[piece]]
            Rectangle(texture=label.texture, pos=position, size=label.texture_size)
            Color(*self.black)
            label=self.pieceTextures[piece]
            Rectangle(texture=label.texture, pos=position, size=label.texture_size)
            
    def drawPieces(self, skip=-1):
        i=0
        for p in self.position:
            if p!='.' and i!=skip:
                self.drawPiece(p,self.toCoordinates(i))
            i+=1
            
    def drawBoard(self):     
        with self.canvas:
            self.canvas.clear()
            Color(*self.dark)
            Rectangle(pos=self.bottomLeft, size=(self.boardSize, self.boardSize))
            Color(*self.light)
            for row in range(8):
                for file in range(8):
                    if((row+file)&0x1):
                        Rectangle(pos=(self.bottomLeft[0]+file*self.squareSize, self.bottomLeft[1]+row*self.squareSize), size=(self.squareSize, self.squareSize))
                      
    def resize(self, instance,value):
        self.squareSize=(min(self.size)/8)  
        self.boardSize=self.squareSize*8
        self.bottomLeft=((self.width-self.boardSize)/2, (self.height-self.boardSize)/2)
        #Generate textures
        self.pieceTextures={}
        for piece in 'pPnNbBrRqQkKUVWXYZ':
            self.pieceTextures[piece]=Label(text=piece, font_name='fonts/kivychess.ttf', font_size=self.squareSize)
            self.pieceTextures[piece].texture_update()
        self.drawBoard() #Draw the board
        self.drawPieces() #Draw pieces
        
    def animateFloatingPiece(self,touch,pos):
        self.drawBoard() #Draw the board
        self.drawPieces(skip=self.floatingPieceFrom) #Draw pieces
        self.drawPiece(self.floatingPiece,pos)

    def __init__(self):
        super(ChessBoardWidget, self ).__init__()
        self.light = (1, 0.808, 0.620 )
        self.dark = (0.821, 0.545, 0.278)
        self.black = (0, 0, 0)
        self.white = (1, 1, 1)
        self.bind(size=self.resize)
        self.setPosition('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        self.backgroundTextures={'p':'U','P':'U','n':'V','N':'V','b':'W','B':'W','r':'X','R':'X','q':'Y','Q':'Y','k':'Z','K':'Z'}
        self.bind(floatingPiecePos=self.animateFloatingPiece)
    
    def on_touch_down(self, touch):
        square=self.toSquare(touch)
        if square==-1 : 
            touch.ud['movingPiece']='.'
            return
        else : 
            touch.ud['movingPiece']=self.position[square]
        if self.position[square]=='.' : return
        touch.ud['fromSquare']=square
        self.drawBoard() #Draw the board
        self.drawPieces() #Draw pieces
        self.highlightSquare(square,(1,1,0))

    def on_touch_move(self, touch):
        if touch.ud['movingPiece']=='.' : return
        self.drawBoard() #Draw the board
        self.drawPieces(skip=touch.ud['fromSquare'])#Draw pieces
        self.highlightSquare(touch.ud['fromSquare'],(1,1,0))
        self.drawPiece(touch.ud['movingPiece'],(touch.x-self.squareSize/2,touch.y-self.squareSize/2))
    
    def squareName(self, i):
        return 'abcdefgh'[i%8]+str(8-i/8)
    
    def on_touch_up(self, touch):
        square=self.toSquare(touch)
        if square==-1 or touch.ud['movingPiece']=='.' or square==touch.ud['fromSquare'] : return
        move=self.squareName(touch.ud['fromSquare'])+self.squareName(square)
        if move in sf.legalMoves(self.fen):
            self.floatingPiece=touch.ud['movingPiece']
            self.floatingPieceFrom=touch.ud['fromSquare']
            self.floatingPiecePos[0]=touch.x-self.squareSize/2
            self.floatingPiecePos[1]=touch.y-self.squareSize/2
            anim = Animation(floatingPiecePos=self.toCoordinates(square), duration=0.04, t='in_out_sine')
            anim.start(self)
            print('MOVE : '+move)
        else:
            if (touch.ud['movingPiece']=='P' and square<8) or (touch.ud['movingPiece']=='p' and square> 55):
                #Show a popup for promotions
                layout = GridLayout(cols=2)
                def choose(piece):
                    popup.dismiss()
                    move=self.squareName(touch.ud['fromSquare'])+self.squareName(square)+piece
                    if move in sf.legalMoves(self.fen):
                        print('MOVE : '+move+piece)
                    else:
                        self.drawBoard() #Draw the board
                        self.drawPieces() #Draw pieces
                for p in 'qrbn':
                    btn=Button(text=p,font_name='fonts/kivychess.ttf', font_size=self.boardSize/3)
                    btn.bind(on_release=lambda btn: choose(p))
                    layout.add_widget(btn)
                popup = Popup(title='Promote to', content=layout)
                popup.open()
            else:
                self.floatingPiece=touch.ud['movingPiece']
                self.floatingPieceFrom=touch.ud['fromSquare']
                self.floatingPiecePos[0]=touch.x-self.squareSize/2
                self.floatingPiecePos[1]=touch.y-self.squareSize/2
                anim = Animation(floatingPiecePos=self.toCoordinates(touch.ud['fromSquare']), duration=0.3, t='in_out_sine')
                anim.start(self)
        return      


class MyApp(App):
    def build(self):
        self.title = sf.info().split(' by ')[0]
        return ChessBoardWidget()

if __name__ == '__main__':
    MyApp().run()