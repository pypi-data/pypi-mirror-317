#!/bin/env python3

# SPDX-FileCopyrightText: 2024 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

from licomp.interface import UseCase
from licomp.interface import Provisioning
from licomp.main_base import LicompParser

from licomp_gnuguide.config import cli_name
from licomp_gnuguide.config import description
from licomp_gnuguide.config import epilog
from licomp_gnuguide.gnuguide import GnuQuickGuideLicense

def main():
    lg = GnuQuickGuideLicense()
    o_parser = LicompParser(lg,
                            cli_name,
                            description,
                            epilog,
                            UseCase.LIBRARY,
                            Provisioning.BIN_DIST)
    o_parser.run()


if __name__ == '__main__':
    main()
