# -*- coding: utf-8 -*-
"""Command Line Interface module"""

import argparse
import logging
import sys


class CLI(object):
    """Command Line Interface helper class"""

    def __init__(self):
        """CLI constructor"""
        self.arguments = argparse.Namespace()
        self.generalParser = argparse.ArgumentParser()
        self.portaudioParser = self.generalParser.add_argument_group(
            'PORTAUDIO', 'Define specific options to Portaudio audio driver')
        self.jackParser = self.generalParser.add_argument_group(
            'JACK', 'Jack Audio Connection Kit specific options')
        self.oscParser = self.generalParser.add_argument_group(
            'OSC', 'Open Sound Control parameters')
        self.setupParsingCLI()

    def performParsingCLI(self):
        """Do what its name sound"""

        self.arguments = self.generalParser.parse_args()
        screenLoggerFormat = logging.Formatter(
            '%(levelname)s:%(filename)s: %(message)s')
        screenLoggerHandler = logging.StreamHandler(stream=sys.stderr)
        screenLoggerHandler.setFormatter(screenLoggerFormat)
        logging.getLogger().addHandler(screenLoggerHandler)
        logging.getLogger().setLevel(getattr(logging, self.arguments.logLevel))
        logging.debug("Command line arguments: " + repr(self.arguments))
        return self.arguments

    def setupParsingCLI(self):
        """Configure the argument parser with some options"""
        # General options
        self.generalParser.add_argument("-l", "--log-level",
                                        choices=['DEBUG', 'INFO',
                                                 'WARNING', 'ERROR', 'CRITICAL'],
                                        dest="logLevel",
                                        default='WARNING',
                                        help="Select logging output level (default WARNING)")
        self.generalParser.add_argument("-v", "--verbose",
                                        action="store_const",
                                        dest="logLevel",
                                        const="DEBUG",
                                        help="Set the log level to DEBUG and be really verbose")
        self.generalParser.add_argument("--length",
                                        type=float,
                                        default=30,
                                        help="Live recording buffer length in seconds (default 30)")

        # OSC
        self.oscParser.add_argument("-p", "--osc-port",
                                    action="store",
                                    type=int,
                                    dest="port",
                                    default=8765,
                                    metavar="OSC_PORT_NUMBER",
                                    help="Define the OSC port to listen to (default 8765)")

        # Portaudio group options
        self.portaudioParser.add_argument("--portaudio",
                                          action="store_const",
                                          dest="audio",
                                          const="portaudio",
                                          help="Define 'portaudio' as the audio server backend and set the supplied number as the main audio interface (see --list-devices to know your audio interface number). If a combination of --portaudio and --jack are used, the last one is the winner")
        self.portaudioParser.add_argument("-a", "--list-portaudio-devices",
                                          action="store_true",
                                          dest="listPortaudioDevices",
                                          help="Print the list of your 'portaudio' system audio interfaces")
        self.portaudioParser.add_argument("-A", "--portaudio-device",
                                          action="store",
                                          type=int,
                                          dest="portaudioDevice",
                                          default=27,
                                          help="Define the 'portaudio' audio interface device by its number (default 27)")

        # Jack group options
        self.jackParser.add_argument("--jack",
                                     action="store_const",
                                     dest="audio",
                                     const="jack",
                                     default="jack",
                                     help="Define 'jack' as the audio server backend (default). If a combination of --portaudio and --jack are used, the last one is the winner")
        self.jackParser.add_argument("--jackname",
                                     action="store",
                                     default="chainsaw",
                                     type=str,
                                     help="Define the name of the 'jack' client. Usefull in conjonction with a 'jack' session management like Qjackctl/PatchBay or Gladish (default 'chainsaw')")
        self.jackParser.add_argument("--sampling-rate",
                                     action="store",
                                     type=int,
                                     dest="samplingRate",
                                     default=48000,
                                     help="Define the audio server sampling rate (default 48000)")
