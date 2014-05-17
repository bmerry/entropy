# Entropy: pauses Rhythmbox when the play queue is finished
# Copyright (C) 2014  Bruce Merry <bmerry@users.sourceforge.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function
from gi.repository import GObject, RB, Peas
import gettext

gettext.install('rhythmbox', RB.locale_dir())

class EntropyPlugin(GObject.Object, Peas.Activatable):
    object = GObject.property(type = GObject.Object)

    def __init__(self):
        super(EntropyPlugin, self).__init__()

    def get_shell_player(self):
        return self.object.props.shell_player

    def song_changed(self, entry, user_data):
        shell_player = self.get_shell_player()
        if shell_player.props.playing and self.playing_from_queue and not shell_player.props.playing_from_queue:
            shell_player.stop()
        self.playing_from_queue = shell_player.props.playing_from_queue

    def do_activate(self):
        '''
        Plugin activation
        '''
        shell_player = self.get_shell_player()
        self.playing_from_queue = shell_player.props.playing_from_queue

        self.song_changed_id = shell_player.connect('playing-song-changed', self.song_changed)

    def do_deactivate(self):
        shell_player = self.get_shell_player()
        shell_player.disconnect(self.song_changed_id)
