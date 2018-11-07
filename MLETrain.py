#Efrat Sofer, 304855125



def computeQE(input_file_name, q_fileName, e_fileName):
    ####calculate e values
    listOfPossiblePP = ['NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'WP', 'VB', 'VBD', 'VBG', 'VBN', 'VBZ', 'VBP', 'MD', 'TO',
                        'JJ', 'JJR', 'JJS', 'RB', 'RBR','RBS', 'IN', 'WDT', 'DT', 'CC', 'RP', 'PRP$', 'POS', 'WRB',
                        'CD', 'PDT', 'FW', 'EX', 'SYM', 'LS', 'PDT', 'WP$', 'UH', '#', '.', ')', '(', '$', ',', ':',
                        '``', "''", 'OTHER']
    #calculate e value, example: e(book|NN) = count(book,NN)\count(NN) and
    #calculate q values: q(c|a,b) = L1*count(a,b,c)/count(a,b) + L2*count(b,c)/count(b) + L3*count(c)/(num of words)
    e_dict = {} #for each pair (i.e in the example the numerator)
    pp_e_dict={}#for each pair (i.e in the example the denominator)
    pp_e_dict['OTHER'] = 0
    #strings for PP that are not in the list
    strForOtherStringsTags = ""
    strForOtherStrings = ""

    ''' read lines from file and then split it into pairs of 'word/tag' and count it for the e values
    and also count the tag appearances '''
    f = open(input_file_name, 'r')
    lines = f.read().splitlines()
    pairs = []
    for line in lines:
        temp = line.split(' ')
        for pair in temp:
            pairs.append(pair)
            if pair in e_dict:
                e_dict[pair] += 1
            else:
                e_dict[pair] = 1
            t = getTagFromPair(pair, '/')
            if t is not None:
                if t in pp_e_dict:
                    pp_e_dict[t] += 1
                else:
                    pp_e_dict[t] = 1
    print 'finished calculating e'
    '''calculate the q values'''
    word_count = 0
    abc_dict = {}
    ab_dict = {}
    bc_dict = {}
    b_dict={}
    c_dict = {}

    for line in lines:
        splitted_line = line.split(' ')
        list_of_tags = getListOfTags(splitted_line, '/')
        word_count += len(list_of_tags)
        list_of_tags.insert(0, 'start')
        list_of_tags.insert(1, 'start')
        calculateQValsTriple(list_of_tags, abc_dict)
        calculateQValsDouble(list_of_tags, ab_dict)
        calculateQValsDouble(list_of_tags, bc_dict)
        calculateQValsSingle(list_of_tags, b_dict)
        calculateQValsSingle(list_of_tags, c_dict)
    print 'finished calculating q'
    writeEValsToFile(e_fileName, e_dict, pp_e_dict)
    print 'finished writing e vals'
    writeQVals(q_fileName, word_count,abc_dict, ab_dict, bc_dict, b_dict, c_dict)
    print 'finished writing q vals'
    print 'hey'

def writeEValsToFile(e_file_name, e_dict_pairs, e_dict):
    f = open(e_file_name, 'w')
    for pair in e_dict_pairs:
        temp = pair.split('/')
        s = temp[0] + ' ' + temp[1] + '\t' + str(e_dict_pairs[pair])
        f.write(s + '\n')
    for key in e_dict:
        s = key + '\t' + str(e_dict[key])
        f.write(s + '\n')


def writeQVals(q_file_name, num_of_words, abc_d, ab_d, bc_d, b_d, c_d):
    f = open(q_file_name, 'w')
    list_of_d = [abc_d, ab_d, bc_d, b_d,c_d]
    for dictionary in list_of_d:
        for key in dictionary:
            s = key + '\t' + str(dictionary[key])
            f.write(s + '\n')
    s = '^numOfWords' + '\t' + str(num_of_words)
    f.write(s + '\n')


def calculateQValsTriple(listOfTags, q_dict):
    if len(listOfTags) < 3:
        return q_dict
    for i in range(0, len(listOfTags)-2):
        a = listOfTags[i]
        b = listOfTags[i+1]
        c = listOfTags[i+2]
        event = a + ' ' + ' ' + b + ' ' + c
        if event in q_dict:
            q_dict[event] += 1
        else:
            q_dict[event] = 1
    return q_dict


