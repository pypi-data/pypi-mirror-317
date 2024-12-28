"""
Route patch dictionnary, must be of this form:
    route = {
        control_change_number: {
            "/osc/address": {
                "method_name": [arg1, args2, "!"],
                "method_name2": ["?"],
                "triggered_method_name3": []
            }
        }
    }

Where:
    "!" will be replaced by the cc's value normalized between 0 and 1
    "?" will be replaced by the cc's value (not normalized)
    If argument list is empty, method is considered as a TRIGGER
"""
route = {
    10: {
        "/chainsaw/instrument/looperTrack": {
            "setMul": ["!"]
        }
    },
    11: {
        "/chainsaw/instrument/looperTrack": {
            "setStart": ["!"]
        }
    },
    12: {
        "/chainsaw/instrument/looperTrack": {
            "setMulController": ["!"]
        }
    },
    13: {
        "/chainsaw/instrument/looperTrack": {
            "setFreqController": ["!"]
        }
    },
    14: {
        "/chainsaw/instrument/looperTrack": {
            "setSharpController": ["!"]
        }
    },
    15: {
        "/chainsaw/instrument": {
            "snapShot": []
        }
    },
    16: {
        "/chainsaw/instrument/looperTrack": {
            "setPlay": ["!"]
        }
    },
    20: {
        "/chainsaw/instrument/Monitor": {
            "setMul": ["!"]
        }
    },
    21: {
        "/chainsaw/instrument/looperTrack": {
            "setDur": ["!"]
        }
    },
    22: {
        "/chainsaw/instrument/looperTrack": {
            "setCenterController": ["!"]
        }
    },
    23: {
        "/chainsaw/instrument/looperTrack": {
            "setShapeController": ["?"]
        }
    },
    24: {
        "/chainsaw/instrument/looperTrack": {
            "setMode": ["?"]
        }
    },
    25: {
        "/chainsaw/instrument": {
            "debug": ["Unnused button, value: ","?"]
        }
    },
    26: {
        "/chainsaw/instrument/looperTrack": {
            "setMonitor": ["!"]
        }
    },
    # Effect Chain for looperTrack
    30: {
        "/chainsaw/instrument/looperTrack": {
            "setWet": ["!"]
        }
    },
    ## Disto
    31: {
        "/chainsaw/instrument/looperTrack/chain/disto": {
            "setDrive": ["!"]
        }
    },
    41: {
        "/chainsaw/instrument/looperTrack/chain/disto": {
            "setWet": ["!"]
        }
    },
    ## Freeverb
    32: {
        "/chainsaw/instrument/looperTrack/chain/freeverb": {
            "setSize": ["!"]
        }
    },
    42: {
        "/chainsaw/instrument/looperTrack/chain/freeverb": {
            "setWet": ["!"]
        }
    },
    ## FreqShift
    33: {
        "/chainsaw/instrument/looperTrack/chain/freqshift": {
            "setShift": ["!"]
        }
    },
    43: {
        "/chainsaw/instrument/looperTrack/chain/freqshift": {
            "setWet": ["!"]
        }
    },
    ## WaveGuide
    34: {
        "/chainsaw/instrument/looperTrack/chain/waveguide": {
            "setFreq": ["!"]
        }
    },
    44: {
        "/chainsaw/instrument/looperTrack/chain/waveguide": {
            "setWet": ["!"]
        }
    },
    50: {
        "/chainsaw/instrument/particleTrack": {
            "setMul": ["!"]
        }
    },
    51: {
        "/chainsaw/instrument/particleTrack": {
            "setPos": ["!"]
        }
    },
    52: {
        "/chainsaw/instrument/particleTrack": {
            "setMulController": ["!"]
        }
    },
    53: {
        "/chainsaw/instrument/particleTrack": {
            "setFreqController": ["!"]
        }
    },
    54: {
        "/chainsaw/instrument/particleTrack": {
            "setDev": ["!"]
        }
    },
    55: {
        "/chainsaw/instrument": {
            "snapShot": []
        }
    },
    56: {
        "/chainsaw/instrument/particleTrack": {
            "setPlay": ["!"]
        }
    },
    60: {
        "/chainsaw/instrument/particleTrack": {
            "setDens": ["!"]
        }
    },
    61: {
        "/chainsaw/instrument/particleTrack": {
            "setDur": ["!"]
        }
    },
    62: {
        "/chainsaw/instrument/particleTrack": {
            "setCenterController": ["!"]
        }
    },
    63: {
        "/chainsaw/instrument/particleTrack": {
            "setShapeController": ["?"]
        }
    },
    64: {
        "/chainsaw/instrument/particleTrack": {
            "setEnv": ["?"]
        }
    },
    65: {
        "/chainsaw/instrument": {
            "debug": ["Unnused button, value: ","?"]
        }
    },
    66: {
        "/chainsaw/instrument/particleTrack": {
            "setMonitor": ["!"]
        }
    },
    # Effect Chain for particleTrack
    70: {
        "/chainsaw/instrument/particleTrack": {
            "setWet": ["!"]
        }
    },
    ## Disto
    71: {
        "/chainsaw/instrument/particleTrack/chain/disto": {
            "setDrive": ["!"]
        }
    },
    81: {
        "/chainsaw/instrument/particleTrack/chain/disto": {
            "setWet": ["!"]
        }
    },
    ## Freeverb
    72: {
        "/chainsaw/instrument/particleTrack/chain/freeverb": {
            "setSize": ["!"]
        }
    },
    82: {
        "/chainsaw/instrument/particleTrack/chain/freeverb": {
            "setWet": ["!"]
        }
    },
    ## FreqShift
    73: {
        "/chainsaw/instrument/particleTrack/chain/freqshift": {
            "setShift": ["!"]
        }
    },
    83: {
        "/chainsaw/instrument/particleTrack/chain/freqshift": {
            "setWet": ["!"]
        }
    },
    ## WaveGuide
    74: {
        "/chainsaw/instrument/particleTrack/chain/waveguide": {
            "setFreq": ["!"]
        }
    },
    84: {
        "/chainsaw/instrument/particleTrack/chain/waveguide": {
            "setWet": ["!"]
        }
    }
}
