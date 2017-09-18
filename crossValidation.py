import matplotlib.pyplot as plt
import numpy as np
import random
import json
import sys
__author__      = "Fang Jin"
__copyright__ = "Copyright 2015"

#1: climate, 0: non-climate
def resultsAnalyzer(realList, estimationList):
    if (len(realList)!=len(estimationList)):
        return


    # results[0] : TP
    # results[1] : FN
    # results[2] : FP
    # results[3] : TN
    # results[4] : Precision
    # results[5] : Recall
    # results[6] : F_measure

    results = [0,0,0,0,0,0,0]

    for i in range(len(realList)):
        if realList[i] == 1 and estimationList[i] == 1 :
            results[0] = results[0] +1
        elif realList[i] == 1 and estimationList[i] == 0 :
            results[1] = results[1] +1
        elif realList[i] == 0 and estimationList[i] == 1 :
            results[2] = results[2] +1
        else:
            results[3] = results[3] +1

    results[4] = 1.0*results[0]/(results[0]+results[2])
    results[5] = 1.0*results[0]/(results[0]+results[1])
    results[6] = 2.0*results[0]/(2*results[0]+results[2]+results[1])
    
    return results



text =[]
with open('uniqueManuallyLabeledData.txt','r') as f:
#with open('manually_labelled_results.txt','r') as f:
    for line in f:
        text.append(line)

#shuffle items in text list
random.shuffle(text)
itemNum = len(text)
oneSectionNum = itemNum/10
print oneSectionNum

#dupilicate the text for cross validation
text = text + text
resultsList = []

for i in range(10):
    print i
    trainingSet = text[i*oneSectionNum:(i+7)*oneSectionNum-1]
    testingSet = text[(i+7)*oneSectionNum:(i+10)*oneSectionNum-1]

    testingList = []
    estimationList = []

    climateNum = 0.0
    climateProb = 0.0
    for item in trainingSet:
        words = item.split()
        if words[0] == 'climate':
            climateNum = climateNum + 1

    climateProb = climateNum/(7*oneSectionNum)

    #random assign

    for item in testingSet:
        if item.split()[0] == 'climate':
            testingList.append(1)
        else:
            testingList.append(0)

        if random.random() < climateProb:
            estimationList.append(1)
        else:
            estimationList.append(0)

    resultsList.append(resultsAnalyzer(testingList, estimationList))


precision = []
recall = []
F_measure = []

for item in resultsList:
    precision.append(item[4])
    recall.append(item[5])
    F_measure.append(item[6])

print "prcesion: ", sum(precision)/len(precision)
print "recall: ", sum(recall)/len(recall)
print "F-measure: ", sum(F_measure)/len(F_measure)

xIndex = range(10)
print xIndex




plt.plot(xIndex,precision, label='Precision')
plt.plot(xIndex,recall, label='Recall')
plt.plot(xIndex,F_measure, label='F_measure')
plt.grid(True)
plt.legend()
plt.xlabel('iteration')
plt.title('randomly assign preformance')
plt.show()








