
class ElectricalOffsetModulation:
   def __init__(self, tc, conditioning, intensity, duration):
      self.tc = tc
      self.duration = duration
      self.intensity = intensity
      self.conditioning = conditioning
      self.currentIntenisity = 0
      self.running = False

   def Duration(self):
      return self.duration[0] + self.duration[1] + self.duration[2] + self.duration[3] + 4

   def UpdateIntensity(self, duration, intensity):
      if not self.running:
         return 1
      
      self.currentIntenisity = intensity
      self.tc.Log.Information("Updating intensity to {}".format(intensity) )

      self.tc.Instruments.Stimulator.Cancel()
      self.tc.Instruments.Stimulator.Generate(self.tc.Stimuli.Repeated(
            self.tc.Stimuli.Arbitrary(lambda t: intensity, 1), 2000, 10))

      return duration

   def Stimulate(self, thr):
      PTT = thr.CH01

      self.running = True
      schedule = self.tc.Scheduler.Create()
      schedule.Add(lambda: self.UpdateIntensity(1000 * self.duration[0], 0))
      schedule.Add(lambda: self.UpdateIntensity(1000 * self.duration[1], PTT * self.conditioning))
      schedule.Add(lambda: self.UpdateIntensity(1000 * self.duration[2], PTT * self.intensity))
      schedule.Add(lambda: self.UpdateIntensity(1000 * self.duration[3], PTT * self.conditioning))
      schedule.Add(lambda: self.UpdateIntensity(5, 0))
      self.tc.Scheduler.Run(schedule)

      return True

   def Control(self, thr):
      PTT = thr.CH01

      self.running = True
      schedule = self.tc.Scheduler.Create()
      schedule.Add(lambda: self.UpdateIntensity(1000 * self.duration[0], 0))
      schedule.Add(lambda: self.UpdateIntensity(1000 * self.duration[1], PTT * self.conditioning))
      schedule.Add(lambda: self.UpdateIntensity(1000 * self.duration[2], PTT * self.conditioning))
      schedule.Add(lambda: self.UpdateIntensity(1000 * self.duration[3], PTT * self.conditioning))
      schedule.Add(lambda: self.UpdateIntensity(5, 0))
      self.tc.Scheduler.Run(schedule)

      return True
   
   def Sample(self):
      return [self.currentIntenisity]
   
   def Stop(self):
      self.running = False
      self.tc.Instruments.Stimulator.Cancel()
      return True
   
def CreateElectricalIncreasingOffsetModulation(tc):
   return ElectricalOffsetModulation(tc, 1.5, 1.8, [2, 10, 10, 10])

def CreateElectricalDecreasingOffsetModulation(tc):
   return ElectricalOffsetModulation(tc, 1.8, 1.5, [2, 10, 10, 10])
