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
from kivy.event import EventDispatcher
from kivy.properties import ListProperty, StringProperty

class Game(EventDispatcher):
    start_position = StringProperty('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    moves = ListProperty([])

    def current_fen(self):
        return sf.get_fen(self.start_position, self.moves)

    def legal_moves(self):
        return sf.legal_moves(self.current_fen())