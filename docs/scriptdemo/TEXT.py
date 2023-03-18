def CreateEnglishText():
    return {
        "SURVEY.INSTRUCTION:Instructions":                                         "Instructions",
        "SURVEY.HAND:Hand":                                                        "Hand",
        "SURVEY.HAND:Which hand do you normally write with?":                      "Which hand do you normally write with?",
        "SURVEY.HAND:Right hand":                                                  "Right hand",
        "SURVEY.HAND:Left hand":                                                   "Left hand",
        "SURVEY.HAND:Both hands":                                                  "Both hands",
        "SURVEY.CLEARING:Clearing for pressure tests":                             "Clearing for pressure tests",
        "SURVEY.CLEARING:Is the subject cleared for pressure test?":               "Is the subject cleared for pressure test?",
        "SURVEY.CLEARING:Both":                                                    "Both",
        "SURVEY.CLEARING:Right":                                                   "Right",
        "SURVEY.CLEARING:Left":                                                    "Left",
        "SURVEY.CLEARING:None":                                                    "None",
        "SURVEY.LEGSIZE:Leg size":                                                 "Leg size",
   	    "SURVEY.CUFFSIZE:Select cuff size for leg size":                           "Select cuff size for leg size {size}cm", # Do not delete {size} from this text.
		"SURVEY.CUFFSIZE:Small":                                                   "Small (size <= 40cm)",
		"SURVEY.CUFFSIZE:Medium":                                                  "Medium (40cm < size <= 50cm)",
		"SURVEY.CUFFSIZE:Large":                                                   "Large (size > 50cm)",
        "CPT_CLEARING.CLEARING:Clearing":                                          "Clearing",
		"CPT_CLEARING.CLEARING:Is the subject cleared for the cold pressor test?": "Is the subject cleared for the cold pressor test?",
		"CPT_CLEARING.CLEARING:Left hand (default)":                               "Left hand (default)",
		"CPT_CLEARING.CLEARING:Right hand":                                        "Right hand",
		"CPT_CLEARING.CLEARING:Not eligible":                                      "Not eligible"
    }

def CreateDanishText():
    return {
        "SURVEY.INSTRUCTION:Instructions":                                         "Instructions",
        "SURVEY.HAND:Hand":                                                        "Hand",
        "SURVEY.HAND:Which hand do you normally write with?":                      "Which hand do you normally write with?",
        "SURVEY.HAND:Right hand":                                                  "Right hand",
        "SURVEY.HAND:Left hand":                                                   "Left hand",
        "SURVEY.HAND:Both hands":                                                  "Both hands",
        "SURVEY.CLEARING:Clearing for pressure tests":                             "Clearing for pressure tests",
        "SURVEY.CLEARING:Is the subject cleared for pressure test?":               "Is the subject cleared for pressure test?",
        "SURVEY.CLEARING:Both":                                                    "Both",
        "SURVEY.CLEARING:Right":                                                   "Right",
        "SURVEY.CLEARING:Left":                                                    "Left",
        "SURVEY.CLEARING:None":                                                    "None",
        "SURVEY.LEGSIZE:Leg size":                                                 "Leg size",
   	    "SURVEY.CUFFSIZE:Select cuff size for leg size":                           "Select cuff size for leg size {size}cm", # Do not delete {size} from this text.
		"SURVEY.CUFFSIZE:Small":                                                   "Small (size <= 40cm)",
		"SURVEY.CUFFSIZE:Medium":                                                  "Medium (40cm < size <= 50cm)",
		"SURVEY.CUFFSIZE:Large":                                                   "Large (size > 50cm)",
        "CPT_CLEARING.CLEARING:Clearing":                                          "Clearing",
		"CPT_CLEARING.CLEARING:Is the subject cleared for the cold pressor test?": "Is the subject cleared for the cold pressor test?",
		"CPT_CLEARING.CLEARING:Left hand (default)":                               "Left hand (default)",
		"CPT_CLEARING.CLEARING:Right hand":                                        "Right hand",
		"CPT_CLEARING.CLEARING:Not eligible":                                      "Not eligible"
    }

def CreateItalianText():
    return {
        "SURVEY.INSTRUCTION:Instructions":                                         "Instructions",
        "SURVEY.HAND:Hand":                                                        "Hand",
        "SURVEY.HAND:Which hand do you normally write with?":                      "Which hand do you normally write with?",
        "SURVEY.HAND:Right hand":                                                  "Right hand",
        "SURVEY.HAND:Left hand":                                                   "Left hand",
        "SURVEY.HAND:Both hands":                                                  "Both hands",
        "SURVEY.CLEARING:Clearing for pressure tests":                             "Clearing for pressure tests",
        "SURVEY.CLEARING:Is the subject cleared for pressure test?":               "Is the subject cleared for pressure test?",
        "SURVEY.CLEARING:Both":                                                    "Both",
        "SURVEY.CLEARING:Right":                                                   "Right",
        "SURVEY.CLEARING:Left":                                                    "Left",
        "SURVEY.CLEARING:None":                                                    "None",
        "SURVEY.LEGSIZE:Leg size":                                                 "Leg size",
   	    "SURVEY.CUFFSIZE:Select cuff size for leg size":                           "Select cuff size for leg size {size}cm", # Do not delete {size} from this text.
		"SURVEY.CUFFSIZE:Small":                                                   "Small (size <= 40cm)",
		"SURVEY.CUFFSIZE:Medium":                                                  "Medium (40cm < size <= 50cm)",
		"SURVEY.CUFFSIZE:Large":                                                   "Large (size > 50cm)",
        "CPT_CLEARING.CLEARING:Clearing":                                          "Clearing",
		"CPT_CLEARING.CLEARING:Is the subject cleared for the cold pressor test?": "Is the subject cleared for the cold pressor test?",
		"CPT_CLEARING.CLEARING:Left hand (default)":                               "Left hand (default)",
		"CPT_CLEARING.CLEARING:Right hand":                                        "Right hand",
		"CPT_CLEARING.CLEARING:Not eligible":                                      "Not eligible"
    }

def CreateText():
	if Language == 'EN':
		return CreateEnglishText()
	elif Language == 'DA':
		return CreateDanishText()
	elif Language == 'IT':
		return CreateItalianText()
	else:
		return CreateEnglishText()    

def CreateEnglishInstructions():
	return {
		"SURVEY_INSTRUCTION": "SURVEY_INSTRUCTION_EN"
	}

def CreateDanishInstructions():
	return {
		"SURVEY_INSTRUCTION": "SURVEY_INSTRUCTION_DA"
	}

def CreateItalianInstructions():
	return {
		"SURVEY_INSTRUCTION": "SURVEY_INSTRUCTION_IT"
	}

def CreateInstructions():
	if Language == 'EN':
		return CreateEnglishInstructions()
	elif Language == 'DA':
		return CreateDanishInstructions()
	elif Language == 'IT':
		return CreateItalianInstructions()
	else:
		return CreateEnglishInstructions()

