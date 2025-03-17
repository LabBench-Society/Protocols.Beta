def GetRandomizationTableWP1(tc):
   '''Perform randomization based on the subject ID
      0: Calf (Right)
      1: Lumbar (Right)
      2: Forearm (Right)
      3: Calf (Left)
      4: Lumbar (Left)
      5: Forearm (Left)
   '''
   return [
      [0,1,2,3,4,5], # Calf_R        Lumbar_R        Forearm_R      Calf_L        Lumbar_L       Forearm_L
      [0,2,1,3,5,4], # Calf_R        Forearm_R       Lumbar_R       Calf_L        Forearm_L      Lumbar_L
      [1,0,2,4,3,5], # Lumbar_R      Calf_R          Forearm_R      Lumbar_L      Calf_L         Forearm_L
      [1,2,0,4,5,3], # Lumbar_R      Forearm_R       Calf_R         Lumbar_L      Forearm_L      Calf_L
      [2,0,1,5,3,4], # Forearm_R     Calf_R          Lumbar_R       Forearm_L     Calf_L         Lumbar_L
      [2,1,0,5,4,3], # Forearm_R     Lumbar_R        Calf_R         Forearm_L     Lumbar_L       Calf_L
      [0,1,2,3,4,5], # Calf_R        Lumbar_R        Forearm_R      Calf_L        Lumbar_L       Forearm_L
      [1,0,2,4,3,5], # Lumbar_R      Calf_R          Forearm_R      Lumbar_L      Calf_L         Forearm_L
      [2,0,1,5,3,4], # Forearm_R     Calf_R          Lumbar_R       Forearm_L     Calf_L         Lumbar_L
      [2,1,0,5,4,3], # Forearm_R     Lumbar_R        Calf_R         Forearm_L     Lumbar_L       Calf_L
      [3,4,5,0,1,2], # Calf_L        Lumbar_L        Forearm_L      Calf_R        Lumbar_R       Forearm_R
      [3,5,4,0,2,1], # Calf_L        Forearm_L       Lumbar_L       Calf_R        Forearm_R      Lumbar_R
      [4,3,5,1,0,2], # Lumbar_L      Calf_L          Forearm_L      Lumbar_R      Calf_R         Forearm_R
      [4,5,4,1,2,0], # Lumbar_L      Forearm_L       Calf_L         Lumbar_R      Forearm_R      Calf_R
      [5,3,4,2,0,1], # Forearm_L     Calf_L          Lumbar_L       Forearm_R     Calf_R         Lumbar_R
      [5,4,3,2,1,0], # Forearm_L     Lumbar_L        Calf_L         Forearm_R     Lumbar_R       Calf_R
      [3,4,5,0,1,2], # Calf_L        Lumbar_L        Forearm_L      Calf_R        Lumbar_R       Forearm_R
      [4,3,5,1,0,2], # Lumbar_L      Calf_L          Forearm_L      Lumbar_R      Calf_R         Forearm_R
      [5,3,4,2,0,1], # Forearm_L     Calf_L          Lumbar_L       Forearm_R     Calf_R         Lumbar_R
      [5,4,3,2,1,0]  # Forearm_L     Lumbar_L        Calf_L	        Forearm_R     Lumbar_R       Calf_R
   ]

