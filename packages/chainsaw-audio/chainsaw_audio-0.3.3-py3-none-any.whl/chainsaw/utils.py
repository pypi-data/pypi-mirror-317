# -*- coding: utf-8 -*-
"""This module supplies some smart utilities"""

import logging
import pyo
import math


def mapToRange(inVal, rangeIn=[0, 1], rangeOut=None, scale="lin", resolution="float"):
    """
    Map a value (inVal) from a range to another range

    Params:

    inVal : numberfloat
    input value

    rangeIn : list
    min and max values expected in input

    rangeOut : list
    min and max value expected in output
    if rangeOut[0] > rangeOut[1] the scale will be reversed accordingly

    scale : str
    scaling mode between rangeIn and rangeOut
    'lin'  - linear
    'exp'  - exponential
    'sqr'  - x**2
    'cub'  - x**3
    'log'  - logarithmic
    'sqrt' - square root (better than 'log')

    resolution : str
    output number resolution
    'float' - default
    'int' - value will be rounded and parsed as an integer
    """

    rangeInMin = min(rangeIn[0],
                     rangeIn[1])
    rangeInMax = max(rangeIn[0],
                     rangeIn[1])
    outVal = float(max(rangeInMin, min(inVal, rangeInMax)))

    if rangeOut is not None:
        rangeOutMin = min(rangeOut[0],
                          rangeOut[1])
        rangeOutMax = max(rangeOut[0],
                          rangeOut[1])
        dIn = rangeInMax - rangeInMin
        dOut = rangeOutMax - rangeOutMin
        normalizedInput = (outVal - rangeInMin) / dIn
        scaleOut = dOut + rangeOutMin
        if scale == 'log':
            outVal = math.log10(normalizedInput * 9 + 1) * scaleOut
        elif scale == 'exp':
            outVal = (math.pow(10, normalizedInput) /
                      9.0 - 1.0 / 9.0) * scaleOut
        elif scale == 'sqr':
            outVal = normalizedInput**2 * scaleOut
        elif scale == 'cub':
            outVal = normalizedInput**3 * scaleOut
        elif scale == 'sqrt':
            outVal = math.sqrt(normalizedInput) * scaleOut
        elif scale == 'lin' or scale is None:
            outVal = normalizedInput * scaleOut

        outVal = max(rangeOutMin, min(outVal, rangeOutMax))

    if resolution == 'int':
        outVal = int(round(outVal))
    return outVal


def mapArgs(method):
    """
    Decorator function : filter a method's argument by applying mapToRange
    Retrieve the arguments from self.exposed_to_osc, which must be a dictionnary
    of the following form :
    self.exposed_to_osc = {
        "methodToExposeAndDecorate": {"rangeIn": [0,1], "rangeOut": [0,127], "scale": "lin", "resolution": "float"},
        # etc
    }


    Usage:

    @mapArgs
    self.methodToExposeAndDecorate(self, value):
        ...
    """

    def setter(self, IN):
        arguments = self.exposed_to_osc[method.__name__]
        OUT = mapToRange(IN, **arguments)
        logging.info("From '%s' mapping '%s %s' to '%s %s' using '%s' scale method" % (method.__name__, IN, arguments.get(
            "rangeIn", [0, 1]), OUT, arguments.get("rangeOut", ""), arguments.get("scale", "lin")))
        return method(self, OUT)

    return setter
