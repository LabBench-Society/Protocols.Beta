import random

def GetWords(tc):
    if tc.Language == 'DA':
        return {'b': 'BLÅ','y': 'GUL','r': 'RØD','g': 'GRØN'}
    
    return {'b': 'BLUE','y': 'YELLOW','r': 'RED','g': 'GREEN'}

def StroopNeutralStimulate(tc, x):
    display = tc.Instruments.ImageDisplay
    name =  tc.StimulusName
    triggerGenerator = tc.Instruments.TriggerGenerator

    with tc.Image.GetCanvas(display) as canvas:
        canvas.Fill(True)
        canvas.Color(tc.StroopColors[name[0]])
        canvas.Circle(display.Width/2, display.Height/2, display.Height/8)

        triggerGenerator.GenerateTriggerSequence(tc.Triggers.StartTrigger.Response01, 
                                                 tc.Triggers.Sequence()
                                                   .Add(tc.Triggers.Trigger(10).Stimulus().Code(1)))
        display.Display(canvas, tc.StroopDisplayTime, True)
        
    return True

def StroopStimulate(tc, x):
    display = tc.Instruments.ImageDisplay
    name =  tc.StimulusName
    triggerGenerator = tc.Instruments.TriggerGenerator

    with tc.Image.GetCanvas(display) as canvas:
        canvas.AlignCenter()
        canvas.AlignMiddle()
        canvas.Font("Roboto")
        canvas.TextSize(200)

        canvas.Color(tc.StroopColors[name[0]])
        canvas.Write(display.Width/2, display.Height/2, tc.StroopWords[name[1]])

        triggerCode = 1 if name[0] == name[1] else 2
        triggerGenerator.GenerateTriggerSequence(tc.Triggers.StartTrigger.Response01, 
                                                 tc.Triggers.Sequence()
                                                   .Add(tc.Triggers.Trigger(10).Stimulus().Code(triggerCode)))
        display.Display(canvas, tc.StroopDisplayTime, True)
        
    return True

def IsCorrect(tc, result):
    if (result.Stimulus[0] == 'b'):
        return True if result.Response == 1 else False
    elif (result.Stimulus[0] == 'y'):
        return True if result.Response == 2 else False
    elif (result.Stimulus[0] == 'r'):
        return True if result.Response == 3 else False
    elif (result.Stimulus[0] == 'g'):
        return True if result.Response == 4 else False
    else:
        tc.Log.Error("Invalid stimulus name: " + result.Stimulus)
        return False
    
def StroopEvaluate(tc):
    tc.Current.Annotations.SetBools("correct", [IsCorrect(tc, s) for s in tc.Current.Stimulations])   
    return True