#!/usr/bin/env python

# Copyright (C) 2010 by Kevin Saff

# This file is part of the CA scanner.

# The CA scanner is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# The CA scanner is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with the CA scanner.  If not, see <http://www.gnu.org/licenses/>.

import pygame
import registry, window
from optparse import OptionParser
import os.path, logging

# create formatter
#formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# add formatter to ch
#ch.setFormatter(formatter)


def main():
    parser = OptionParser()
    options, args = parser.parse_args()

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    dirname = os.path.dirname(__file__)
    if dirname:
        os.chdir(dirname)

    for directory in ['algorithms']:
        registry.auto_register(os.path.join(os.path.dirname(__file__),
                                            directory))

    window.create(options, args, pygame).run()

if __name__ == '__main__':
    main()
