#!/usr/bin/env python3
import argparse
import logging
import sys
from mididings import *
from mididings.extra.osc import SendOSC

import importlib

class CLI(object):
    """Command Line Interface helper class"""

    def __init__(self):
        """CLI constructor"""
        self.arguments = argparse.Namespace()
        self.generalParser = argparse.ArgumentParser()
        self.oscParser = self.generalParser.add_argument_group('OSC', 'Open Sound Control parameters')
        self.setupParsingCLI()


    def performParsingCLI(self):
        """Do what its name sound"""

        self.arguments = self.generalParser.parse_args()
        screenLoggerFormat = logging.Formatter('%(levelname)s:%(filename)s: %(message)s')
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
                                        choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL'],
                                        dest="logLevel",
                                        default='WARNING',
                                        help="Select logging output level (default WARNING)")
        self.generalParser.add_argument("-v", "--verbose",
                                        action="store_const",
                                        dest="logLevel",
                                        const="DEBUG",
                                        help="Set the log level to DEBUG and be really verbose")

        # OSC
        self.oscParser.add_argument("-p", "--first-osc-port",
                                    action="store",
                                    type=int,
                                    dest="osc_port",
                                    default=8765,
                                    metavar="FIRST_OSC_PORT_NUMBER",
                                    help="Define the first OSC port to listen to (default 8765) for the first channel. +1 on each additionnal channel.")

        self.oscParser.add_argument("-t", "--osc-target-ip",
                                    action="store",
                                    type=str,
                                    dest="osc_target_ip",
                                    default="127.0.0.1",
                                    metavar="OSC_TARGET_IP",
                                    help="Define the OSC target IPv4 (default to '127.0.0.1')")

        # MIDI to OSC mapping template file
        self.oscParser.add_argument("-f", "--midi2osc-mapping-template-file",
                                    action="store",
                                    type=str,
                                    dest="midi2oscMappingTemplateFilename",
                                    default="midi_chainsaw.mapping_template",
                                    metavar="MAPPING_TEMPLATE_FILE",
                                    help="Define MIDI to OSC mapping template filename, with or without extension .py (default to 'midi_chainsaw.mapping_template')")

        # Number of channels (how many Chainsaw instances)
        self.oscParser.add_argument("-n", "--nchan",
                                    action="store",
                                    type=int,
                                    dest="nchan",
                                    default=1,
                                    metavar="CHANNEL_NUMBER",
                                    help="Define the number of channel to instance")


def main():
    route = {}
    patch = [Print()]
    cli = CLI().performParsingCLI()
    channel_module = importlib.import_module(cli.midi2oscMappingTemplateFilename)
    config(
        backend='jack',
        client_name='midi_chainsaw'
    )
    
    for channel in range(1, cli.nchan + 1):
        route[channel] = channel_module.route
        for cc in route[channel]:
            for address in route[channel][cc]:
                for method in route[channel][cc][address]:
                    logging.info("Register " + address + " " + method)
                    filtre = ChannelFilter(channel) >> CtrlFilter(cc)
                    oscArgs = route[channel][cc][address][method][0:]
                    args = [method]
                    if len(oscArgs) > 0 :
                        """
                        '!' will be replaced by the cc's value normalized between 0 and 1
                        '?' will be replaced by the cc's value (not normalized)
                        If argument list is empty, method is considered as a TRIGGER
                        """
                        for arg in oscArgs:
                            if arg == '!':
                                args.append(lambda ev: ev.value / 127.0)
                            elif arg == '?':
                                args.append(lambda ev: ev.value)
                            else:
                                args.append(arg)
                    else:
                        filtre = filtre >> CtrlValueFilter(lower=1)
                    patch.append(filtre >> SendOSC((cli.osc_target_ip, cli.osc_port + channel - 1), address, *args))

                    logging.debug("Chan" + str(channel) + "/CC#" + str(cc) + " to OSC: " + " ".join([str(address), str(args)]))
    amp_control = ChannelFilter(10) >> (
        CtrlRange(1, 0, 69) >>
        CtrlRange(2, 0, 69) >>
        CtrlRange(3, 0, 69) >>
        CtrlRange(4, 0, 69) >>
        CtrlRange(5, 0, 69) >>
        CtrlRange(6, 0, 69) >>
        CtrlRange(7, 0, 69) >>
        CtrlRange(8, 0, 69)
        )
    patch.append(amp_control)
    run(patch)
