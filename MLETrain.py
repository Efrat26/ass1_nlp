#Efrat Sofer, 304855125



def computeQE(input_file_name, q_fileName, e_fileName):
    ####calculate e values
    listOfPossiblePP = {'NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'WP', 'VB', 'VBD', 'VBG', 'VBN', 'VBZ', 'VBP', 'MD', 'TO',
                        'JJ', 'JJR', 'JJS', 'RB', 'RBR','RBS', 'IN', 'WDT', 'DT', 'CC', 'RP', 'PRP$', 'POS', 'WRB',
                        'CD', 'PDT', 'FW', 'EX', 'SYM', 'LS', 'PDT', 'WP$', 'UH', '#', '.', ')', '(', '$', ',', ':',
                        '``', "''", 'OTHER'}
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
    f.close()
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
    f.close()
    #write to the files:
    e_file_object = open(e_fileName, 'w')
    for key in e_dict:
        temp = key.split('/')
        word = getWordFromPair(key, '/')
        classification = temp[-1]
        s = word + ' ' + classification + '\t' + str(e_dict[key])
        e_file_object.write(s+'\n')
    e_file_object.close()
    #write q values:
    q_file_object = open(q_fileName, 'w')
    s = '^numOfWords' + '\t' + str(numOfWords2)
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

    q_file_object.close()
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


'''caculate q value according to the data given in the file q.mle.
    in case one or more (but not all of them) of the denominator is zero then calculate without it.
    in all the denominators are zero, it will return -1
'''
def computeQ(t1, t2, t3):
    #calcute the q values:
    lambda1 = 0.33
    lambda2 = 0.33
    lambda3 = 0.34
    qEventsFileName = 'q.mle'
    #go over the file and find the counts needed
    abc = t1 + ' ' + t2 + ' ' + t3
    ab = t1 + ' ' + t2
    bc = t2 + ' ' + t3
    b = t2
    c = t3
    numOfWords = '^numOfWords'
    values_dict={}
    #initialize values of dictionary
    values_dict[abc] = 0
    values_dict[ab] = 0
    values_dict[bc] = 0
    values_dict[b] = 0
    values_dict[c] = 0
    values_dict[numOfWords] = 0
    counter = 0
    with open(qEventsFileName) as f:
        for line in f:
            splitted_line = line.split('\t')
            if(len(splitted_line) < 2):
                print 'error in splitting line according to \t in q calculation\nline is: ' + line + '\n'
            if (counter == 6):
            #make calculation and return
                break
            if splitted_line[0] == abc:
                values_dict[abc] = int(splitted_line[1])
            elif splitted_line[0] == ab:
                values_dict[ab] = int(splitted_line[1])
            elif splitted_line[0] == bc:
                values_dict[bc] = int(splitted_line[1])
            elif splitted_line[0] == b:
                values_dict[b] = int(splitted_line[1])
            elif splitted_line[0] == c:
                values_dict[c] = int(splitted_line[1])
            elif splitted_line[0]  == numOfWords:
                values_dict[numOfWords] = int(splitted_line[1])

    file.close()
    #handle the different cases that can be
    if(values_dict[ab] > 0 and values_dict[b] >0 and values_dict[numOfWords] >0 ):
        return (lambda1 * (values_dict[abc] / values_dict[ab]) + lambda2 * (values_dict[bc] / values_dict[b]) +
                lambda3 * (values_dict[c] / values_dict[numOfWords]))
    elif values_dict[ab] < 1 and values_dict[b] >0 and values_dict[numOfWords] > 0:
        return (lambda2 * (values_dict[bc] / values_dict[b]) +
                lambda3 * (values_dict[c] / values_dict[numOfWords]))
    elif values_dict[b] < 1 and values_dict[ab] > 0 and values_dict[numOfWords] > 0:
        return (lambda1 * (values_dict[abc] / values_dict[ab]) + lambda3 * (values_dict[c] / values_dict[numOfWords]))
    elif values_dict[numOfWords] < 1 and values_dict[ab] > 0 and values_dict[b] > 0:
        return (lambda1 * (values_dict[abc] / values_dict[ab]) + lambda2 * (values_dict[bc] / values_dict[b]))
    elif values_dict[ab]< 1 and values_dict[b]<1 and values_dict[numOfWords] > 0:
        return lambda3 * (values_dict[c] / values_dict[numOfWords])
    elif values_dict[ab] < 1 and values_dict[numOfWords] < 1 and values_dict[b] > 0:
        return lambda2 * (values_dict[bc] / values_dict[b])
    elif values_dict[b] < 1 and values_dict[numOfWords] < 1 and values_dict[ab] > 0:
        return lambda1 * (values_dict[abc] / values_dict[ab])
    else:
        return -1


def computeE(w, t):
    eEventsFileName = 'e.mle'

def main():
    print("hello world")
   # computeQE("/home/efrat/Documents/nlp/ass1/data/ass1-tagger-train", "e.mle", "q.mle")
    computeQE("/home/efrat/Documents/nlp/ass1/data/test", "e.mle", "q.mle")

if __name__ == "__main__":
        main()