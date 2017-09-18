import string
import enchant
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import random
import difflib
from heapq import nlargest
from textblob import TextBlob

__author__      = "Fang Jin"
__copyright__   = "Copyright 2015"

lmtzr = WordNetLemmatizer()

exclude = set(string.punctuation)
stop_words = set(stopwords.words('english'))
english_words = enchant.Dict("en_us")

NEAREST_NUM = 30
MID_NUM = NEAREST_NUM/2
threshold = 5


def purifyString(s):

    # remove punctuations
    s = ''.join(ch for ch in s if ch not in exclude)
    s = ''.join(ch for ch in s if not ch.isdigit())
    
    # remove short words
    list_of_words = s.split()
    for w in list_of_words:
        if len(w)<3:
             list_of_words.remove(w)
    
    # remove stop words
    delete_stop_words = [ word for word in list_of_words if word.lower() not in stop_words ]
    
    # rmove non-english words
    filtered_words = [ word.lower() for word in delete_stop_words if english_words.check(word.decode('utf-8')) ]

    #filtered_words_2 = [ lmtzr.lemmatize(word) for word in filtered_words ]
    
    return ' '.join(filtered_words)


def randomAssign(prob):
    if random.random() < prob:
        return True
    else:
        return False


def resultsAnalyzer(realList, estimationList):
    if (len(realList) != len(estimationList)):
        return
     
    # results[0] : TP
    # results[1] : FN
    # results[2] : FP
    # results[3] : TN
    # results[4] : Precision
    # results[5] : Recall
    # results[6] : F_measure
    # results[7] : Accuracy
    
    results = [0,0,0,0,0,0,0,0]
    
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
    results[7] = 1.0*(results[0]+results[3])/(results[0]+results[1]+results[2]+results[3])
    return results


with open('english_dataset.txt', 'r') as f:
    climate_num = 0
    non_climate_num = 0
    text = []
    for line in f:
        text.append(line.decode('utf-8'))

    random.shuffle(text)
    data_num = len(text)
    training_dataset = text[:int(data_num*0.7)]
    testing_dataset = text[int(data_num*0.7)+1:]
    training_dataset_climate = []
    training_dataset_non_climate = []

    for line in training_dataset:
        items = line.split('\t') 
        if items[0] == '1':
            training_dataset_climate.append(items[-1])
        else:
            training_dataset_non_climate.append(items[-1])

    prob = 1.0*len(training_dataset_climate)/len(training_dataset)

    realValue = []
    estimationValue = []

    training_num = min(len(training_dataset_climate),len(training_dataset_non_climate))
    training_dataset_climate_knn = training_dataset_climate[0:training_num-1]
    training_dataset_non_climate_knn = training_dataset_non_climate[0:training_num-1]

    # Majority assign
    for line in testing_dataset:
        items = line.split('\t')
        if items[0] == '1':
            realValue.append(1)
        else:
            realValue.append(0)

        if randomAssign(prob):
            estimationValue.append(1)
        else:
            estimationValue.append(0)

    results = resultsAnalyzer(realValue, estimationValue)
    print "Majority assign results"
    print '\tpresion', results[4]
    print '\trecall', results[5]
    print '\tF-measure',results[6]
    print '\taccuracy',results[7]

    # knn
    estimationValue = []
    for line in testing_dataset:
        line = line.encode('ascii', 'ignore')
        items = line.split('\t')
        fn2 = purifyString(items[-1])

        score_climate = []
        score_non_climate = []

        for data in training_dataset_climate_knn:
            data = data.encode('ascii', 'ignore')
            fn1 = purifyString(data)
            score = difflib.SequenceMatcher(None,fn1,fn2).ratio()
            score_climate.append(score)

        for data in training_dataset_non_climate_knn:
            data = data.encode('ascii', 'ignore')
            fn1 = purifyString(data)
            score = difflib.SequenceMatcher(None,fn1,fn2).ratio()
            score_non_climate.append(score)

        if nlargest(NEAREST_NUM, score_climate)[MID_NUM-1 + threshold] > nlargest(NEAREST_NUM, score_non_climate)[MID_NUM-1]:
            estimationValue.append(1)
        else:
            estimationValue.append(0)

    results = resultsAnalyzer(realValue, estimationValue)
    print "KNN results with K: ", NEAREST_NUM, "\tthreshold: ", threshold
    print '\tpresion', results[4]
    print '\trecall', results[5]
    print '\tF-measure',results[6]
    print '\taccuracy',results[7]




    









