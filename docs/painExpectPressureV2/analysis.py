# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 08:29:18 2023

@author: KristianHennings
"""
import PainExpect as pex

print("Loading test data")
content = pex.loadData("data_julian.json")
subject = 0

learningData = pex.LearningData(content, subject)
learningData.plotTrials()

testData = pex.TestData(content, subject)
testData.plotStatistics()