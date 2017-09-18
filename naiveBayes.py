import nltk
import random
from textblob import TextBlob
import string
__author__      = "Fang Jin"
__copyright__   = "Copyright 2015"

LOGISTIC_COEFFICIENT = 1.0

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
    training_dataset_climate = []
    training_dataset_non_climate = []
    noun_dict_climate = {}
    noun_dict_non_climate = {}
    noun_num_climate = 0
    noun_num_non_climate = 0

    for line in training_dataset:
        items = line.split('\t') 
        content = items[-1]
        wiki = TextBlob(content)

        if items[0] == '1':
            training_dataset_climate.append(content)
            for tag in wiki.tags:
                if tag[1] == 'NN'or tag[1] == 'NNS' :
                    noun_num_climate += 1
                    if(tag[0] in noun_dict_climate.keys()):
                        noun_dict_climate[tag[0]] += 1
                    else:
                        noun_dict_climate[tag[0]] = 1
        else:
            training_dataset_non_climate.append(content)
            for tag in wiki.tags:
                if tag[1] == 'NN'or tag[1] == 'NNS' :
                    noun_num_non_climate += 1
                    if(tag[0] in noun_dict_non_climate.keys()):
                        noun_dict_non_climate[tag[0]] += 1
                    else:
                        noun_dict_non_climate[tag[0]] = 1

    realValue = []
    estimationValue = []

    #print noun_num_climate
    #print noun_num_non_climate
    #print noun_dict_climate
    #print noun_dict_non_climate

    for line in testing_dataset:
        items = line.split('\t') 
        content = items[-1]
        wiki = TextBlob(content)
        word_list = []

        for tag in wiki.tags:
            if tag[1] == 'NN'or tag[1] == 'NNS' :
                word_list.append(tag[0])

        if items[0] == '1':
            realValue.append(1)
        else:
            realValue.append(0)


        weight_climate = 0
        weight_non_climate = 0

        for w in word_list:
            if w in noun_dict_climate.keys():
                weight_climate += noun_dict_climate[w]

            if w in noun_dict_non_climate.keys():
                weight_non_climate += noun_dict_non_climate[w]

        prob_climate = 1.0*weight_climate/noun_num_climate
        prob_non_climate = 1.0*weight_non_climate/noun_num_non_climate

        #print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        #print "climate prob: ", prob_climate
        #print "non_climate prob: ", prob_non_climate
        #print '\n'

        if prob_climate > LOGISTIC_COEFFICIENT * prob_non_climate:
            estimationValue.append(1)
        else:
            estimationValue.append(0)

    results = resultsAnalyzer(realValue, estimationValue)
    print 'logistic model results with LOGISTIC_COEFFICIENT = ', LOGISTIC_COEFFICIENT
    print '\tpresion', results[4]
    print '\trecall', results[5]
    print '\tF-measure',results[6]
    print '\taccuracy',results[7]


"""
with open('all_dataset_translated_to_english.txt','r') as f, open('logistic_label_non_english_results.txt','w') as out:
    line_num = 0
    content_prev = ''
    for line in f:
        line_num += 1
        print line_num
        ss = line.decode('utf-8')
        items = ss.split('\t')
        time = items[4][:10]
        country = items[6]

        # since english dataset has been labeled manually, and used as training dataset
        # So, we just ignore english dataset and only lable 'es' and 'pt'
        if(items[0] == 'en'):
            continue

        content = items[1]
        # ingnore short discription
        if len(content) < 5:
            continue
        # delete duplicate description
        elif content == content_prev:
            continue
        else:
            content_prev = content

        wiki = TextBlob(content)
        word_list = []

        for tag in wiki.tags:
            if tag[1] == 'NN'or tag[1] == 'NNS' :
                word_list.append(tag[0])
        
        weight_climate = 0
        weight_non_climate = 0

        for w in word_list:
            if w in noun_dict_climate.keys():
                weight_climate += noun_dict_climate[w]

            if w in noun_dict_non_climate.keys():
                weight_non_climate += noun_dict_non_climate[w]

        prob_climate = 1.0*weight_climate/noun_num_climate
        prob_non_climate = 1.0*weight_non_climate/noun_num_non_climate

        if prob_climate > LOGISTIC_COEFFICIENT * prob_non_climate:
            out.write('climate\t')
        else:
            out.write('non-climate\t')

        out.write(time)
        out.write('\t')
        out.write(country.encode('ascii', 'ignore'))
        out.write('\t')
        out.write(content.encode('ascii', 'ignore'))
        out.write('\n')
"""








