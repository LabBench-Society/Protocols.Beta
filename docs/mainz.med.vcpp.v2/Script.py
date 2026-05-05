import random
from collections import defaultdict

class Condition:
   _data = {
      1:  (3, "3-3", ["4-4", "5-5", "6-6", "7-7"]),
      2:  (4, "4-4", ["5-5", "6-6", "7-7"]),
      3:  (5, "5-5", ["6-6", "7-7"]),
      4:  (6, "6-6", ["7-7"]),
      5:  (4, "4-5", ["4-6", "4-7", "6-5", "7-5"]),
      6:  (5, "4-5", ["4-6", "4-7", "6-5", "7-5"]),
      7:  (5, "5-6", ["5-7", "7-6"]),
      8:  (6, "5-6", ["5-7", "7-6"]),
      9:  (3, "3-6", ["3-7", "4-6", "5-6", "7-6"]),
      10: (6, "3-6", ["3-7", "4-6", "5-6", "7-6"]),
      11: (4, "4-7", ["5-7", "6-7"]),
      12: (7, "4-7", ["5-7", "6-7"]),
      13: (4, "4-6", ["5-6", "7-6", "4-7"]),
      14: (6, "4-6", ["5-6", "7-6", "4-7"]),
      15: (3, "3-7", ["4-7", "5-7", "6-7"]),
      16: (7, "3-7", ["4-7", "5-7", "6-7"]),
   }

   _lure_pools = defaultdict(list)

   def __init__(self, condition: int, tc):
      if condition not in self._data:
         raise ValueError(f"Invalid condition: {condition}")
      
      self.CardWidth = 0.7/4
      self.CardMargin = 0.05/4

      self.tc = tc
      self.Cards = tc.Assets.Cards
      self.Condition = condition
      self.TargetIntensity, self.Target, lures = self._data[condition]

      self.Lure = self._next_lure(condition, lures)

      self.TargetLeft = random.choice([True, False]) 

      self.TargetPositions = [0, 1]
      random.shuffle(self.TargetPositions)

      self.LureIntensity = self.get_intensity(self.Lure)
      self.LurePositions = [0, 1]
      random.shuffle(self.LurePositions)

      self.InterTrialInterval = random.choice([1000, 1500, 2000, 2500, 3000])

   @classmethod
   def _next_lure(cls, condition, lures):
      pool = cls._lure_pools[condition]

      if not pool:
         pool.extend(lures)
         random.shuffle(pool)

      return pool.pop()
   
   def is_target_selected(self, leftPressed):
      if self.TargetLeft:
         return leftPressed
      else:            
         return not leftPressed

   def parse(self, cue: str):
      a, b = map(int, cue.split("-"))
      return [a, b]

   def get_intensity(self, cue: str) -> int:
      return random.choice(self.parse(cue))
   
   def plotCue(self, image, x, cue, position):
      y = image.Height / 2
      cardWidth = self.CardWidth * image.Width
      cardMargin = self.CardMargin * image.Width

      cue0loc = image.Sprite(x-cardWidth/2 - cardMargin/2, y, self.Cards[f'Spades0{cue[position[0]]}'], cardWidth, -1)
      cue1loc = image.Sprite(x+cardWidth/2 + cardMargin/2, y, self.Cards[f'Spades0{cue[position[1]]}'], cardWidth, -1)
      image.Rectangle(cue0loc.Left - cardMargin, cue0loc.Top - cardMargin, cue1loc.Right + cardMargin, cue1loc.Bottom + cardMargin, cardMargin)

   def plot(self, image):
      image.AlignCenter()
      image.AlignMiddle()
      image.Color("#FFFFFF")
      image.TextSize(72)
      
      y = image.Height / 2
      xLeft = int(image.Width / 4)
      xRight = int(3 * image.Width / 4)
      target = self.parse(self.Target)
      lure = self.parse(self.Lure)
      targetPos = self.TargetPositions
      lurePos = self.LurePositions

      self.plotCue(image, xLeft, target if self.TargetLeft else lure, targetPos if self.TargetLeft else lurePos)
      self.plotCue(image, xRight, lure if self.TargetLeft else target, lurePos if self.TargetLeft else targetPos)   

   def plot_selected(self, image, targetSelected):
      image.AlignCenter()
      image.AlignMiddle()
      image.Color("#FFFFFF")

      y = image.Height / 2
      x = int(image.Width / 2)
      cue = self.parse(self.Target if targetSelected else self.Lure)
      pos = self.TargetPositions if targetSelected else self.LurePositions

      self.plotCue(image, x, cue, pos)

   def __repr__(self):
      return (
         f"Condition({self.Condition}) -> "
         f"Target={self.Target} (I: {self.TargetIntensity}, P: {self.TargetPositions}), "
         f"Lure={self.Lure} (I: {self.LureIntensity}, P: {self.LurePositions}), "
         f"TargetLeft={self.TargetLeft}"
      )
   
