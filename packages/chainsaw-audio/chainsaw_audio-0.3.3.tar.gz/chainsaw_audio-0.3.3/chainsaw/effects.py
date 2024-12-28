#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module supply Effect, EffectChain and specialized effects.

Speciqlized are: Disto, Freeverb and FreqShift (list to be scaled up).

"""

import logging
import pyo
from chainsaw.osc import OscNode
from chainsaw.configuration import audioInputs
from chainsaw.utils import mapArgs


class Effect(OscNode):
    """Pyo effect wrapper with dry/wet setting support"""

    def __init__(self, name, parent, input=audioInputs[0]):
        """
        Effect constructor
        Make sure "effectType" matches a valid Pyo effect class
        Instanciate a FaderInput to act as the effect's input wrapper
        Instanciate the effect processor which takes the FaderInput as input
        Inherit from pyo.Mixer to output the audio stream
        and handle Dry/Wet setting between these two

        Params:
        name : str
        effectType : str
        input : PyoObject
        """
        OscNode.__init__(self, name, parent)

        self.in_fader = pyo.InputFader(input)
        self.wetLevel = pyo.Sig(0)
        self.out_fader = self.in_fader * \
            (1-self.wetLevel) + self * self.wetLevel
        logging.debug("Creates a new effect named '%s' as child of '%s'" % (
            name, getattr(parent, "nodeName", "ROOT")))
        self.exposed_to_osc.update(
            {
                "setWet": {"scale": "sqr"}
            }
        )

    def getOut(self):
        """Return the correct output based on the inner mixing mechanism"""
        return self.out_fader

    def out(self, chnl=0, inc=1, dur=0, delay=0):
        """Start processing and send samples to audio output beginning at chnl.

        This method returns self, allowing it to be applied at the object creation.

        Params:
        chnl : int
        Physical output assigned to the first audio stream of the object. Defaults to 0.

        inc : int
        Output channel increment value. Defaults to 1.

        dur : float
        Duration, in seconds, of the object’s activation. The default is 0 and means infinite duration.

        delay : float
        Delay, in seconds, before the object’s activation. Defaults to 0.
        """
        self.out_fader.out(chnl, inc, dur, delay)

    @mapArgs
    def setWet(self, wetLevel):
        """
        Set wet level (0 = dry = input signal only / 1 = wet = processed signal only)

        Params:
        wetLevel : float (between 0 and 1)
        """
        logging.info("Set '%s' effect wet level 'wetLevel' to %s" %
                     (self.nodeName, wetLevel))
        logging.debug("%s.wetLevel.setValue(%s)" % (self.nodeName, wetLevel))
        self.wetLevel.setValue(wetLevel)

    def setInput(self, newInput):
        """
        Set Effect's input

        Params:
        newInput : PyoObject
        """
        logging.info("Set '%s' audio input signal 'input' to %s" %
                     (self.nodeName, newInput))
        logging.debug("%s.in_fader.setInput(%s)" % (self.nodeName, newInput))
        self.in_fader.setInput(newInput)


class Disto(Effect, pyo.Disto):
    """Specialized effect as Disto"""

    def __init__(self, name, parent, input=audioInputs[0]):
        """Disto constructor"""
        pyo.Disto.__init__(self, input=audioInputs[0])
        Effect.__init__(self, name, parent, input)
        pyo.Disto.setInput(self, self.in_fader)
        self.exposed_to_osc.update(
            {
                "setDrive": {}
            }
        )

    @mapArgs
    def setDrive(self, drive):
        """
        Set disto drive amount

        Params:
        drive : float [0..1]
           Drive amount normalized
        """
        logging.info("Set '%s' Disto drive amount 'drive' to %s" %
                     (self.nodeName, drive))
        logging.debug("%s.setDrive(%s)" % (self.nodeName, drive))
        pyo.Disto.setDrive(self, drive)


class Freeverb(Effect, pyo.Freeverb):
    """Specialized effect as Freeverb"""

    def __init__(self, name, parent, input=audioInputs[0]):
        """Freeverb constructor"""
        pyo.Freeverb.__init__(
            self, input=audioInputs[0], size=0, damp=0.5, bal=1.0)
        Effect.__init__(self, name, parent, input)
        pyo.Freeverb.setInput(self, self.in_fader)
        self.exposed_to_osc.update(
            {
                "setSize": {}
            }
        )

    @mapArgs
    def setSize(self, size):
        """
        Set reverb room size

        Params:
        size : float [0..1]
           Reverb room size
        """
        logging.info("Set '%s' Freeverb room size 'size' to %s" %
                     (self.nodeName, size))
        logging.debug("%s.setSize(%s)" % (self.nodeName, size))
        pyo.Freeverb.setSize(self, size)


class FreqShift(Effect, pyo.FreqShift):
    """Specialized effect as FreqShift"""

    def __init__(self, name, parent, input=audioInputs[0]):
        """FreqShift constructor"""
        pyo.FreqShift.__init__(self, input=audioInputs[0])
        Effect.__init__(self, name, parent, input)
        pyo.FreqShift.setInput(self, self.in_fader)
        self.exposed_to_osc.update(
            {
                "setShift": {"rangeOut": [0, 1000]}
            }
        )

    @mapArgs
    def setShift(self, freq):
        """
        Set FreqShift frequency shift

        Params:
        freq : float [0..1000]
           Frequency shifting value
        """
        logging.info("Set '%s' FreqShift frequency shifting value 'shift' to %s" % (
            self.nodeName, freq))
        logging.debug("%s.setShift(%s)" % (self.nodeName, freq))
        pyo.FreqShift.setShift(self, freq)


class WaveGuide(Effect, pyo.AllpassWG):
    """Specialized effect as AllpassWG"""

    def __init__(self, name, parent, input=audioInputs[0]):
        """AllpassWG constructor"""
        self.freqFactor = pyo.Randi(
            min=.95, max=1.05, freq=[.145, .2002, .1055, .071])
        pyo.AllpassWG.__init__(self, input=input, freq=self.freqFactor*[
                               74.99, 75, 75.01, 75.1], feed=1, detune=pyo.Randi(min=.5, max=1.0, freq=[.022, .13, .155, .171]))
        Effect.__init__(self, name, parent, input)
        pyo.AllpassWG.setInput(self, self.in_fader)

        self.exposed_to_osc.update(
            {
                "setFreq": {"rangeOut": [0, 10000], "scale": "cub"}
            }
        )

    @mapArgs
    def setFreq(self, factor):
        """Set frequency factor to drive harmonics

        Params:
        factor : float [0..10000]
           Frequency factor value
        """
        logging.info("Set '%s' AllpassWG frequency factor value to '%s'" %
                     (self.nodeName, factor))
        logging.debug("%s.setFreq(%s)" % (self.nodeName, factor))
        self.freqFactor = pyo.Randi(min=.95, max=1.05, freq=[
                                    factor*.145, factor*.2002, factor*.1055, factor*.071])
        pyo.AllpassWG.setFreq(self, self.freqFactor*[74.99, 75, 75.01, 75.1])


class EffectChain(OscNode, pyo.PyoObject):
    """Contains multiple effects and manage their order"""

    def __init__(self, name, parent, children=None, order=None, input=audioInputs[0]):
        """
        EffectChain constructor
        """
        OscNode.__init__(self, name, parent, children)
        pyo.PyoObject.__init__(self)

        self.effectClasses = {
            "Disto": Disto,
            "Freeverb": Freeverb,
            "FreqShift": FreqShift,
            "WaveGuide": WaveGuide
        }

        self.order = order if order is not None else []
        self.in_fader = pyo.InputFader(input)

        self.out_fader = pyo.InputFader(audioInputs[0])
        self._base_objs = self.out_fader.getBaseObjects()

    def setInput(self, newInput):
        """
        Set Chain's input

        Params:
        newInput : PyoObject
        """
        logging.debug("Set '%s' audio input signal 'input' to %s" %
                      (self.nodeName, newInput))
        self.in_fader.setInput(newInput)

    def addEffect(self, name, effectType):
        """
        Add an Effect object to the chain

        Params:
        name : str
        effectType : str
        """
        logging.debug("Parent '%s' wants a new child effect '%s' named '%s'" % (
            self.nodeName, effectType, name))
        if effectType in self.effectClasses.keys():
            self.addChild(self.effectClasses[effectType](name, self))
            self.order.append(name)
            self.refreshPatch()

    def removeEffect(self, name):
        """
        Remove an Effect object from the chain

        Params:
        name : name
        """
        if name in self.children.keys():
            logging.info("Remove from '%s' effect '%s'" %
                         (self.nodeName, name))
            del self.children[name]
            del self.order[self.order.index(name)]
            self.refreshPatch()

    def setOrder(self, *newOrder):
        """
        Set a new patch order for the effects in the chain

        Params:
        *newOrder : multiple args (str)
        """
        logging.info("Set '%s' chain order to '%s'" %
                     (self.nodeName, newOrder))
        self.order = newOrder
        self.refreshPatch()

    def refreshPatch(self):
        """
        Set the effect's inputs according to the chain's order
        Special cases:
        First effect's input = chainInput
        Chain's Mix (self) must replace his input with the chain's last effect
        """
        logging.debug("Refresh '%s' effect chain patch" % (self.nodeName))
        previousStream = self.in_fader
        cursor = 0
        for item in self.order:
            if item in self.children.keys():
                if cursor == 0:
                    self.children[item].setInput(previousStream)
                else:
                    self.children[item].setInput(previousStream.getOut())

                cursor += 1
                previousStream = self.children[item]

        if previousStream != self.in_fader:
            self.out_fader.setInput(previousStream.getOut())

    def play(self, dur=0, delay=0):
        """Start processing without sending samples to output. This method is called automatically at the object creation.

        This method returns self, allowing it to be applied at the object creation.

        Params:
        dur : float
        Duration, in seconds, of the object’s activation. The default is 0 and means infinite duration.

        delay : float
        Delay, in seconds, before the object’s activation. Defaults to 0.
        """
        self.out_fader.play(dur, delay)
        return pyo.PyoObject.play(self, dur, delay)

    def stop(self):
        """Stop processing.

        This method returns self, allowing it to be applied at the object creation.
        """
        self.out_fader.stop()
        return pyo.PyoObject.stop(self)

    def out(self, chnl=0, inc=1, dur=0, delay=0):
        """Start processing and send samples to audio output beginning at chnl.

        This method returns self, allowing it to be applied at the object creation.

        Params:
        chnl : int
        Physical output assigned to the first audio stream of the object. Defaults to 0.

        inc : int
        Output channel increment value. Defaults to 1.

        dur : float
        Duration, in seconds, of the object’s activation. The default is 0 and means infinite duration.

        delay : float
        Delay, in seconds, before the object’s activation. Defaults to 0.
        """
        self.out_fader.play(dur, delay)
        return pyo.PyoObject.out(self, chnl, inc, dur, delay)


if __name__ == "__main__":
    oneEffect = FreqShift("freqshiftTest", None)
    oneEffect.setInput(audioInputs[1])
    oneEffect.setWet(.8)
    oneEffect.ctrl()
    oneEffect.out()

    oneChain = EffectChain("chainTest", None)
    oneChain.setInput(audioInputs[1])
    oneChain.addEffect("fatDisto", "Disto")
    oneChain.children["fatDisto"].ctrl()
    oneChain.addEffect("fatVerb", "Freeverb")
    oneChain.children["fatVerb"].ctrl()
    oneChain.setOrder("fatVerb", "fatDisto")
    oneChain.out()

    from chainsaw.osc import OscRootNode
    from chainsaw.configuration import commandLine
    oscRouter = OscRootNode("effect", oscPort=commandLine.port)
    oscRouter.addChild(oneEffect)
    oscRouter.addChild(oneChain)
    oscSender = pyo.OscDataSend(
        "sf", commandLine.port, "/effect/chainTest/fatDisto")
    oscSender.send(["setWet", 1])
    oscSender = pyo.OscDataSend(
        "sf", commandLine.port, "/effect/chainTest/fatVerb")
    oscSender.send(["setWet", 1])
    oscSender = pyo.OscDataSend(
        "sf", commandLine.port, "/effect/chainTest/fat*")
    oscSender.send(["setWet", .5])
    oscSender = pyo.OscDataSend("sf", commandLine.port, "/effect/*/*")
    oscSender.send(["setWet", .2])
    oscSender = pyo.OscDataSend(
        "sf", commandLine.port, "/effect/fre[Qq]shi?tTest")
    oscSender.send(["setWet", 1])

    from chainsaw.configuration import audioServer
    audioServer.start()
    audioServer.gui(locals())
