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

from kivy.uix.label import Label
import stockfish as sf


class GamePanel(Label):
    _game = None

    @property
    def game(self):
        return self._game

    @game.setter
    def game(self, g):
        if self._game is not None:
            self._game.unbind(moves=self._update_panel)
            self._game.unbind(start_position=self._update_panel)
        self._game = g
        g.bind(moves=self._update_panel)
        g.bind(start_position=self._update_panel)

    def _update_panel(self, instance, value):
        print 'PANEL UPDATE'
        return
        moves = sf.to_san(self._game.moves)
        display_list = []
        for i in range(0, len(moves)):
            if not i & 1:
                display_list.append(str(i / 2 + 1)+'. ')
            display_list.append(moves[i])
        self.text = ' '.join(display_list)
        print 'END PANEL UPDATE'
