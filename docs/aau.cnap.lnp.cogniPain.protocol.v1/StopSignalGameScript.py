import random
import math

class UpDownAlgorithm:
    def __init__(self, tc, stepsize, initialDelay):
        self.lowerLimit = tc.StopSignalLowDelayLimit
        self.highLimit = tc.StopSignalHighDelayLimit
        self.delay = initialDelay
        self.stopSignalDelay = []
        self.stepsize = stepsize

        self.delays = []

    def Complete(self, result):
        result.Annotations.SetIntegers("sstDelays", self.delays)
        result.Annotations.SetIntegers("sstStopSignalDelay", self.stopSignalDelay)

    def Iterate(self, answer):
        if answer:
            self.delay = self.delay + self.stepsize
            
            if self.delay > self.highLimit:
                self.delay = self.highLimit
        else:
            self.delay = self.delay - self.stepsize
            
            if self.delay < self.lowerLimit:
                self.delay = self.lowerLimit
        
        self.stopSignalDelay.append(self.delay)

class PsiAlgorithm:
    def __init__(self, tc):
        self.lowerLimit = tc.StopSignalLowDelayLimit
        self.highLimit = tc.StopSignalHighDelayLimit
        self.delays = []
        self.method = tc.Create(tc.Psychophysics.PsiMethod()
                                                .NumberOfTrials(tc.StopSignalTrials)
                                                .Function(tc.Psychophysics.Functions.Quick(Beta=1, Lambda=0.02, Gamma=0))
                                                .Alpha(X0=tc.StopSignalAlphaX0,X1=1.0,N = tc.StopSignalAlphaN)
                                                .Beta(X0=tc.StopSignalBetaX0,X1=tc.StopSignalBetaX1,N = tc.StopSignalBetaN)
                                                .Intensity(X0 = tc.StopSignalIntensityX0,X1 = 1.0,N = tc.StopSignalIntensityN))
        
        self.delay = self.Transform(self.method.Setup())     
        self.alpha = []
        self.beta = []
        self.ConfidenceLevel = tc.StopSignalConfidenceLevel
        self.alphaConfidence = []
        self.betaConfidence = []
        self.stopSignalDelay = []
        self.delays = []

    def Transform(self, x):
        return (self.highLimit - self.lowerLimit) * (1 - x) + self.lowerLimit
    
    def Complete(self, result):
        result.Annotations.SetNumber("sstLowerLimit", self.lowerLimit)
        result.Annotations.SetNumber("sstHighLimit", self.highLimit)
        result.Annotations.SetNumbers("sstDelays", self.delays)
        result.Annotations.SetNumbers("sstStopSignalDelay", self.stopSignalDelay)
        result.Annotations.SetNumbers("sstAlpha", self.alpha)        
        result.Annotations.SetNumbers("sstAlphaLower", [x[0] for x in self.alphaConfidence])        
        result.Annotations.SetNumbers("sstAlphaUpper", [x[1] for x in self.alphaConfidence])        
        result.Annotations.SetNumbers("sstBeta", self.beta)   
        result.Annotations.SetNumbers("sstBetaLower", [x[0] for x in self.betaConfidence])        
        result.Annotations.SetNumbers("sstBetaUpper", [x[1] for x in self.betaConfidence])                

    def Iterate(self, answer):
        self.delays.append(self.delay)

        self.delay = self.Transform(self.method.Iterate(answer))      

        alpha = self.method.EstimateAlpha()
        self.alpha.append(alpha)
        self.beta.append(self.method.EstimateBeta())
        self.alphaConfidence.append(self.method.EstimateAlphaConfidenceInterval(self.ConfidenceLevel))
        self.betaConfidence.append(self.method.EstimateBetaConfidenceInterval(self.ConfidenceLevel))
        self.stopSignalDelay.append(self.Transform(alpha))
        

