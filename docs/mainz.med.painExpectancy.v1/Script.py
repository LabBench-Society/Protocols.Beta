import random 


class ResponseTask:
   class CueState:
      """
      Selection of either a lure and or target cue by the participant. 

      Cues provide visual information about the propability of the painfulness of the upcoming stimulus. 
      The each stimulation may be result in one of two stimulus intensities that are equally probable; one low and one high.
      Consequently, the cue results in an average pain expectancy that is the mean of the two possible stimulus intensities.

      The lure has a higher average pain expectancy than the target.
      """
      def __init__(self, tc, owner):
         self.owner = owner
         self.tc = tc
         pass

      def CreateCueImage(self, cue):
         with self.tc.Image.GetCanvas(self.tc.Instruments.ImageDisplay, "#000000") as canvas:
            w = self.tc.Instruments.ImageDisplay.Width
            h = self.tc.Instruments.ImageDisplay.Height
            canvas.AlignCenter()
            canvas.AlignMiddle()
            canvas.Color("#FFFFFF")
            canvas.Write(w, h, "Cue: {}".format(cue))
            return canvas.GetImage()

      def Enter(self):
         pass

      def Leave(self):
         pass

      def Update(self):
         pass

   class DisplayState:
      def __init__(self, tc, owner):
         self.owner = owner
         self.tc = tc
         pass

      def Enter(self):
         pass

      def Leave(self):
         pass

      def Update(self):
         pass

   class StimulateState:
      def __init__(self, tc, owner):
         self.owner = owner
         self.tc = tc
         pass

      def Enter(self):
         pass

      def Leave(self):
         pass

      def Update(self):
         pass

   class RateState:
      def __init__(self, tc, owner):
         self.owner = owner
         self.tc = tc
         pass

      def Enter(self):
         pass

      def Leave(self):
         pass

      def Update(self):
         pass

   class PauseState:
      def __init__(self, tc, owner):
         self.owner = owner
         self.tc = tc
         pass

      def Enter(self):
         pass

      def Leave(self):
         pass

      def Update(self):
         pass

   def __init__(self, tc):
      self.tc = tc
      self.states = {
         "Cue": self.CueState(tc, self),
         "Display": self.DisplayState(tc, self),
         "Stimulate": self.StimulateState(tc, self),
         "Rate": self.RateState(tc, self),
         "Pause": self.PauseState(tc, self),
      }

   def Start(self):
      self.ratings = []      
      self.current = 0
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
      return self.states[self.tc.CurrentState.ID].Enter()
 
   
   def Leave(self):
      return self.states[self.tc.CurrentState.ID].Leave()
   
   def Update(self):
      return self.states[self.tc.CurrentState.ID].Update()

def CreateTask(tc):
   return ResponseTask(tc)

