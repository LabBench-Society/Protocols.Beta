
class OffsetAnalgesia:
   def __init__(self, tc, intensity, duration):
      self.tc = tc
      self.PreDuration = duration[0]
      self.StimulusDuration = duration[1]
      self.PostDuration = duration[2]
      self.Intensity = intensity

   def Duration(self):
      return self.PreDuration + self.StimulusDuration + self.PostDuration

   def Stimulate(self, sr):
      cpar = self.tc.Instruments.PressureAlgometer
      channel = cpar.Channels[0]

      PDT = sr.PDT
      PTT = sr.PTT

      CondIntensity = self.tc.CondPressure * (PTT - PDT) + PDT

      channel.SetStimulus(1, channel.CreateWaveform()
                        .Step(CondIntensity,self.PreDuration)
                        .Step(self.Intensity * PTT,self.StimulusDuration)
                        .Step(CondIntensity,self.PostDuration))
      cpar.ConfigurePressureOutput(0, cpar.ChannelIDs.CH01)
      cpar.ConfigurePressureOutput(1, cpar.ChannelIDs.NoChannel)
      cpar.StartStimulation(cpar.StopCriterions.WhenButtonPressed, True)

      return True

   def Control(self, sr):
      cpar = self.tc.Instruments.PressureAlgometer
      channel = cpar.Channels[0]

      PDT = sr.PDT
      PTT = sr.PTT

      CondIntensity = self.tc.CondPressure * (PTT - PDT) + PDT

      channel.SetStimulus(1, channel.CreateWaveform()
                        .Step(CondIntensity,self.PreDuration)
                        .Step(CondIntensity,self.StimulusDuration)
                        .Step(CondIntensity,self.PostDuration))
      cpar.ConfigurePressureOutput(0, cpar.ChannelIDs.CH01)
      cpar.ConfigurePressureOutput(1, cpar.ChannelIDs.NoChannel)
      cpar.StartStimulation(cpar.StopCriterions.WhenButtonPressed, True)

      return True
   
def CreateThresholdVersion(tc):
   return OffsetAnalgesia(tc, 1, [5, 2, 5])

def Stop(tc):
   cpar = tc.Instruments.PressureAlgometer
   cpar.StopStimulation()
   return True

def Sample(tc):
   cpar = tc.Instruments.PressureAlgometer
   return [cpar.Pressure[0]]
