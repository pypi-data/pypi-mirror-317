#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module encapsulate the OSC mechanism"""

import logging
import pyo
import re


class OscNode(object):
    """Represent an individual node in the OSC tree"""

    def __init__(self, name, parent=None, children=None):
        """
        OscNode constructor
        Set the node's name that will be use as an identifier

        Params:
        name : str
        """
        self.nodeName = str(name)
        self.parent = parent
        self.children = children if children is not None else {}
        self.exposed_to_osc = {}

    def addChild(self, childNode):
        """
        Add a child to the node, store it children against its nodeName

        Params:
        childNode : OscNode
        """
        if not hasattr(childNode, "nodeName"):
            raise TypeError('ERROR: could not add child %s to node %s (not a valid OscNode instance)' % (
                str(childNode), self.nodeName))

        self.removeChild(childNode.nodeName)
        logging.debug("Parent '%s' has a new child: '%s'" %
                      (self.nodeName, childNode.nodeName))
        self.children[childNode.nodeName] = childNode

    def removeChild(self, childName):
        """
        Remove a child from the node

        Params:
        childName : str
        """
        if childName in self.children:
            logging.debug("Parent '%s' lost child: '%s'" %
                          (self.nodeName, childName))
            del self.children[childName]

    def stringMatch(self, regExpPattern, subject):
        """
        Shorthand for regexp pattern matching
        Returns a boolean

        Params:
        regExpPattern : str
        subject : str
        """
        pattern = re.compile("^" + regExpPattern + "$")
        match = pattern.match(subject)
        matched = match != None and len(match.string) > 0
        match_string = "Match" if matched else "Mismatch"
        logging.debug("%s node '%s' comparing '%s' to '%s'" %
                      (match_string, self.nodeName, regExpPattern, subject))
        return matched

    def receiveOsc(self, path, *args):
        """
        Receive OSC message and check if the node should interpret it
        """
        if self.stringMatch(path[0], self.nodeName):
            logging.debug("Node '%s' process OSC path: %s" %
                          (self.nodeName, path))
            self.processOsc(path, *args)

    def processOsc(self, path, *args):
        """
        Process received osc message

        Params:
        path : list (of node names)
        *args : anything?
        """
        if len(path) == 1:
            # The message has reach its target
            # args[0] = method to execute
            # args[1:] = args to pass
            methodName = self.lastMethod = args[0]
            if methodName in self.exposed_to_osc:
                methodArgs = args[1:]
                getattr(self, methodName, self.processFallback)(*methodArgs)
        else:
            # pass the message to the next target
            newPath = path[1:]

            for name in self.children:
                self.children[name].receiveOsc(newPath, *args)

    def processFallback(self, *args):
        """Process OSC fallback

        When a processOsc do not find any method to call, this one is called and
        prints a nice warning message
        """
        logging.warning("'%s' is not defined in '%s' node. Args were: %s" % (
            self.lastMethod, self.nodeName, str(args)))

    def debug(self, *args):
        """Debugging"""
        logging.debug("'%s' node receives '%s' args" %
                      (self.nodeName, str(args)))


class OscRootNode(OscNode):
    """Root node of the OSC tree"""

    def __init__(self, name, children=None, oscPort=None):
        """
        OscRootNode constructor
        Instanciate an OSC server listening on port "oscPort"
        Set a list of children whom OSC messages will be transfered to

        Params:
        name : str
        oscPort : int
        """
        OscNode.__init__(self, name, children=children)
        logging.info("'%s' creates an OSC server listening on port:'%s'" %
                     (self.nodeName, oscPort))
        self.server = pyo.OscListener(self.normalizeOsc, oscPort)
        logging.debug("'%s' starts its OSC server" % (self.nodeName))
        self.server.start()

    def normalizeAddress(self, address):
        """
        Convert OSC 1.1 compliant address to regexp pattern standards
        Escape ^, $ (start/end of string delimiters) and \ (escape char)
        ?           -> .?
        [!a-Z]      -> [^a-Z]
        {foo,bar}   -> (foo|bar)

        Params:
        address : str
        """
        patterns = {
            r"\?": ".",
            r"\*": ".*",
            r"\[!([^\]]*)\]": r"[^\1]",
            r"\$": r"\$",
            r"\^": r"\^",
            r"\\": r"\\"
        }

        for pattern, repl in patterns.items():
            normAddress = re.sub(pattern, repl, address)

        def transliteration(match):
            s = match.group(0)
            s = s.replace("{", "(")
            s = s.replace("}", ")")
            s = s.replace(",", "|")
            return s

        normAddress = re.sub(re.compile(
            r"\{[^\}]*\}"), transliteration, normAddress)

        logging.debug("'%s' normalized OSC address from '%s' to '%s'" %
                      (self.nodeName, address, normAddress))
        return normAddress

    def normalizeOsc(self, address, *args):
        """
        Normalise OSC message and pass it to receiveOsc method
        Split the address into a path array whose items represent the nodes to traverse
        """

        normAddress = self.normalizeAddress(address)

        if normAddress[0] == "/":
            normAddress = normAddress[1:]
        if normAddress[-1] == "/":
            normAddress = normAddress[0:len(normAddress)-2]

        path = normAddress.split("/")
        logging.debug("'%s' computed OSC path from '%s' to '%s'" %
                      (self.nodeName, address, path))
        self.receiveOsc(path, *args)

    def dumpOscTree(self):
        """Prints the OSC tree from this root node"""
        logging.info("==== BEGIN DUMP OSC TREE ====")
        startLevel = 0

        def traverseTree(child, level):
            tabs = level * 2 * " "
            logging.info(tabs + child.nodeName)
            if len(child.exposed_to_osc) > 0:
                tabs += " "
                for childFunction in sorted(child.exposed_to_osc.keys()):
                    logging.info(tabs + childFunction + "()")
            if len(child.children) > 0:
                keys = sorted(child.children)
                for childName in keys:
                    traverseTree(child.children[childName], level + 1)

        traverseTree(self, startLevel)
        logging.info("==== END DUMP OSC TREE ====")


if __name__ == "__main__":
    from chainsaw.configuration import commandLine
    oscRouter = OscRootNode("osc", oscPort=commandLine.port)
    oscRouter.addChild(OscNode("nodeOne"))
    oscRouter.addChild(OscNode("nodeTwo"))
    oscRouter.children["nodeTwo"].addChild(OscNode("nodeTwoSubOne"))
    oscRouter.children["nodeTwo"].addChild(OscNode("nodeTwoSubTwo"))
    oscRouter.addChild(OscNode("nodeThree"))
    oscRouter.addChild(OscNode("nodeFour"))
    oscRouter.children["nodeFour"].addChild(OscNode("nodeFourSubOne"))
    oscSender = pyo.OscDataSend("sfiTFdN", commandLine.port, "/osc/node*")
    oscSender.send(["debug", 1.0, 2, True, False, 1234.5678, None])
    oscRouter.dumpOscTree()

    from configuration import audioServer
    audioServer.start()
    audioServer.gui(locals())
