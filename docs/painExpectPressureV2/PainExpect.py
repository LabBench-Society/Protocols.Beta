# -*- coding: utf-8 -*-
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def loadData(filename):
    with open(filename, 'r') as file:
        data = json.load(file)

    return data

def calculateIndex(len, period, offset):
    return [period * n + offset for n in range(0, len)]

def pickElements(set, index):
    retValue = []
    
    for s in set:
        retValue.extend([s[n] for n in index])
        
    return retValue

class LearningData:
    def __init__(self, dataset, subject):
        data = dataset['data'][subject]
        LP1 = data['LP1']
        LP2 = data['LP2']
        LP3 = data['LP3']
        LP4 = data['LP4']
        
        self._id = dataset['id'][subject]
        self._high = LP1['annotations']['high']
        self._variant = LP1['annotations']['variant']
        self._cue = LP1['annotations']['cue']
        self._Ntrials = len(self._high) 
        self._BlockSize = int(len(LP1['stimuli'])/6)
        
        index = calculateIndex(self._BlockSize, 6, 2)
        self._stimuli = pickElements([
            LP1['stimuli'], LP2['stimuli'], LP3['stimuli'], LP4['stimuli']
            ], index)

        self._responses = pickElements([
            LP1['responses'], LP2['responses'], LP3['responses'], LP4['responses']
            ], index)
        
        self._trials = pd.DataFrame({
                'order': range(0, len(self._high)),
                'high': self._high,
                'response': self._responses
            })        
        
    def plotTrials(self):
        # Filter DataFrame into two frames one for low cues and one for high cues
        low = self._trials[self._trials['high'] == 0]
        high = self._trials[self._trials['high'] == 1]
        
        # Create scatter plot
        plt.scatter(low['order'], low['response'], label='Low Cue', c='blue')
        plt.scatter(high['order'], high['response'], label='High Cue', c='red')

        # Add labels and legend
        plt.xlabel('Order')
        plt.ylabel('Response')
        plt.title('Learning Task (Subject: {id})'.format(id = self._id))
        
        # Show the plot
        plt.savefig('{id} LearningTask.png'.format(id = self._id), dpi=300)
        self._trials.to_csv('{id} LearningTask.csv'.format(id = self._id), index=False)
        plt.show()

class TestData:
    def __init__(self, dataset, subject):
        data = dataset['data'][subject]
        TP1 = data['TP1']
        TP2 = data['TP2']
        TP3 = data['TP3']
        TP4 = data['TP4']
        TP5 = data['TP5']

        self._id = dataset['id'][subject]
        self._high = TP1['annotations']['high']
        self._correct = TP1['annotations']['correct']
        self._Ntrials = len(self._high) 
        self._BlockSize = int(len(TP1['stimuli'])/8)
        
        index = calculateIndex(self._BlockSize, 8, 2)
        self._stimuli = pickElements([
            TP1['stimuli'], TP2['stimuli'], TP3['stimuli'], TP4['stimuli'], TP5['stimuli']
            ], index)
        
        self._responses = pickElements([
            TP1['responses'], TP2['responses'], TP3['responses'], TP4['responses'], TP5['responses']
            ], index)
        
        self._trials = pd.DataFrame({
                'order': range(0, len(self._high)),
                'high': self._high,
                'correct': self._correct,
                'response': self._responses
            }) 
        
    def printData(self):
        print(self._trials)
        
    def plotStatistics(self):
        # Create a boxplot using seaborn
        custom_palette = {0: 'blue', 1: 'red'}
        sns.boxplot(x='high', y='response', hue='correct', data=self._trials, palette=custom_palette)

        # Add labels and title
        plt.xlabel('High')
        plt.ylabel('Response')
        plt.title('Test Task (Subject: {id})'.format(id = self._id))
        
        # Show the plot
        plt.savefig('{id} TestTask.png'.format(id = self._id), dpi=300)    
        self._trials.to_csv('{id} TestTask.svg'.format(id = self._id), index=False)
        
        plt.show()

def main():
    # Your main code goes here
    print("Loading test data")
    content = loadData("data_julian.json")
    
    learningData = LearningData(content, 2)
    learningData.plotTrials()
    
    testData = TestData(content, 2)
    testData.plotStatistics()
    testData.printData()

# Check if the script is being run as the main program
if __name__ == "__main__":
    # Call the main function
    main()

    