class ResponseTask:
   def __init__(self, tc):
      self.tc = tc
      self.currentRating = 0

   def Start(self, numberOfTrials = 9999):
      self.trials = [Condition(c, self.tc) for c in range(1, 17) for _ in range(5)]
      random.shuffle(self.trials)

      if numberOfTrials < len(self.trials):
         self.trials = self.trials[:numberOfTrials]

      for trial in self.trials:
         self.tc.Log.Information(f"Trial: {trial}")
     
      self.index = 0
      self.ratings = []     
      self.currentRating = 0
      self.targetSelected = [] 

      return True
   
   def Complete(self):
      data = self.tc.Current

      data.SetNumbers("ratings", self.ratings)
      data.SetBools("targetSelected", self.targetSelected)
      data.SetIntegers("conditions", [condition.Condition for condition in self.trials])
      data.SetString("targets", [condition.Target for condition in self.trials])
      data.SetString("lures", [condition.Lure for condition in self.trials])
      data.SetIntegers("targetIntensities", [condition.TargetIntensity for condition in self.trials])
      data.SetIntegers("lureIntensities", [condition.LureIntensity for condition in self.trials])
      
      return True

   def PlotInstruction(self, x,y, message):
      with self.tc.Image.GetCanvas(x, y, "#000000") as image:
         image.AlignCenter()
         image.AlignMiddle()
         image.Color("#FFFFFF")
         image.TextSize(48)
         image.Write(x /2, y /2, message)
         return image.GetImage()

   def PlotRating(self, x, y):
      with self.tc.Image.GetCanvas(x, y, "#000000") as image:
         image.AlignCenter()
         image.AlignMiddle()
         image.Color("#FFFFFF")
         image.TextSize(48)
         image.Write(x /2, y /2, f"Rating: {self.currentRating:.1f}")
         return image.GetImage()
                
   def PlotChoices(self, condition: Condition):
      display = self.tc.Instruments.ImageDisplay

      with self.tc.Image.GetCanvas(display, "#000000") as image:
         condition.plot(image)
         return image.GetImage()

   def PlotOperatorChoices(self, x, y, condition: Condition):
      with self.tc.Image.GetCanvas(x, y, "#000000") as image:
         condition.plot(image)
         return image.GetImage()

   def PlotSelected(self, condition: Condition, targetSelected: bool):
      display = self.tc.Instruments.ImageDisplay

      with self.tc.Image.GetCanvas(display, "#000000") as image:
         condition.plot_selected(image, targetSelected)
         return image.GetImage()

   def PlotOperatorSelected(self, x, y, condition: Condition, targetSelected: bool):
      with self.tc.Image.GetCanvas(x, y, "#000000") as image:
         condition.plot_selected(image, targetSelected)
         return image.GetImage()

   def Stimulate(self, condition: Condition, targetSelected: bool, srTest):
      if targetSelected:
         intensity = condition.TargetIntensity
         self.tc.Log.Information("Target intensity: {intensity}", condition.TargetIntensity)
      else:
         intensity = condition.LureIntensity
         self.tc.Log.Information("Lure intensity: {intensity}", condition.LureIntensity)      

      pressure = srTest.GetPressureFromPerception(intensity)
      self.tc.Log.Information(f"Stimulation pressure: {pressure:.1f}kPa")

      algometer = self.tc.Instruments.PressureAlgometer
      chan = algometer.Channels[0]

      chan.SetStimulus(1, chan.CreateWaveform().Step(pressure, 2))
      algometer.ConfigurePressureOutput("outlet-1", "channel-1")
      algometer.ConfigurePressureOutput("outlet-2", "none")
      algometer.StartStimulation('stop-when-button-pressed', True)

      return pressure


   def Enter(self, srTest):
      self.tc.Keyboard.Clear();
      self.tc.Instruments.Button.Reset()

      id = self.tc.CurrentState.ID
      display = self.tc.Instruments.ImageDisplay
      condition = self.trials[self.index]
      self.tc.Log.Information(f"Index: {self.index}, Condition: {condition}")

      if id == "CROSS":
         self.tc.CurrentState.SetPlotter(lambda x,y : self.PlotInstruction(x, y, "CROSS"))
         display.Display(self.tc.Assets.Images.Cross, 1500)
      if id == "SELECTION":
         self.tc.CurrentState.SetPlotter(lambda x,y : self.PlotOperatorChoices(x, y, condition))
         display.Display(self.PlotChoices(condition))
      if id == "DISPLAY":
         self.tc.CurrentState.SetPlotter(lambda x,y : self.PlotOperatorSelected(x, y, condition, self.targetSelected[-1]))
         display.Display(self.PlotSelected(condition, self.targetSelected[-1]))
      if id == "STIMULATION":
         display.Display(self.tc.Assets.Images.Stimulating)
         pressure = self.Stimulate(condition, self.targetSelected[-1], srTest)
         self.tc.CurrentState.SetPlotter(lambda x,y : self.PlotInstruction(x, y, f"Stimulating: {pressure:.1f}kPa"))
      if id == "RATING":
         self.tc.CurrentState.SetPlotter(lambda x,y : self.PlotRating(x, y))
      if id == "RESETRATING":
         self.tc.CurrentState.SetPlotter(lambda x,y : self.PlotRating(x, y))
         display.Display(self.tc.Assets.Images.ResetRating)
      if id == "PAUSE":
         display.Display(self.tc.Assets.Images.Blank)
         self.tc.CurrentState.SetPlotter(lambda x,y : self.PlotInstruction(x, y, f"Pause: {condition.InterTrialInterval:.0f}ms"))
      if id == "REST":
         self.tc.Keyboard.Clear()
         display.Display(self.tc.Assets.Images.Break)
         self.tc.CurrentState.SetPlotter(lambda x,y : self.PlotInstruction(x, y, "Press INSERT to continue."))

      return True
     
   def Update(self):
      button = self.tc.Instruments.Button
      scale = self.tc.Instruments.RatioScale
      algometer = self.tc.Instruments.PressureAlgometer

      id = self.tc.CurrentState.ID
      condition = self.trials[self.index]

      if id == "CROSS":
         return "*" if self.tc.CurrentState.RunningTime < 2000 else "SELECTION"
      
      if id == "SELECTION":
         if not button.IsLatched("none"):
            self.tc.Log.Information(f"Latched button: {button.GetLatched()}")

         if button.IsLatched("1"):
            self.targetSelected.append(condition.is_target_selected(True))
            self.tc.Log.Information("BTN 1: Target selected: {selected}", self.targetSelected[-1])
            return "DISPLAY"
         
         if button.IsLatched("2"):
            self.targetSelected.append(condition.is_target_selected(False))
            self.tc.Log.Information("BTN 2: Target selected: {selected}", self.targetSelected[-1])
            return "DISPLAY"
         
      if id == "DISPLAY":
         return "*" if self.tc.CurrentState.RunningTime < 2000 else "STIMULATION"
      
      if id == "STIMULATION":
         return "*" if self.tc.CurrentState.RunningTime < 2500 else "RATING"
      
      if id == "RATING":
         self.currentRating = scale.GetRatioRating()

         if button.IsLatched("1") or button.IsLatched("2"):
            self.ratings.append(self.currentRating)
            return "RESETRATING"         
         
      if id == "RESETRATING":
         self.currentRating = algometer.GetRatioRating()

         if self.currentRating < 0.1:
            return "PAUSE"

      if id == "PAUSE":
         if self.tc.CurrentState.RunningTime < condition.InterTrialInterval:
            return "*"
         
         self.index = self.index + 1

         if self.index == len(self.trials):
            return "complete"
         
         if self.index % 20 == 0:
            return "REST"
         
         return "CROSS"
      
      if id == "REST":
         if self.tc.Keyboard.Pressed("INSERT"):
            return "CROSS"         
         
      return "*"

def CreateTask(tc):
   return ResponseTask(tc)