def GetRandomizationTableWP2(tc):
   '''Perform randomization based on the subject ID
      0: Calf (Right)
      1: Lumbar (Right)
      2: Forearm (Right)
      3: Calf (Left)
      4: Lumbar (Left)
      5: Forearm (Left)
   '''
   return [
      [0,1,2,3,4,5], # Calf_R    Lumbar_R  Forearm_R  Calf_L	 Lumbar_L  Forearm_L
      [0,1,2,3,4,5], # Calf_R    Lumbar_R  Forearm_R  Calf_L	 Lumbar_L  Forearm_L
      [0,1,2,3,4,5], # Calf_R    Lumbar_R  Forearm_R  Calf_L	 Lumbar_L  Forearm_L
      [0,2,1,3,5,4], # Calf_R	   Forearm_R Lumbar_R	Calf_L	 Forearm_L Lumbar_L
      [0,2,1,3,5,4], # Calf_R	   Forearm_R Lumbar_R	Calf_L	 Forearm_L Lumbar_L
      [1,0,2,4,3,5], # Lumbar_R	Calf_R	 Forearm_R	Lumbar_L	 Calf_L	 Forearm_L 
      [1,0,2,4,3,5], # Lumbar_R	Calf_R	 Forearm_R	Lumbar_L	 Calf_L	 Forearm_L
      [1,2,0,4,5,3], # Lumbar_R	Forearm_R Calf_R     Lumbar_L	 Forearm_L Calf_L
      [1,2,0,4,5,3], # Lumbar_R	Forearm_R Calf_R     Lumbar_L	 Forearm_L Calf_L
      [1,2,0,4,5,3], # Lumbar_R	Forearm_R Calf_R     Lumbar_L	 Forearm_L Calf_L
      [2,0,1,5,3,4], # Forearm_R	Calf_R    Lumbar_R   Forearm_L Calf_L	  Lumbar_L
      [2,0,1,5,3,4], # Forearm_R	Calf_R    Lumbar_R   Forearm_L Calf_L	  Lumbar_L
      [2,0,1,5,3,4], # Forearm_R	Calf_R    Lumbar_R   Forearm_L Calf_L	  Lumbar_L
      [2,1,0,5,4,3], # Forearm_R	Lumbar_R	Calf_R	Forearm_L	 Lumbar_L  Calf_L
      [2,1,0,5,4,3], # Forearm_R	Lumbar_R	Calf_R	Forearm_L	 Lumbar_L  Calf_L
      [3,4,5,0,1,2], # Calf_L    Lumbar_L  Forearm_L	Calf_R	 Lumbar_R  Forearm_R
      [3,4,5,0,1,2], # Calf_L    Lumbar_L  Forearm_L	Calf_R	 Lumbar_R  Forearm_R
      [3,4,5,0,1,2], # Calf_L    Lumbar_L  Forearm_L	Calf_R	 Lumbar_R  Forearm_R
      [3,5,4,0,2,1], # Calf_L    Forearm_L Lumbar_L   Calf_R    Forearm_R Lumbar_R
      [3,5,4,0,2,1], # Calf_L    Forearm_L Lumbar_L   Calf_R    Forearm_R Lumbar_R
      [4,3,5,1,0,2], # Lumbar_L	Calf_L    Forearm_L  Lumbar_R  Calf_R    Forearm_R
      [4,3,5,1,0,2], # Lumbar_L	Calf_L    Forearm_L  Lumbar_R  Calf_R    Forearm_R
      [4,5,3,1,2,0], # Lumbar_L  Forearm_L Calf_L     Lumbar_R  Forearm_R Calf_R
      [4,5,3,1,2,0], # Lumbar_L  Forearm_L Calf_L     Lumbar_R  Forearm_R Calf_R
      [4,5,3,1,2,0], # Lumbar_L  Forearm_L Calf_L     Lumbar_R  Forearm_R Calf_R
      [5,3,4,2,0,1], # Forearm_L Calf_L    Lumbar_L	Forearm_R Calf_R    Lumbar_R
      [5,3,4,2,0,1], # Forearm_L Calf_L    Lumbar_L	Forearm_R Calf_R    Lumbar_R
      [5,3,4,2,0,1], # Forearm_L Calf_L    Lumbar_L	Forearm_R Calf_R    Lumbar_R
      [5,4,3,2,1,0], # Forearm_L	Lumbar_L  Calf_L     Forearm_R Lumbar_R  Calf_R
      [5,4,3,2,1,0]  # Forearm_L	Lumbar_L  Calf_L     Forearm_R Lumbar_R  Calf_R
   ]

def GetSubjectNumer(text):
   if not text.startswith("M") or "_" not in text:
      raise ValueError("Invalid format: " + text)
    
   try:
      number_part = text[1:text.index("_")]

      if not number_part.isdigit() or not (1 <= int(number_part) <= 99):
         raise ValueError("Invalid format: " + text)
      
      return int(number_part)
   except (ValueError, IndexError):
      raise ValueError("Invalid format: " + text)   

def RandomizeThresholds(tc):
   n = GetSubjectNumer(tc.Subject)

   if (n < 1):
      raise ValueError("Subject number must be 1 or greater")

   return tc.RTable[(n-1)%30]

def GetPPTWaitTime(tc):
   return 30 if 'TEST' in tc.Subject else 15*60