class StopSignalTask:
    def __init__(self, tc, algorithm, feedback):
        self.Log = tc.Log
        self.feedback = feedback
        self.Buttons = tc.Response.Buttons
        self.display = tc.Instruments.ImageDisplay
        self.response = tc.Instruments.Button
        self.images = tc.Assets.StopSignalGameImages
        self.algorithm = algorithm
        self.feedbackTime = tc.StopSignalFeedbackTime
        self.responseTimeout = tc.StopSignalResponseTimeout
        self.feedbackDelay = tc.StopSignalFeedbackDelay
                   
        self.goSignals = [] # 0: left, 1: right
        self.answer = []
        self.time = []
        
        self.result = tc.Current
        self.Fiducials = tc.ExperimentalSetup != "JOYSTICK"
            
        self.Log.Information("Stop Signal Task [ CREATED ]")
    
    def Complete(self):
        self.result.Annotations.SetIntegers("sstGoSignals", self.goSignals)
        self.result.Annotations.SetBools("sstAnswer", self.answer)
        self.result.Annotations.SetIntegers("sstTime", self.time)
        self.algorithm.Complete(self.result)
        self.Log.Information("Stop Signal Task [ SAVED ]")

    def Go(self):
        self.response.Reset()
        self.signal = random.randint(0,1)
        self.goSignals.append(self.signal)
        
        if self.signal == 0:
            self.display.Display(self.images.Left, self.Fiducials)
        else:
            self.display.Display(self.images.Right, self.Fiducials)                      
       
        self.Log.Information("STOP-SIGNAL TESTING DELAY [ Delay: {delay} ]".format(delay = self.algorithm.delay))

        return self.algorithm.delay
        
    def Stop(self):
        if self.signal == 0:
            self.display.Display(self.images.StopLeft)
        else:
            self.display.Display(self.images.StopRight)    

        return self.responseTimeout - self.algorithm.delay
            
    def Feedback(self):
        if self.response.LatchedActive != self.Buttons.NoResponse:
            self.answer.append(False)
            self.time.append(int(self.response.ReactionTime))
        else:           
            self.answer.append(True)
            self.time.append(int(-1))

        self.algorithm.Iterate(self.answer[-1])

        self.Log.Information("STOP-SIGNAL RESPONSE [ Correct: {answer}, sstDelay: {stopSignalDelay}, New Delay: {delay} ]", 
                        self.answer[-1], 
                        self.algorithm.stopSignalDelay[-1], 
                        self.algorithm.delay)

        self.feedback.StopFeedback(self.answer[-1])

        return self.feedbackTime

class GoSignalTask:
    def __init__(self, tc, feedback):   
        self.Log = tc.Log    
        self.Buttons = tc.Response.Buttons
        self.feedback = feedback
        self.tc = tc
        self.display = tc.Instruments.ImageDisplay
        self.response = tc.Instruments.Button
        self.images = tc.Assets.StopSignalGameImages

        self.goDelay = tc.StopSignalHighDelayLimit
        self.goSignals = [] # 0: left, 1: right
        self.answer = []
        self.time = []
        
        self.feedbackTime = tc.StopSignalFeedbackTime
        self.responseTimeout = tc.StopSignalResponseTimeout
        self.feedbackDelay = tc.StopSignalFeedbackDelay
        
        self.result = tc.Current
        self.Fiducials = tc.ExperimentalSetup != "JOYSTICK"
            
        self.Log.Information("Go Signal Task Created")
        
    def Complete(self):
        self.result.Annotations.SetIntegers("gtSignals", self.goSignals)
        self.result.Annotations.SetBools("gtAnswer", self.answer)
        self.result.Annotations.SetNumbers("gtTime", self.time)
    
    def Go(self):
        self.response.Reset()        
        self.signal = random.randint(0,1)
        self.goSignals.append(self.signal)
        
        if self.signal == 0:
            self.display.Display(self.images.Left, self.Fiducials)
        else:
            self.display.Display(self.images.Right, self.Fiducials)                      
       
        return self.responseTimeout
                  
    def Feedback(self):
        button = self.response.LatchedActive
        self.time.append(self.response.ReactionTime)
        
        if button == self.Buttons.NoResponse:
            self.answer.append(False)
        else:         
            if self.signal == 0: # Left
                if button == self.Buttons.Left: # Correct
                    self.answer.append(True)
                else: # wrong
                    self.answer.append(False)
                    
            else: # Right
                if button == self.Buttons.Right: # Correct
                    self.answer.append(True)
                else: # wrong
                    self.answer.append(False)
                        
        self.Log.Information("GO RESPONSE [ Button: {button}, Signal: {signal}, Correct: {answer}, Time: {time}]", 
                         button, 
                         "left" if self.signal == 0 else "right", 
                         self.answer[-1],
                         self.time[-1])

        self.feedback.GoFeedback(self.answer[-1], self.time[-1])

        return self.feedbackTime
 
