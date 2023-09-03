from Serilog import Log
from LabBench.Interface.Instruments.Algometry import *

def Stimulate(tc, x):
    algometer = tc.Devices.Algometer
    chan = algometer.Channels[0]

    chan.SetStimulus(1, chan.CreateWaveform()
                     .Step(x, 1))
    algometer.ConfigurePressureOutput(0, ChannelID.CH01)
    algometer.StartStimulation(AlgometerStopCriterion.STOP_CRITERION_ON_BUTTON_PRESSED, True)

    return True