from Serilog import Log
from LabBench.Interface.Instruments.Algometry import *

def Condition(tc):
    algometer = tc.Instruments.PressureAlgometer
    chan = algometer.Channels[0]

    chan.SetStimulus(1, chan.CreateWaveform().Step(tc.SR02.PTT*0.70, 9.9 * 60))
    algometer.ConfigurePressureOutput(0, ChannelID.NONE)
    algometer.ConfigurePressureOutput(1, ChannelID.CH01)
    algometer.StartStimulation(AlgometerStopCriterion.STOP_CRITERION_ON_BUTTON_PRESSED, True)

    Log.Information("Starting conditioning: {intensity}", tc.SR02.PTT * 0.70)

    return True

def Stop(tc):
    algometer = tc.Devices.PressureAlgometer
    algometer.StopStimulation()

    return True