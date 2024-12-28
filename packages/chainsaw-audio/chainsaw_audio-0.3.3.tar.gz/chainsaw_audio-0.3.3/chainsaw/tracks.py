#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module supply everything about tracks."""

import logging
import pyo
from chainsaw.osc import OscNode
from chainsaw.effects import EffectChain
from chainsaw.configuration import audioServer, envelopes, monitorManager
from chainsaw.utils import mapArgs


class Track(OscNode):
    """A container representing a TableProcessor and an EffectChain

    WARNING: it does not have to be instanced, just inherited"""

    def __init__(self, name, parent=None):
        """Track constructor

        Params:
        name : str
        Track name

        parent : OscNode
        Parent. Default to None
        """
        OscNode.__init__(self, name, parent=parent)

        self.addChild(EffectChain(name="chain", parent=self, input=self))
        self.children["chain"].addEffect("disto", "Disto")
        self.children["chain"].addEffect("freeverb", "Freeverb")
        self.children["chain"].addEffect("freqshift", "FreqShift")
        self.children["chain"].addEffect("waveguide", "WaveGuide")
        self.children["chain"].setOrder(
            "disto", "freeverb", "freqshift", "waveguide")

        self.chainWetLevel = pyo.Sig(0)
        self.centerController = pyo.Sig(0)
        self.controller = pyo.LFO(freq=0,
                                  mul=1 - self.centerController,
                                  add=self.centerController
                                  )

        self.exposed_to_osc.update(
            {
                "togglePlay": {},
                "setPlay": {},
                "setMul": {"rangeOut": [0, 1], "scale": "sqr"},
                "setWet": {"scale": "sqr"},
                "setMulController": {},
                "setCenterController": {},
                "setFreqController": {"rangeOut": [0, 100], "scale": "cub"},
                "setShapeController": {"rangeIn": [0, 7], "resolution": "int"},
                "setSharpController": {},
                "setMonitor": {}
            }
        )

        self.out_fader = self * (1 - self.chainWetLevel) + \
            self.children["chain"] * self.chainWetLevel
        self.monitor_out = self * \
            (1 - self.chainWetLevel) + \
            self.children["chain"] * self.chainWetLevel
        monitorManager.addInput(input=self.monitor_out)
        self.setPlay(False)
        self.setMul(self.exposed_to_osc["setMul"]["rangeOut"][0])
        self.setWet(0)
        self.setMulController(0)
        self.setCenterController(1)
        self.setFreqController(
            self.exposed_to_osc["setFreqController"]["rangeOut"][0])
        self.setShapeController(
            self.exposed_to_osc["setShapeController"]["rangeIn"][0])
        self.setSharpController(0)
        self.setMonitor(0)

    @mapArgs
    def setMonitor(self, mul):
        """(De)Activate monitoring for this Track

        In facts, it sets quantity sent to the Monitor mixer output.

        Params:
        mul : float
        0 is for deactivate
        1 is for activate
        """
        prefix = "Un-" if int(mul) == 0 else ""
        logging.debug(prefix + "Monitor track '" + self.nodeName + "'")
        self.monitor_out.setMul(mul)

    def getOut(self):
        """Return the output object that contain signal"""
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
        logging.debug("Plays and outputs %s to out:%s with duration:%s and delay:%s" % (
            self.nodeName, chnl, dur, delay))
        self.out_fader.out(chnl, inc, dur, delay)

    def togglePlay(self):
        """
        Toggle Track's state between [playing] and [stopped]
        based on the current playing state
        """
        if self.isPlaying():
            self.stop()
        else:
            self.play()

    def setPlay(self, play=False):
        """
        Set Track's state between [playing] and [stopped]
        """
        if play:
            self.play()
        else:
            self.stop()

    def setController(self, newController):
        """Replace existing controller with a new given one

        This method HAS TO BE OVERRIDEN to comply with subclass controller usage implementation
        """
        if newController is not None:
            logging.debug("Set '%s' controller as %s" %
                          (self.nodeName, newController))
            self.controller = newController
            self.controller.setMul(1 - self.centerController)
            self.controller.setAdd(self.centerController)

    @mapArgs
    def setMul(self, mul):
        """Set the Track multiplication factor through the method mapping (see self.exposed_to_osc)"""
        logging.debug("Set '%s' multiplication factor 'mul' to %s" %
                      (self.nodeName, mul))
        self.out_fader.setMul(mul)

    @mapArgs
    def setWet(self, chainWetLevel):
        """
        Set wet level (0 = dry = input signal only / 1 = wet = processed signal only)

        Params:
        chainWetLevel : float (between 0 and 1)
        """
        logging.debug("Set '%s' chain wet level 'chainWetLevel' to %s" %
                      (self.nodeName, chainWetLevel))
        self.chainWetLevel.setValue(chainWetLevel)

    @mapArgs
    def setMulController(self, mul):
        """Set the Controller multiplication factor through the method mapping (see self.exposed_to_osc)"""
        if hasattr(self.controller, "setMul"):
            logging.debug(
                "Set '%s' controller multiplication factor 'mul' to %s" % (self.nodeName, mul))
            self.controller.setMul(mul)
        else:
            logging.warning("No 'setMul' for %s controller" %
                            (self.controller))

    @mapArgs
    def setCenterController(self, centerValue):
        """Set the Controller center through the method mapping (see self.exposed_to_osc)"""
        logging.debug("Set '%s' controller center value to %s" %
                      (self.nodeName, centerValue))
        self.centerController.setValue(centerValue)

    @mapArgs
    def setFreqController(self, freq):
        """Set the Controller frequency through the method mapping (see self.exposed_to_osc)"""
        if hasattr(self.controller, "setFreq"):
            logging.debug("Set '%s' controller frequency 'freq' to %s" %
                          (self.nodeName, freq))
            self.controller.setFreq(freq)
        else:
            logging.warning("No 'setFreq' for %s controller" %
                            (self.controller))

    @mapArgs
    def setShapeController(self, shape):
        """Set the Controller waveform type through the method mapping (see self.exposed_to_osc)"""
        if hasattr(self.controller, "setType"):
            logging.debug("Set '%s' controller waveform shape 'type' to %s" % (
                self.nodeName, shape))
            self.controller.setType(shape)
        else:
            logging.warning("No 'setType' for %s controller" %
                            (self.controller))

    @mapArgs
    def setSharpController(self, sharp):
        """Set the Controller sharpness factor through the method mapping (see self.exposed_to_osc)"""
        if hasattr(self.controller, "setSharp"):
            logging.debug("Set '%s' controller sharpness factor 'sharp' to %s" % (
                self.nodeName, sharp))
            self.controller.setSharp(sharp)
        else:
            logging.warning("No 'setSharp' for %s controller" %
                            (self.controller))


