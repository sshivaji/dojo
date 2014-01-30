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


class EnginePanel(Label):

    def _update(self, engine_string):
        uci_info=engine_string.split(' ')
        if 'depth' in uci_info:
            self.depth = uci_info[uci_info.index('depth') + 1]
        if 'seldepth' in uci_info:
            self.seldepth = uci_info[uci_info.index('seldepth') + 1]
        if 'score' in uci_info:
            index = uci_info.index('score') + 1
            score_type = uci_info[index]
            if score_type == 'cp':
                self.score = str(float(uci_info[index+1])/100.0)
            if score_type == 'lowerbound':
                self.score = '>=' + str(float(uci_info[index+1])/100.0)
            if score_type == 'upperbound':
                self.score = '<=' + str(float(uci_info[index+1])/100.0)
            if score_type == 'mate':
                self.score = 'M' + uci_info[index+1]
        #if 'pv' in uci_info:
        #    self.pv = ' '.join(uci_info[uci_info.index('pv')+1:])
        if 'currmove' in uci_info:
            self.currmove = uci_info[uci_info.index('currmove')+1]
        if 'nps' in uci_info:
            self.nps = uci_info[uci_info.index('nps')+1]
        self.text = '[' + self.depth + '/' + self.seldepth + '] ' + self.score + ' ' + self.currmove + ' ' + str(int(self.nps)/1000) +'kN/s'


    def __init__(self, **kwargs):
        super(EnginePanel, self).__init__(**kwargs)
        sf.add_observer(self._update)
        self.depth = ''
        self.seldepth = ''
        #self.pv = ''
        self.score = ''
        self.currmove = ''
        self.nps = ''
