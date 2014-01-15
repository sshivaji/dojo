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

import kivy
kivy.require('1.0.5')

from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
import stockfish as sf
from game import Game
from random import choice
from kivy.config import Config

#Set start resolution
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '800')


#class MyApp(App):
#   def build(self):
#        self.title = sf.info().split(' by ')[0]
#        self.game = Game()
#        print self.game.moves
#        print self.game.start_position
#        return ChessBoardWidget(self.game)

#MyApp().run()

class Controller(FloatLayout):
    '''Create a controller that receives a custom widget from the kv lang file.

    Add an action to be called from the kv lang file.
    '''
    label_wid = ObjectProperty()
    info = StringProperty()
    title = StringProperty()
    game = ObjectProperty()

    def do_action(self):
        self.label_wid.text = 'My label after button press'
        self.info = 'New info text'
        #self.chessboard_wid.game=self.game
        try:
            self.game.moves.append(choice(self.game.legal_moves()))
        except IndexError:
             print 'No legal moves'

class DojoApp(App):

    def build(self):
        return Controller(info='Hello world', title=sf.info().split(' by ')[0], game=Game())

if __name__ == '__main__':
    DojoApp().run()