#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import pyo
from chainsaw.configuration import jackname, audioInputs, audioServer, commandLine, monitorManager
from chainsaw.osc import OscRootNode

# Global name
__program__ = "chainsaw"
__version__ = '0.3.3'
__author__ = 'Grégory David'
__author_email__ = 'dev@groolot.net'
__license__ = 'GPLv3'


def main():
    """
    Main program entry
    """
    from chainsaw.instruments import Instrument

    oscRoot = OscRootNode(commandLine.jackname, oscPort=commandLine.port)
    instrument = Instrument("instrument")
    instrument.out()

    oscRoot.addChild(instrument)
    oscRoot.addChild(monitorManager)
    oscRoot.dumpOscTree()
    audioServer.start()
    audioServer.gui(
        locals=locals() if logging.getLogger().getEffectiveLevel() == logging.DEBUG else None,
        title=jackname,
        exit=False
    )