class LooperTrack(Track, pyo.Looper):
    """A specialized Track and pyo.Looper"""

    def __init__(self, name, table, parent=None, controller=None):
        """LooperTrack constructor

        Params:
        name : str
        Object name

        table : pyo.NewTable
        Input table to be read

        parent : OscNode
        LooperTrack parent that supply OSC commands
        """
        pyo.Looper.__init__(self,
                            table=table,
                            pitch=1,
                            start=0,
                            dur=1.0,
                            xfade=1,  # 1% of the table time
                            mode=1,  # forward
                            xfadeshape=1,  # equal power
                            startfromloop=False,
                            interp=2,
                            autosmooth=False,
                            mul=1,
                            add=0)
        Track.__init__(self, name, parent=parent)

        self.setController(
            self.controller if controller is None else controller)

        self.exposed_to_osc.update(
            {
                "setStart": {"rangeOut": [0, self.table.length], "scale": "cub"},
                "setDur": {"rangeOut": [0, self.table.length], "scale": "cub"},
                "setMode": {"rangeIn": [1, 3], "resolution": "int"}
            }
        )

        self.setStart(0)
        self.setDur(self.table.length)
        self.setMode(1)

    def setController(self, newController):
        """Replace existing controller with a new given one

        OVERRIDEN to comply with subclass controller usage implementation
        """
        Track.setController(self, newController)
        logging.debug("Set '%s' pitch controller to %s" %
                      (self.nodeName, newController))
        self.setPitch(self.controller)

    @mapArgs
    def setStart(self, position):
        """Mapped wrapper to pyo.Looper.setStart()

        Params:
        position : float
        Starting point, in seconds, of the loop, updated only once per loop cycle.
        """
        logging.debug("Set '%s' LooperTrack start position 'start' to %s seconds" % (
            self.nodeName, position))
        pyo.Looper.setStart(self, position)

    @mapArgs
    def setDur(self, duration):
        """Mapped wrapper to pyo.Looper.setDur()

        Params:
        duration : float
        Duration, in seconds, of the loop, updated only once per loop cycle.
        """
        logging.debug("Set '%s' LooperTrack duration 'dur' to %s seconds" % (
            self.nodeName, duration))
        pyo.Looper.setDur(self, duration)

    @mapArgs
    def setMode(self, mode):
        """
        Loop modes.

        0 = no loop
        1 = forward
        2 = backward
        3 = back-and-forth
        """
        modename = ["no loop", "forward", "backward", "back-and-forth"]
        logging.debug("Set '%s' LooperTrack 'mode' to %s (%s)" %
                      (self.nodeName, mode, modename[mode]))
        pyo.Looper.setMode(self, mode)


