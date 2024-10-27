def ArmIntensity(tc):
   return (tc.ARM1.GetPressureFromPerception(7.0)+tc.ARM2.GetPressureFromPerception(7.0)+tc.ARM3.GetPressureFromPerception(7.0))/3

def LegIntensity(tc):
   return (tc.LEG1.GetPressureFromPerception(7.0)+tc.LEG2.GetPressureFromPerception(7.0)+tc.LEG3.GetPressureFromPerception(7.0))/3
