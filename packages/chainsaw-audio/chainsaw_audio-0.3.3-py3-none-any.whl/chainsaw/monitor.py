from chainsaw.osc import OscNode
from chainsaw.utils import mapArgs
import pyo


class MonitorManager(OscNode, pyo.Mixer):
    """
    Monitors Manager
    """

    def __init__(self, name, chnl):
        OscNode.__init__(self, name)
        pyo.Mixer.__init__(self, outs=1, chnls=1)
        pyo.Mixer.out(self, chnl)

        self.exposed_to_osc.update(
            {
                "setMul": {"scale": "sqr"}
            }
        )

    def addInput(self, input):
        key = pyo.Mixer.addInput(self, None, input)
        self.setAmp(key, 0, 1)

    @mapArgs
    def setMul(self, mul):
        pyo.Mixer.setMul(self, mul)
