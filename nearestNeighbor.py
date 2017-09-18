import string
import json
from pprint import pprint
from heapq import nlargest
import difflib
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
import enchant
__author__      = "Fang Jin"
__copyright__   = "Copyright 2015"


d = enchant.Dict("en_us")
#from textblob import TextBlob


exclude = set(string.punctuation)
print exclude

stop1 = set(stopwords.words('english'))
print "***************************************************"
print stop1
NEAREST_NUM = 20 
MID_NUM = NEAREST_NUM/2
print MID_NUM


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
       if realList[i] == 1 and estimationList[i] == 1:
           results[0] = results[0] +1
       elif realList[i] == 1 and estimationList[i] == 0:
           results[1] = results[1] +1
       elif realList[i] == 0 and estimationList[i] == 1:
           results[2] = results[2] +1
       else:
           results[3] = results[3] +1
    
   results[4] = 1.0*results[0]/(results[0]+results[2])
   results[5] = 1.0*results[0]/(results[0]+results[1])
   results[6] = 2.0*results[0]/(2*results[0]+results[2]+results[1])

   return results



def stringProcessing(s):

    # remove punctuations
    s = ''.join(ch for ch in s if ch not in exclude)
    list_of_words = s.split()

    # remove short words
    for w in list_of_words:
        if len(w)<3:
            list_of_words.remove(w)
    
    # remove stop words
    delete_stop_words = [ word for word in list_of_words if word not in stop1 ]

    # rmove non-english words
    filtered_words = [ word for word in delete_stop_words if d.check(word.decode('utf-8')) ]

    return ' '.join(filtered_words)

with open('climate_records.txt', 'r') as f:    
    climate_data = []
    for line in f:
        if line[0] != '#':
            climate_data.append(stringProcessing(line))

with open('non-climate_records.txt', 'r') as f:    
    non_climate_data = []
    for line in f:
        if line[0] != '#':
            non_climate_data.append(stringProcessing(line))



with open('uniqueManuallyLabeledData.txt', 'r') as f:    
    realValue = []
    estimatedValue = []
    for line in f:
        items = line.split()
        if items[0] == 'climate':
            realValue.append(1)
        else:
            realValue.append(0)

        del items[0]
        fn2 = stringProcessing(' '.join(items))
        
        score_climate = []
        for fn1 in climate_data:
            score = difflib.SequenceMatcher(None,fn1,fn2).ratio()
            score_climate.append(score)
        
        score_non_climate = []
        for fn1 in non_climate_data:
            score = difflib.SequenceMatcher(None,fn1,fn2).ratio()
            score_non_climate.append(score)
        
        if nlargest(MID_NUM, score_climate)[MID_NUM-1] > nlargest(MID_NUM, score_non_climate)[MID_NUM-1]:
            estimatedValue.append(1)
        else:
            estimatedValue.append(0)
        
    #print realValue
    #print estimatedValue

    results = resultsAnalyzer(realValue, estimatedValue)
    print "Precision", results[4]
    print "Recall", results[5]
    print "F-measure", results[6]