class ParticleTrack(Track, pyo.Particle):
    """A specialized Track and pyo.Particle"""

    def __init__(self, name, table, parent=None, controller=None):
        """ParticleTrack constructor

        Params:
        name : str
        Object name

        table : pyo.NewTable
        Input table to be read

        parent : OscNode
        ParticleTrack parent that supply OSC commands
        """
        pyo.Particle.__init__(self,
                              table=table,
                              env=envelopes[5],
                              dens=1,
                              pitch=1,
                              pos=0,
                              dur=0,
                              dev=0.1,
                              pan=0.5,
                              chnls=1
                              )
        Track.__init__(self,
                       name,
                       parent=parent)

        self.setController(
            self.controller if controller is None else controller)

        self.exposed_to_osc.update(
            {
                "setEnv": {"rangeIn": [0, len(envelopes)], "resolution": "int"},
                "setDens": {"rangeOut": [1 / self.table.length, 50], "scale": "cub"},
                "setPos": {"rangeOut": [0, self.table.size], "scale": "cub"},
                "setDur": {"rangeOut": [0, self.table.length-0.00001], "scale": "cub"},
                "setDev": {}
            }
        )

        self.setEnv(0)
        self.setDens(self.exposed_to_osc["setDens"]["rangeOut"][0])
        self.setPos(0.34)
        self.setDur(self.table.length / 16)
        self.setDev(0.24)

    def setController(self, newController):
        """Replace existing controller with a new given one

        OVERRIDEN to comply with subclass controller usage implementation
        """
        Track.setController(self, newController)
        logging.debug("Set '%s' 'pitch' to %s" %
                      (self.nodeName, newController))
        self.setPitch(self.controller)

    @mapArgs
    def setEnv(self, env):
        """Mapped wrapper to pyo.Particle.setEnv()

        Params:
        env : int
        configuration.envelopes[] Index reference to a Table containing the grain envelope

        WARNING: some envelopes make glitches due to their shapes
        See: pyo_0.7.9-doc/api/classes/tables.html
        """
        logging.debug("Set '%s' ParticleTrack envelope 'env' to %s (%s)" % (
            self.nodeName, env, envelopes[env]))
        pyo.Particle.setEnv(self, envelopes[env])

    @mapArgs
    def setDens(self, density):
        """Mapped wrapper to pyo.Particle.setDens()

        Params:
        density : float
        Density of grains per second.
        """
        logging.debug("Set '%s' ParticleTrack density 'dens' to %s" %
                      (self.nodeName, density))
        pyo.Particle.setDens(self, density)

    @mapArgs
    def setPos(self, position):
        """Mapped wrapper to pyo.Particle.setPos()

        Params:
        position : int
        Pointer position, in samples, in the waveform table.
        Each grain sampled the current value of this stream at the beginning
        of its envelope and hold it until the end of the grain.
        """
        logging.debug("Set '%s' ParticleTrack position 'pos' to %s" %
                      (self.nodeName, position))
        pyo.Particle.setPos(self, position)

    @mapArgs
    def setDur(self, duration):
        """Mapped wrapper to pyo.Particle.setDur()

        Params:
        duration : float
        Duration, in seconds, of the grain. Each grain sampled the current value
        of this stream at the beginning of its envelope and hold it until the
        end of the grain.
        """
        logging.debug("Set '%s' ParticleTrack duration 'dur' to %s" %
                      (self.nodeName, duration))
        pyo.Particle.setDur(self, duration)

    @mapArgs
    def setDev(self, deviation):
        """Mapped wrapper to pyo.Particle.setDev()

        Params:
        deviation : float
        Maximum deviation of the starting time of the grain, between 0 and 1 (relative
        to the current duration of the grain).
        Each grain sampled the current value of this stream at the beginning of
        its envelope and hold it until the end of the grain.
        """
        logging.debug("Set '%s' ParticleTrack maximum deviation 'dev' to %s" % (
            self.nodeName, deviation))
        pyo.Particle.setDev(self, deviation)


if __name__ == "__main__":
    from chainsaw.osc import OscRootNode
    from chainsaw.configuration import commandLine
    oscRouter = OscRootNode("tracks", oscPort=commandLine.port)

    table = pyo.SndTable(pyo.SNDS_PATH + "/transparent.aif")
    table.length = table.getDur()  # mimic NewTable length attribute

    particle = ParticleTrack('particle', t)
    oscRouter.addChild(particle)
    particle.play()
    particle.centerController.ctrl(title="particle pitch center")
    # particle.controller.ctrl(title="pitch controller")
    mixer = pyo.Mix(particle, 2).out()

    looper = LooperTrack('looper', t)
    oscRouter.addChild(looper)
    looper.setMulController(.5)
    looper.setFreqController(.5)
    looper.setController(pyo.BrownNoise())
    # Next do not do anything, because there is no Freq attribute in pyo.BrownNoise, but print information
    looper.setFreqController(.5)
    # looper.out()
    # looper.centerController.ctrl()
    # looper.controller.ctrl()
    # looper.ctrl()

    audioServer.start()
    audioServer.gui(locals())