def calculateQValsDouble(list_of_tags, q_val_dict):
    if len(list_of_tags) < 2:
        return q_val_dict
    for i in range(0, len(list_of_tags) - 1):
        a = list_of_tags[i]
        b = list_of_tags[i+1]
        event = a + ' ' + b
        if event in q_val_dict:
            q_val_dict[event] += 1
        else:
            q_val_dict[event] = 1
    return q_val_dict


def calculateQValsSingle(list_of_tags, q_val_dict):
    if len(list_of_tags) < 1:
        return q_val_dict
    for i in range(0, len(list_of_tags)):
        a = list_of_tags[i]
        if a in q_val_dict:
            q_val_dict[a] += 1
        else:
            q_val_dict[a] = 1
    return q_val_dict

def getListOfTags(word_tag_list, sep):
    result = []
    for pair in word_tag_list:
        temp = pair.split(sep)
        result.append(temp[-1])
    return result


def getTagFromPair(pair, sep):
    splitted_pair = pair.split(sep)
    if splitted_pair != None:
        return splitted_pair[-1]
    else:
        return None

'''calculate q value according to the data given in the file q.mle.
    in case one or more (but not all of them) of the denominator is zero then calculate without it.
    in all the denominators are zero, it will return 0
'''
def computeQ(newTag, two_before_new, one_before, values_dict):
    #calcute the q values:
    lambda1 = 0.33
    lambda2 = 0.33
    lambda3 = 0.34
    qEventsFileName = 'q.mle'
    #go over the file and find the counts needed
    abc = two_before_new + ' ' + one_before + ' ' + newTag
    ab = two_before_new + ' ' + one_before
    bc = one_before + ' ' + newTag
    b = one_before
    c = newTag
    numOfWords = '^numOfWords'
    events_of_interest = [abc, ab, bc, b, c ,numOfWords]
    for event in events_of_interest:
        if event not in values_dict:
            values_dict[event] = 0.0

    #handle the different cases that can be
    result = 0.0
    p1 = 0.0
    p2 = 0.0
    p3 = 0.0
    if values_dict[ab] != 0:
        p1 =  lambda1 * (values_dict[abc] / (values_dict[ab]))
    if values_dict[b] != 0:
        p2 = lambda2 * (values_dict[bc] / (values_dict[b]))
    if values_dict[numOfWords] != 0:
        p3 = lambda3 * (values_dict[c] / values_dict[numOfWords])
    return (p1+p2+p3)

'''
compute e value according to the values given in the file e.mle
in case the denominator is zero, it will return 0
'''
def computeE(w, t, values_dict):
    eEventsFileName = 'e.mle'
    count_wt = 0
    count_t = 0
    w_and_t = w + ' ' + t
    events_of_interest = [w_and_t, t]
    for event in events_of_interest:
        if event not in values_dict:
            values_dict[event] = 0
    count_t = float(values_dict[t])
    count_wt = float(values_dict[w_and_t])
    if(count_t > 1):
        return (count_wt / count_t)
    return 0



def main():
    #print("hello world")
    computeQE("/home/efrat/Documents/nlp/ass1/data/ass1-tagger-train", "q.mle", "e.mle")
    #computeQE("/home/efrat/Documents/nlp/ass1/data/test", "q.mle", "e.mle")
    '''
    q_result = computeQ('WDT', 'CD', 'NNS')
    print 'q result is: '+ str(q_result) + '\n'
    e_result = computeE('stacked', 'VBN')
    print 'e result is: ' + str(e_result) + '\n'
    '''
    '''
    computeQE("/home/efrat/Documents/nlp/ass1/data/test", "q.mle", "e.mle")
    q_result = computeQ('NP', 'NNP', 'P')
    print 'result from compute q is: ' + str(q_result)
    e_result = computeE('this', 'DT')
    print 'result from compute e is: ' + str(e_result)
    '''
if __name__ == "__main__":
        main()