class GameFeedback:
    def __init__(self, tc):
        self.tc = tc

        self.images = tc.Assets.StopSignalGameImages
        self.display = tc.Instruments.ImageDisplay
        self.algometer = tc.Instruments.PressureAlgometer

        if tc.THRSelection.Value:
            self.intensity = tc.THR70.PULSE
        else:
            self.intensity = 100

        self.score = 0
        self.accumulated = 0
        self.result = tc.Current
        self.Log = tc.Log

    def Complete(self):
        self.result.Annotations.SetInteger("score", int(self.score))

    def Stimulate(self):
        algometer = self.algometer

        chan = algometer.Channels[0]
        chan.SetStimulus(1, chan.CreateWaveform().Step(self.intensity, 1.5))
        algometer.ConfigurePressureOutput(0, algometer.ChannelIDs.CH01)
        algometer.StartStimulation(algometer.StopCriterions.WhenButtonPressed, True, False)

        return True

    def GoFeedback(self, answer, time):        
        display = self.display
        with self.tc.Image.GetCanvas(self.display) as canvas:
            canvas.AlignCenter()
            canvas.AlignMiddle()
            canvas.Font("Roboto")
            canvas.TextSize(98)
            distance = display.Height/14

            if answer:
                score = math.ceil((self.tc.StopSignalResponseTimeout - time)/10)
                self.Log.Debug("Reaction time: {time} => score: {score}", time, score)
                score = score if score > 0 else 1
                self.score = int(self.score + score)
                self.accumulated = int(self.accumulated + score)
                canvas.Color("#00FF00")
                canvas.Write(display.Width/2 , display.Height/2 - distance, "YOU WIN")
                canvas.Write(display.Width/2, display.Height/2 + distance, "+{score} points".format(score = score))
            else:
                canvas.Color("#FF0000")
                canvas.Write(display.Width/2 , display.Height/2, "YOU LOOSE")
                #self.Stimulate()

            self.display.Display(canvas)

    def StopFeedback(self, answer):
        display = self.display

        with self.tc.Image.GetCanvas(self.display) as canvas:
            canvas.AlignCenter()
            canvas.AlignMiddle()
            canvas.Font("Roboto")
            canvas.TextSize(98)
            distance = display.Height/14

            if answer:
                canvas.Color("#00FF00")
                canvas.Write(display.Width/2 , display.Height/2, "YOU WIN")
            else:
                self.level = 1
                canvas.Color("#FF0000")
                canvas.Write(display.Width/2 , display.Height/2 - distance, "YOU LOOSE")
                canvas.Write(display.Width/2, display.Height/2 + distance, "-{score} points".format(score = self.accumulated))
                self.score = self.score - self.accumulated # Penalty for loosing
                self.Stimulate()

            self.accumulated = 0
            self.display.Display(canvas)

def UpDownGameInitialize(tc):
    feedback = GameFeedback(tc)
    tc.Defines.Set("Feedback", feedback)
    tc.Defines.Set("StopTask", StopSignalTask(tc, UpDownAlgorithm(tc, 100, 150), feedback))
    tc.Defines.Set("GoTask", GoSignalTask(tc, feedback))
    return True

def PsiGameInitialize(tc):
    feedback = GameFeedback(tc)
    tc.Defines.Set("Feedback", feedback)
    tc.Defines.Set("StopTask", StopSignalTask(tc, PsiAlgorithm(tc), feedback))
    tc.Defines.Set("GoTask", GoSignalTask(tc, feedback))
    return True

def Complete(tc):
    tc.StopTask.Complete()
    tc.GoTask.Complete()
    tc.Feedback.Complete()
    return True

def DisplayScore(tc):
    with tc.Image.GetCanvas(tc.DisplayWidth, tc.DisplayHeight) as canvas:
        canvas.AlignCenter()
        canvas.AlignMiddle()
        canvas.Font("Roboto")
        canvas.TextSize(72)
        canvas.Color("#FFFFFF")
        canvas.Write(tc.DisplayWidth/2, tc.DisplayHeight/2, "Final Score: {points} points".format(points = int(tc.Current.Annotations.score)))
        return canvas.GetAsset()

def Stimulate(tc, x):   
    display = tc.Instruments.ImageDisplay
    
    if tc.StimulusName == "STOP":
        display.Run(display.Sequence(tc.StopTask)
                    .Display(tc.Assets.StopSignalGameImages.FixationCross, tc.StopSignalFixationDelay)
                    .Run(lambda task: task.Go())
                    .Run(lambda task: task.Stop())
                    .Display(tc.Assets.StopSignalGameImages.FixationCross, tc.StopSignalFeedbackDelay)
                    .Run(lambda task: task.Feedback()))
        
    elif tc.StimulusName == "GO":
        display.Run(display.Sequence(tc.GoTask)
                    .Display(tc.Assets.StopSignalGameImages.FixationCross, tc.StopSignalFixationDelay)
                    .Run(lambda task: task.Go())
                    .Display(tc.Assets.StopSignalGameImages.FixationCross, tc.StopSignalFeedbackDelay)
                    .Run(lambda task: task.Feedback()))
    else:
        tc.Log.Error("Unknown stimulus: {name}".format(name = tc.StimulusName))

    return True

