# -*- coding: utf-8 -*-
"""Configuration module to share data globally inside pyoChainsaw"""
import time
import pyo
import chainsaw.cli as cli
from chainsaw.monitor import MonitorManager

"""
Parse CLI arguments
"""
commandLine = cli.CLI().performParsingCLI()

if commandLine.listPortaudioDevices:
    pyo.pa_list_devices()
    exit(0)


"""
Instanciate the audio server
Once the pyo.Server is booted, whatever signal can
be added to the global stream.
"""
jackname = "{!s}-{!s}".format(commandLine.jackname, commandLine.port)
audioServer = pyo.Server(audio=commandLine.audio,
                         sr=commandLine.samplingRate,
                         jackname=jackname,
                         ichnls=1,
                         nchnls=2)  # + 1 for monitoring
pyoVerbosityMapping = {
    'DEBUG': 8,
    'INFO': 4,
    'WARNING': 2,
    'ERROR': 1,
    'CRITICAL': 1,
}
audioServer.setVerbosity(pyoVerbosityMapping[commandLine.logLevel])
audioServer.deactivateMidi()

if commandLine.audio == "portaudio":
    audioServer.setInOutDevice(commandLine.portaudioDevice)
elif commandLine.audio == "jack":
    audioServer.setJackAuto(xin=False, xout=False)

audioServer.boot()
loop = 0
while not audioServer.getIsBooted():
    time.sleep(0.2)
    if loop < 100:
        loop += 1
    else:
        print("Audio server can't be booted")
        exit(33)

"""
Construct a tuple containing the input audio stream
"""
audioInputs = (pyo.Sig(0), pyo.Input(0))  # Set to tuple to avoid mutation


"""
Base Envelopes
"""
envelopes = [
    pyo.ChebyTable(),
    pyo.CosLogTable(),
    pyo.CosTable(),
    pyo.CurveTable(),
    pyo.ExpTable(),
    pyo.HannTable(),
    pyo.HarmTable(),
    pyo.LinTable(),
    pyo.LogTable(),
    pyo.ParaTable(),
    pyo.PartialTable(),
    pyo.SawTable(),
    pyo.SincTable(),
    pyo.SquareTable(),
    pyo.AtanTable()
]

"""
Monitors Manager
"""
monitorManager = MonitorManager('Monitor', audioServer.getNchnls() - 1)
