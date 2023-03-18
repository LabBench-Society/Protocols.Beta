def LegSizeInstruction():
    if SURVEY['CLEARING'] == 3:   # Both sides cleared
        if SURVEY['HAND'] == 1: # Right hand is dominant
            return 'What is the size of the right leg in cm'
        elif SURVEY['HAND'] == 2: # Left hand is dominant
            return 'What is the size of the left leg in cm'
        else: # Both hands are dominant
            return 'What is the size of the right leg in cm'
    elif SURVEY['CLEARING'] == 2: # Left side cleared
        return 'What is the size of the left leg in cm'
    elif SURVEY['CLEARING'] == 1: # Right side cleared
        return 'What is the size of the right leg in cm'
    else: # None cleared for test
        return 'No side is cleared'  
