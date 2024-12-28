#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Graph the routing using Graphviz """

import logging
import pygraphviz as pgv
import cli

def main():
    """ Main logic"""
    command_line = cli.CLI().performParsingCLI()
    logging.debug("")
    route = command_line.routeModule.route
    graph = pgv.AGraph(name="MIDI2OSCrouting",
                       label="Chainsaw routing MIDI to OSC",
                       strict=True,
                       directed=True)
    graph.node_attr['shape'] = 'record'

    def recursive_elements(_arbre, _osc_string, _channel, _control_change, _function=None):
        """ recursively create a dictionary from the route mapping """
        if len(_osc_string.split('/')) == 1:
            if isinstance(_arbre, dict):
                if _osc_string not in _arbre.keys():
                    _arbre[_osc_string] = dict()
            if _function not in _arbre[_osc_string]:
                _arbre[_osc_string][_function] = {'linker': '%s%s%s' % (_function,
                                                                        _channel,
                                                                        _control_change),
                                                  'chan': _channel,
                                                  'cc': _control_change}
        else:
            element = _osc_string.split('/', maxsplit=1)[0]
            if element not in _arbre.keys():
                _arbre[element] = dict()
            recursive_elements(_arbre[element],
                               _osc_string.split('/', maxsplit=1)[1],
                               _channel,
                               _control_change,
                               _function)
        return

    osc_structure = dict()
    for channel in route:
        for control_change in route[channel]:
            for target in route[channel][control_change]:
                for function in route[channel][control_change][target]:
                    recursive_elements(osc_structure, target[1:], channel, control_change, function)

    for channel in route:
        node_name = 'chnl_' + str(channel)
        channel_name = 'Chan: ' + str(channel)
        node_label = channel_name + '|{'
        cc_counter = 0
        for control_change in route[channel]:
            cc_source_name = 'cc%s' % (control_change)
            cc_name = '<%s> cc:%s' % (cc_source_name, control_change)
            if cc_counter == 0:
                node_label = '%s %s' % (node_label, cc_name)
            else:
                node_label = '%s | %s' % (node_label, cc_name)
            for target in route[channel][control_change]:
                for function in route[channel][control_change][target]:
                    graph.add_node(function)
                    graph.add_edge(node_name, function, tailport=cc_source_name, label='t')
            cc_counter += 1
        node_label = node_label + '}'
        graph.add_node(node_name, label=node_label)

    graph.layout(prog='fdp')
    graph.draw('route.pdf')

if __name__ == "__main__":
    main()
