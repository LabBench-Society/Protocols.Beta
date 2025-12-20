
class ElectricalOffsetModulation:
   def __init__(self, tc, conditioning, intensity, duration):
      self.tc = tc
      self.Duration = duration
      self.Intensity = intensity
      self.Conditioning = conditioning
      self.CurrentIntenisity = 0
      self.running = False

   def Duration(self):
      return self.Duration[0] + self.Duration[1] + self.Duration[3] + self.Duration[4] + 4

   def UpdateIntensity(self, duration, intensity):
      if not self.running:
         return 1
      
      self.CurrentIntenisity = intensity
      self.tc.Log.Information("Updating intensity to {}".format(intensity) )

      self.tc.Instruments.Stimulator.Cancel()
      self.tc.Instruments.Stimulator.Generate(self.tc.Stimuli.Repeated(
            self.tc.Stimuli.Arbitrary(lambda t: intensity, 1), 2000, 10))

      return duration

   def Stimulate(self, thr):
      PTT = thr.CH01

      self.running = True
      schedule = self.tc.Scheduler.Create()
      schedule.Add(lambda: self.UpdateIntensity(1000 * self.Duration[0], 0))
      schedule.Add(lambda: self.UpdateIntensity(1000 * self.Duration[1], PTT * self.Conditioning))
      schedule.Add(lambda: self.UpdateIntensity(1000 * self.Duration[2], PTT * self.Intensity))
      schedule.Add(lambda: self.UpdateIntensity(1000 * self.Duration[3], PTT * self.Conditioning))
      schedule.Add(lambda: self.UpdateIntensity(5, 0))
      self.tc.Scheduler.Run(schedule)

      return True

   def Control(self, thr):
      PTT = thr.CH01

      self.running = True
      schedule = self.tc.Scheduler.Create()
      schedule.Add(lambda: self.UpdateIntensity(1000 * self.Duration[0], 0))
      schedule.Add(lambda: self.UpdateIntensity(1000 * self.Duration[1], PTT * self.Conditioning))
      schedule.Add(lambda: self.UpdateIntensity(1000 * self.Duration[2], PTT * self.Conditioning))
      schedule.Add(lambda: self.UpdateIntensity(1000 * self.Duration[3], PTT * self.Conditioning))
      schedule.Add(lambda: self.UpdateIntensity(5, 0))
      self.tc.Scheduler.Run(schedule)

      return True
   
   def Sample(self):
      return [self.CurrentIntenisity]
   
   def Stop(self):
      self.running = False
      self.tc.Instruments.Stimulator.Cancel()
      return True
   
def CreateElectricalOffsetModulation(tc):
   return ElectricalOffsetModulation(tc, 1.5, 1.8, [2, 10, 10, 10])
