# -*- coding: utf-8 -*-
""" This module supply everything's related to instruments."""

import logging
import pyo
from chainsaw.configuration import audioInputs, audioServer, commandLine
from chainsaw.osc import OscNode
from chainsaw.tracks import LooperTrack, ParticleTrack


class Instrument(OscNode, pyo.PyoObject):
    """
    An Instrument is a double track container that hold a LooperTrack and a ParticleTrack
    """

    def __init__(self, name, instrumentInput=audioInputs[1], autoNormalize=True):
        """
        Instrument constructor

        Params:
        name : self
        Instrument name that also define its OSC nodeName.

        instrumentInput : pyo.Input
        The qualified pyo.Input input, or the '0 signaled' global Input as default.

        Doctest:
        >>> i = Instrument('testInstrument')
        >>> i.in_fader is not None
        True
        >>> i.nodeName == 'testInstrument'
        True
        >>> i = Instrument('testInstrument')
        >>> i.nodeName == 'somethingWrong'
        False
        >>> del i
        """
        logging.debug("Creating instrument node named '%s'" % (name))
        OscNode.__init__(self, name)
        pyo.PyoObject.__init__(self)

        self.duration = commandLine.length
        self.in_fader = pyo.InputFader(instrumentInput)
        self.liveBuffer = pyo.NewTable(
            length=self.duration, chnls=1, feedback=0)
        self.recorder = pyo.TableFill(
            input=self.in_fader, table=self.liveBuffer)
        self.fixedBuffer = pyo.NewTable(length=self.liveBuffer.getLength())
        self.setAutoNormalize(autoNormalize)

        self.addChild(LooperTrack("looperTrack", self.fixedBuffer, self))
        self.addChild(ParticleTrack("particleTrack", self.fixedBuffer, self))

        self.out_fader = self.children["looperTrack"].getOut(
        ) + self.children["particleTrack"].getOut()
        self._base_objs = self.out_fader.getBaseObjects()

        self.exposed_to_osc.update(
            {"snapShot": {},
             "togglePlay": {},
             "setPlay": {},
             }
        )

        logging.debug("New instrument named '%s' created with auto normalization '%s'" % (
            name, "on" if self.autoNormalize else "off"))

    def __del__(self):
        """Destructor called when still no reference to object

        See: https://docs.python.org/2/reference/datamodel.html#object.__del__
        """
        logging.info("'%s' Instrument is dying!" % (self.nodeName))

    def view(self):
        """Show something relevant to current instrument, particularly its wavetable"""
        self.fixedBuffer.view(title=commandLine.jackname +
                              " (" + str(commandLine.port) + ")")

    def refreshFixedBuffer(self):
        """
        Update the fixedBuffer buffer with the last live recorded table liveBuffer

        Return:
        True while everything's good
        False otherwise

        Doctest:
        >>> i = Instrument('testInstrument')
        >>> i.in_fader is not None
        True
        >>> i.nodeName == 'testInstrument'
        True
        """
        logging.info("Snapshot the '%s' liveBuffer" % (self.nodeName))
        rotatePosition = int(self.recorder.getCurrentPos())
        logging.debug("Snapshot rotate position for '%s' : %s samples (eq: %s sec)"
                      % (self.nodeName,
                         rotatePosition,
                         rotatePosition / self.getSamplingRate()))
        self.fixedBuffer.copyData(table=self.liveBuffer)
        logging.debug(
            "Dump '%s' liveBuffer to fixedBuffer with 'copyData'" % (self.nodeName))
        self.fixedBuffer.rotate(rotatePosition)
        logging.debug("Rotate '%s' fixedBuffer at %s samples" %
                      (self.nodeName, rotatePosition))
        if self.autoNormalize:
            self.fixedBuffer.normalize()

    def snapShot(self):
        """Wrapper to refreshFixedBuffer"""
        self.refreshFixedBuffer()

    def setAutoNormalize(self, value=True):
        """Define the auto normalization flag

        Params:
        value : bool
        Th flag vaue. Default to True.
        """
        self.autoNormalize = True if value is None else value

    def setInput(self, newInput, fadetime=0.05):
        """
        Set the Instrument input to another one

        Params:
        newInput : pyo.PyoObject or int
        New input to use for live recording.
        If int, corresponding jack audio input wil be used

        fadetime : float
        Crossfade time between old and new input. Defaults to 0.05.
        """
        logging.debug("Set '%s' audio input signal to '%s'" %
                      (self.nodeName, newInput))
        if isinstance(newInput, int) and newInput in range(len(audioInputs)):
            self.in_fader.setInput(audioInputs[newInput], float(fadetime))
        elif isinstance(newInput, pyo.PyoObject) or hasattr(newInput, "stream"):
            self.in_fader.setInput(newInput, float(fadetime))

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
        logging.info("Instrument '%s' sends its signal to output #%s" %
                     (self.nodeName, chnl))
        self.out_fader.play(dur, delay)
        return pyo.PyoObject.out(self, chnl, inc, dur, delay)

    def togglePlay(self):
        """
        Toggle Intrument's state between [playing] and [stopped] based on current state
        """
        if self.isPlaying():
            self.stop()
        else:
            self.play()

    def setPlay(self, play=False):
        """
        Set Intrument's state between [playing] and [stopped]
        """
        if play:
            self.play()
        else:
            self.stop()


if __name__ == "__main__":
    import doctest
    fails, total = doctest.testmod(verbose=True)
    if total > 0 and fails == 0:
        instrument = Instrument("1")
        patLive = pyo.Pattern(instrument.liveBuffer.refreshView, 0.05).play()
        patFixed = pyo.Pattern(instrument.fixedBuffer.refreshView, 0.05).play()
        instrument.liveBuffer.view()
        instrument.fixedBuffer.view()
        audioServer.start()
        audioServer.gui(locals())
