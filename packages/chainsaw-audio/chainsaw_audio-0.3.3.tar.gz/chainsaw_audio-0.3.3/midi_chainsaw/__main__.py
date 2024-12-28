#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# MIDI-Chainsaw
#
# Copyright (C) 2021 Grégory David <dev@groolot.net>
#
# MIDI-Chainsaw is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# MDIDI-Chainsaw is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program. If not, see
# <http://www.gnu.org/licenses/>.

"""Allow user to run MIDI-Chainsaw as a module."""

# Execute with:
# $ python -m midi_chainsaw

import midi_chainsaw

if __name__ == '__main__':
    midi_chainsaw.main()
