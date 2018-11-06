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
    #read from file
    with open(input_file_name) as f:
        for line in f:
            splitted_line = line.split()
            for pair in splitted_line:
                if pair in e_dict:
                    e_dict[pair] += 1
                else:
                    e_dict[pair] = 1
                #split the word to get the count of the pp classication
                splitted_pair = pair.split('/')
                if splitted_pair[-1] in pp_e_dict and splitted_pair[-1] in listOfPossiblePP:
                    pp_e_dict[splitted_pair[-1]] += 1
                elif splitted_pair[-1] in listOfPossiblePP:
                    pp_e_dict[splitted_pair[-1]] = 1
                else:
                    strForOtherStringsTags += ',' + splitted_pair[-1]
                    strForOtherStrings += ',' + splitted_pair[0];
                    pp_e_dict['OTHER'] += 1
    #calculate q interpolated values:
    numOfWords = sum(value for key, value in pp_e_dict.iteritems())
    q_val_dict={}
    count_abc_dict={}
    count_ab_dict={}
    count_bc_dict={}
    count_b_dict = {}
    count_c_dict = {}
    words = ["","",""]
    count = 0
    numOfWords2 = 0
    temp = ""
    #f.close()
    with open(input_file_name) as f:
        for line in f:
            splitted_line = line.split()
            for pair in splitted_line:
                words[count] = pair.split('/')[-1]
                numOfWords2 += 1
                count += 1
                #got 3 words
                if count == 3:
                    #count the 3 words
                    triple = ', '.join(words)
                    if triple in count_abc_dict:
                        count_abc_dict[triple] += 1
                    else:
                        count_abc_dict[triple] = 1
                    #count ab
                    ab = words[0] + ', ' + words[1]
                    if ab in count_ab_dict:
                        count_ab_dict[ab] += 1
                    else:
                        count_ab_dict[ab] = 1
                    #count bc
                    bc = words[1] + ', ' + words[2]
                    if bc in count_bc_dict:
                        count_bc_dict[bc] += 1
                    else:
                        count_bc_dict[bc] = 1
                    #count b
                    b = words[1]
                    if b in count_b_dict:
                        count_b_dict[b] += 1
                    else:
                        count_b_dict[b] = 1
                    #count c
                    c = words[2]
                    if c in count_c_dict:
                        count_c_dict[c] += 1
                    else:
                        count_c_dict[c] = 1

                    #for the next 3 words
                    words[0] = words[1]
                    words[1] = words[2]
                    words[2] = ""
                    count = 2
    #f.close()
    #write to the files:
    e_file_object = open(e_fileName, 'w')
    for key in e_dict:
        temp = key.split('/')
        word = getWordFromPair(key, '/')
        classification = temp[-1]
        s = word + ' ' + classification + '\t' + str(e_dict[key])
        e_file_object.write(s+'\n')
    for key in pp_e_dict:
        s = key + '\t' + str(pp_e_dict[key])
        e_file_object.write(s+'\n')
    #e_file_object.close()
    #write q values:
    q_file_object = open(q_fileName, 'w')
    s = '^numOfWords' + '\t' + str(numOfWords2)
    q_file_object.write(s + '\n')
    for key in count_abc_dict:
        temp = key.split(', ')
        s = temp[0] + ' ' + temp[1] + ' ' + temp[2] + '\t' + str(count_abc_dict[key])
        q_file_object.write(s+'\n')
    for key in count_ab_dict:
        temp = key.split(', ')
        s = temp[0] + ' ' + temp[1] + ' ' + '\t' + str(count_ab_dict[key])
        q_file_object.write(s+'\n')
    for key in count_bc_dict:
        temp = key.split(', ')
        s = temp[0] + ' ' + temp[1] + ' ' + '\t' + str(count_bc_dict[key])
        q_file_object.write(s+'\n')
    for key in count_b_dict:
        s = key + '\t' + str(count_b_dict[key])
        q_file_object.write(s+'\n')
    for key in count_c_dict:
        s = key + '\t' + str(count_c_dict[key])
        q_file_object.write(s+'\n')

    #q_file_object.close()
    return

def getWordFromPair(pair, seperator):
    temp = pair.split(seperator)
    length = len(temp)
    count = 0
    word=""
    while count != length-1:
        word += temp[count]
        count += 1
    return word


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
    #computeQE("/home/efrat/Documents/nlp/ass1/data/ass1-tagger-train", "q.mle", "e.mle")
    computeQE("/home/efrat/Documents/nlp/ass1/data/test", "q.mle", "e.mle")
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