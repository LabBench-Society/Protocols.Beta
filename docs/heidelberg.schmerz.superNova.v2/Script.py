def StimulateSES01(tc):
    return _stimulate(tc, tc.SES01NDLEG.PTT, tc.SES01CPM.RunningTime)

def StimulateSES02(tc):
    return _stimulate(tc, tc.SES02NDLEG.PTT, tc.SES02CPM.RunningTime)

def _stimulate(tc, ptt, running_time):
    algometer = tc.Instruments.PressureAlgometer
    display = tc.Instruments.ImageDisplay
    intensity = 0.7 * ptt
    time = 110 - running_time

    chan = algometer.Channels[0]
    chan.SetStimulus(1, chan.CreateWaveform().Step(intensity, time))
    chan = algometer.Channels[1]
    chan.SetStimulus(1, chan.CreateWaveform())

    algometer.ConfigurePressureOutput(0, algometer.ChannelIDs.NoChannel)
    algometer.ConfigurePressureOutput(1, algometer.ChannelIDs.CH01)

    algometer.StartStimulation(algometer.StopCriterions.WhenButtonPressed, True, False)
    tc.Log.Information("STIMULATION STARTED [ Intensity: {intensity}, Time: {time}]", intensity, time)

    display.Display(tc.Assets.CPAInstructions.COND)
    return True

def ConditioningTimeSES01(tc):
    return _conditioning_time(tc, tc.SES01CPM.RunningTime)

def ConditioningTimeSES02(tc):
    return _conditioning_time(tc, tc.SES02CPM.RunningTime)

def _conditioning_time(tc, running_time):
    try:
        return 110 - running_time + 15
    except Exception:
        return 125


def Stop(tc):
    try:
        tc.Instruments.PressureAlgometer.StopStimulation()
    except:
        pass
    return True
