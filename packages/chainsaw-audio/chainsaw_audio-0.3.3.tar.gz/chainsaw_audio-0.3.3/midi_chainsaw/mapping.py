""" Routing configuration for the BCF2000 """
route = {}
for i in range(1, 3):
    route[i] = {
        10: {
            "/chainsaw/instruments/"+str(i)+"/looperTrack": {
                "setMul": ["!"]
            }
        },
        11: {
            "/chainsaw/instruments/"+str(i)+"/looperTrack": {
                "setStart": ["!"]
            }
        },
        12: {
            "/chainsaw/instruments/"+str(i)+"/looperTrack": {
                "setMulController": ["!"]
            }
        },
        13: {
            "/chainsaw/instruments/"+str(i)+"/looperTrack": {
                "setFreqController": ["!"]
            }
        },
        14: {
            "/chainsaw/instruments/"+str(i)+"/looperTrack": {
                "setSharpController": ["!"]
            }
        },
        15: {
            "/chainsaw/instruments/"+str(i): {
                "snapShot": []
            }
        },
        16: {
            "/chainsaw/instruments/"+str(i)+"/looperTrack": {
                "togglePlay": ["!"]
            }
        },
        20: {
            "/chainsaw/Monitor": {
                "setMul": ["!"]
            }
        },
        21: {
            "/chainsaw/instruments/"+str(i)+"/looperTrack": {
                "setDur": ["!"]
            }
        },
        22: {
            "/chainsaw/instruments/"+str(i)+"/looperTrack": {
                "setCenterController": ["!"]
            }
        },
        23: {
            "/chainsaw/instruments/"+str(i)+"/looperTrack": {
                "setShapeController": ["?"]
            }
        },
        24: {
            "/chainsaw/instruments/"+str(i)+"/looperTrack": {
                "setMode": ["?"]
            }
        },
        25: {
            "/chainsaw/instruments/"+str(i): {
                "debug": ["Unnused button, value: ", "?"]
            }
        },
        26: {
            "/chainsaw/instruments/"+str(i)+"/looperTrack": {
                "setMonitor": ["!"]
            }
        },
        # Effect Chain for looperTrack
        30: {
            "/chainsaw/instruments/"+str(i)+"/looperTrack": {
                "setWet": ["!"]
            }
        },
        ## Disto
        31: {
            "/chainsaw/instruments/"+str(i)+"/looperTrack/chain/disto": {
                "setDrive": ["!"]
            }
        },
        41: {
            "/chainsaw/instruments/"+str(i)+"/looperTrack/chain/disto": {
                "setWet": ["!"]
            }
        },
        ## Freeverb
        32: {
            "/chainsaw/instruments/"+str(i)+"/looperTrack/chain/freeverb": {
                "setSize": ["!"]
            }
        },
        42: {
            "/chainsaw/instruments/"+str(i)+"/looperTrack/chain/freeverb": {
                "setWet": ["!"]
            }
        },
        ## FreqShift
        33: {
            "/chainsaw/instruments/"+str(i)+"/looperTrack/chain/freqshift": {
                "setShift": ["!"]
            }
        },
        43: {
            "/chainsaw/instruments/"+str(i)+"/looperTrack/chain/freqshift": {
                "setWet": ["!"]
            }
        },
        ## WaveGuide
        34: {
            "/chainsaw/instruments/"+str(i)+"/looperTrack/chain/waveguide": {
                "setFreq": ["!"]
            }
        },
        44: {
            "/chainsaw/instruments/"+str(i)+"/looperTrack/chain/waveguide": {
                "setWet": ["!"]
            }
        },

        50: {
            "/chainsaw/instruments/"+str(i)+"/particleTrack": {
                "setMul": ["!"]
            }
        },
        51: {
            "/chainsaw/instruments/"+str(i)+"/particleTrack": {
                "setPos": ["!"]
            }
        },
        52: {
            "/chainsaw/instruments/"+str(i)+"/particleTrack": {
                "setMulController": ["!"]
            }
        },
        53: {
            "/chainsaw/instruments/"+str(i)+"/particleTrack": {
                "setFreqController": ["!"]
            }
        },
        54: {
            "/chainsaw/instruments/"+str(i)+"/particleTrack": {
                "setDev": ["!"]
            }
        },
        55: {
            "/chainsaw/instruments/"+str(i): {
                "snapShot": []
            }
        },
        56: {
            "/chainsaw/instruments/"+str(i)+"/particleTrack": {
                "togglePlay": ["!"]
            }
        },

        60: {
            "/chainsaw/instruments/"+str(i)+"/particleTrack": {
                "setDens": ["!"]
            }
        },
        61: {
            "/chainsaw/instruments/"+str(i)+"/particleTrack": {
                "setDur": ["!"]
            }
        },
        62: {
            "/chainsaw/instruments/"+str(i)+"/particleTrack": {
                "setCenterController": ["!"]
            }
        },
        63: {
            "/chainsaw/instruments/"+str(i)+"/particleTrack": {
                "setShapeController": ["?"]
            }
        },
        64: {
            "/chainsaw/instruments/"+str(i)+"/particleTrack": {
                "setEnv": ["?"]
            }
        },
        65: {
            "/chainsaw/instruments/"+str(i): {
                "debug": ["Unnused button, value: ", "?"]
            }
        },
        66: {
            "/chainsaw/instruments/"+str(i)+"/particleTrack": {
                "setMonitor": ["!"]
            }
        },

        # Effect Chain for particleTrack
        70: {
            "/chainsaw/instruments/"+str(i)+"/particleTrack": {
                "setWet": ["!"]
            }
        },
        ## Disto
        71: {
            "/chainsaw/instruments/"+str(i)+"/particleTrack/chain/disto": {
                "setDrive": ["!"]
            }
        },
        81: {
            "/chainsaw/instruments/"+str(i)+"/particleTrack/chain/disto": {
                "setWet": ["!"]
            }
        },
        ## Freeverb
        72: {
            "/chainsaw/instruments/"+str(i)+"/particleTrack/chain/freeverb": {
                "setSize": ["!"]
            }
        },
        82: {
            "/chainsaw/instruments/"+str(i)+"/particleTrack/chain/freeverb": {
                "setWet": ["!"]
            }
        },
        ## FreqShift
        73: {
            "/chainsaw/instruments/"+str(i)+"/particleTrack/chain/freqshift": {
                "setShift": ["!"]
            }
        },
        83: {
            "/chainsaw/instruments/"+str(i)+"/particleTrack/chain/freqshift": {
                "setWet": ["!"]
            }
        },
        ## WaveGuide
        74: {
            "/chainsaw/instruments/"+str(i)+"/particleTrack/chain/waveguide": {
                "setFreq": ["!"]
            }
        },
        84: {
            "/chainsaw/instruments/"+str(i)+"/particleTrack/chain/waveguide": {
                "setWet": ["!"]
            }
        }
    }
