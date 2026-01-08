import random 


class ResponseTask:
   def __init__(self, tc):
      self.tc = tc
      self.Cue = tc.Assets.Images.Cue
      self.Cue01 = tc.Assets.Images.Cue01
      self.Cue02 = tc.Assets.Images.Cue02
      self.Stimulating = tc.Assets.Images.Stimulating
      self.ratings = []    
      self.current = 0  

   def Start(self):
      self.ratings = []      
      return True
   
   def Complete(self):
      self.tc.Current.SetNumbers("ratings", self.ratings)
      return True

   def PlotRating(self, x, y):
      with self.tc.Image.GetCanvas(x, y, "#FFFFFF") as canvas:
         canvas.AlignCenter()
         canvas.AlignMiddle()
         canvas.Color("#000000")
         canvas.Write(x /2, y /2, "Rating: {}".format(self.current))
         return canvas.GetImage()
      
   def Stimulate(self, freq):
      sound = self.tc.Instruments.SoundCard
      sound.Play(self.tc.Waveforms.Sin(1, freq, 0, 4000,44100).SetChannel(3))      

   def Enter(self):
      id = self.tc.CurrentState.ID
      display = self.tc.Instruments.Display
      self.tc.Keyboard.Clear()
      self.tc.Instruments.Joystick.Reset()

      if id == "CUE":
         display.Display(self.Cue)
         return True
      if id == "CUE01":
         display.Display(self.Cue01)
         return True
      if id == "STIM01":
         self.Stimulate(1000)
         display.Display(self.Stimulating)
         return True
      if id == "CUE02":
         display.Display(self.Cue02)
         return True
      if id == "STIM02":
         self.Stimulate(2000)
         display.Display(self.Stimulating)
         return True
      if id == "RATING":
         self.current = 0
         self.tc.Log.Information("Actions; ESC) Abort, INSERT) Complete, ENTER) Continue.")
         self.tc.CurrentState.SetPlotter(lambda x, y: self.PlotRating(x,y))
         return True
      
      return False
   
   
   def Leave(self):
      id = self.tc.CurrentState.ID
      self.tc.Keyboard.Clear();

      if id == "CUE":
         return True
      if id == "CUE01":
         return True
      if id == "STIM01":
         return True
      if id == "CUE02":
         return True
      if id == "STIM02":
         return True
      if id == "RATING":
         return True
      
      return False      
   
   def Update(self):
      id = self.tc.CurrentState.ID

      if id == "CUE":
         Joystick = self.tc.Instruments.Joystick
         self.tc.CurrentState.Status = "Remaining time: {time}".format(time = 2000 - self.tc.CurrentState.RunningTime)

         if self.tc.CurrentState.RunningTime > 2000: 
            self.tc.Log.Information("No response, selecting one random selection")
            return random.choice(["CUE01", "CUE02"])
         
         if Joystick.IsLatched("left"):
            return "CUE01"

         if Joystick.IsLatched("right"):
            return "CUE02"

         return "*" 
      
      if id == "CUE01":
         return "*" if self.tc.CurrentState.RunningTime < 1000 else "STIM01"
      
      if id == "STIM01":
         self.tc.CurrentState.Status = "Running time: {time}".format(time = self.tc.CurrentState.RunningTime)
         return "*" if self.tc.CurrentState.RunningTime < 1000 else "RATING"
      
      if id == "CUE02":
         return "*" if self.tc.CurrentState.RunningTime < 1000 else "STIM02"
      
      if id == "STIM02":
         self.tc.CurrentState.Status = "Running time: {time}".format(time = self.tc.CurrentState.RunningTime)
         return "*" if self.tc.CurrentState.RunningTime < 1000 else "RATING"
      
      if id == "RATING":
         self.current = self.tc.Instruments.Scale.GetCurrentRating()
         self.tc.CurrentState.Changed = True

         if self.tc.Keyboard.Pressed("ESC"):
            return "abort"
         
         if self.tc.Keyboard.Pressed("INSERT"):
            self.ratings.append(self.current)
            return "complete"
         
         if self.tc.Keyboard.Pressed("ENTER"):
            self.ratings.append(self.current)
            return "CUE"

         return "*"

      return "abort"

def CreateTask(tc):
   return ResponseTask(tc)

