from Serilog import Log
from LabBench.Interface.Instruments.Algometry import *

def Condition(tc):
    algometer = tc.Devices.PressureAlgometer
    chan = algometer.Channels[0]

    chan.SetStimulus(1, chan.CreateWaveform()
                     .Step(tc.SR.PTT*0.70, 9.9 * 60))
    algometer.ConfigurePressureOutput(0, ChannelID.CH01)
    algometer.StartStimulation(AlgometerStopCriterion.STOP_CRITERION_ON_BUTTON_PRESSED, True)

    Log.Information("Starting conditioning: {intensity}", tc.SR.PTT)

    return True

def Stop(tc):
    algometer = tc.Devices.Algometer
    algometer.StopStimulation()

    return True