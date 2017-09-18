from sklearn import linear_model
import numpy as np
from sklearn import svm
from nltk.corpus import stopwords
import random
from textblob import TextBlob
import string
import enchant
d = enchant.Dict("en_us")
exclude = set(string.punctuation)
#print exclude
STOP = stopwords.words("english")
#print STOP

__author__      = "Fang Jin"
__copyright__   = "Copyright 2015"

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


# english_dataset are all english language, which have been labeled manually
with open('english_dataset.txt', 'r') as f:
    text = []
    for line in f:
        text.append(line.decode('utf-8'))

    random.shuffle(text)
    dataset_num = len(text)

    training_dataset = text[:int(dataset_num*0.7)]
    testing_dataset = text[int(dataset_num*0.7)+1:]
    word_dict = {}

    for line in training_dataset:
        items = line.split('\t') 
        content = items[-1]
        content_no_punctuation = ''

        for c in content:
            if 'A'<= c and c <= 'Z':
                content_no_punctuation += c
            elif 'a' <= c and c <= 'z':
                content_no_punctuation += c
            else:
                content_no_punctuation += ' '

        words = content_no_punctuation.lower().split()

        for w in words:
            if w not in STOP and d.check(w) and len(w)>2:
                if w in word_dict.keys():
                    word_dict[w] += 1
                else:
                    word_dict[w] = 1

    print len(word_dict)

    #word_freq_threshold = 1

    #for key in word_dict.keys():
    #    if word_dict[key] < word_freq_threshold:
    #        del word_dict[key]

    #print len(word_dict)

    word_num = 0
    word_list = []

    for key in word_dict.keys():
        word_num += word_dict[key]
        word_list.append(key)

    print word_num
    word_list.sort()
    #print word_list
    #print weight_list

    X = []
    Y = []

    for line in training_dataset:
        items = line.split('\t') 
        content = items[-1]
        content_cleaned = ''

        for c in content:
            if 'A'<= c and c <= 'Z':
                content_cleaned += c
            elif 'a' <= c and c <= 'z':
                content_cleaned += c
            else:
                content_cleaned += ' '

        words = content_cleaned.lower().split()
        x = []

        for w in word_list:
            x.append(0)

        for w in words:
            if w in word_list:
                idx = word_list.index(w)
                x[idx] = word_dict[key]

        X.append(x)

        if items[0] == '1':
            Y.append(1)
        else:
            Y.append(0)

    logreg = linear_model.LogisticRegression(C=1e5)
    # we create an instance of Neighbours Classifier and fit the data.
    logreg.fit(X, Y)

    realValue = []
    estimationValue = []

    for line in testing_dataset:
        items = line.split('\t') 
        content = items[-1]
        content_cleaned = ''

        for c in content:
            if 'A'<= c and c <= 'Z':
                content_cleaned += c
            elif 'a' <= c and c <= 'z':
                content_cleaned += c
            else:
                content_cleaned += ' '

        words = content_cleaned.lower().split()
        x = []

        for w in word_list:
            x.append(0)

        for w in words:
            if w in word_list:
                idx = word_list.index(w)
                x[idx] = word_dict[key]

        xArray = np.asarray(x)
        #estimationValue.append(clf.predict(xArray.reshape(1,-1))[0])
        estimationValue.append(logreg.predict(xArray.reshape(1,-1))[0])

        if items[0] == '1':
            realValue.append(1)
        else:
            realValue.append(0)

    results = resultsAnalyzer(realValue, estimationValue)
    print 'Logistic Model results: '
    print '\tprecision', results[4]
    print '\trecall', results[5]
    print '\tF-measure',results[6]
    print '\taccuracy',results[7]

    # lable all the dataset 
    with open('all_dataset_translated_to_english.txt','r') as f, open('real_logistic_label_non_english_results.txt','w') as out:
        line_num = 0
        for line in f:
            line_num += 1
            print line_num
            ss = line.decode('utf-8')
            items = ss.split('\t')
    
            # since english dataset has been labeled manually, and used as training dataset
            # So, we just ignore english dataset and only lable 'es' and 'pt'
            if(items[0] == 'en'):
                continue
    
            content = items[1]
            # ingnore short discription
            if len(content) < 5:
                continue
            ## delete duplicate description
            #elif content == content_prev:
            #    continue
            #else:
            #    content_prev = content
    
            content_cleaned = ''
    
            for c in content:
                if 'A'<= c and c <= 'Z':
                    content_cleaned += c
                elif 'a' <= c and c <= 'z':
                    content_cleaned += c
                else:
                    content_cleaned += ' '
    
            words = content_cleaned.lower().split()
            x = []
    
            for w in word_list:
                x.append(0)
    
            for w in words:
                if w in word_list:
                    idx = word_list.index(w)
                    x[idx] = word_dict[key]
    
            xArray = np.asarray(x)
            #estimationValue.append(clf.predict(xArray.reshape(1,-1))[0])
    
            if (logreg.predict(xArray.reshape(1,-1))[0] == 1):
                print line_num
                print "climate"
                out.write('climate\t')
            else:
                out.write('non-climate\t')
    
            out.write(line)
    
