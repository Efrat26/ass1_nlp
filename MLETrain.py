import sys
#Efrat Sofer, 304855125, orian ezra 315855494
def MLETrain(input_file_name, q_fileName, e_fileName):
    ####calculate e values
    #calculate e value, example: e(book|NN) = count(book,NN)\count(NN) and
    #calculate q values: q(c|a,b) = L1*count(a,b,c)/count(a,b) + L2*count(b,c)/count(b) + L3*count(c)/(num of words)
    e_dict = {} #for each pair (i.e in the example the numerator)
    pp_e_dict={}#for each pair (i.e in the example the denominator)
    signature_dict = {}

    ''' read lines from file and then split it into pairs of 'word/tag' and count it for the e values
    and also count the tag appearances '''
    f = open(input_file_name, 'r')
    lines = f.read().splitlines()
    rare_words = getRareWords(lines)
    start_count = 2*len(lines)
    pairs = []
    for line in lines:
        temp = line.split(' ')
        temp.insert(0, 'start/START')
        temp.insert(1, 'start/START')
        for pair in temp:
            word = getWordFromPair(pair)
            if word != 'start' and word in rare_words:
                t = getTagFromPair(pair, '/')
                signature = sig(word, t)
                if signature in signature_dict:
                    signature_dict[signature] += 1
                else:
                    signature_dict[signature] = 1
            else:
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

    #print 'finished calculating e'
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
        list_of_tags.insert(0, 'START')
        list_of_tags.insert(1, 'START')
        #list_of_tags.insert(len(list_of_tags), 'end')
        #list_of_tags.insert(len(list_of_tags), 'end')
        calculateQValsTriple(list_of_tags, abc_dict)
        calculateQValsDouble(list_of_tags, ab_dict)
        calculateQValsDouble(list_of_tags, bc_dict)
        calculateQValsSingle(list_of_tags, b_dict)
        calculateQValsSingle(list_of_tags, c_dict)
    double_dict_merged = mergeDicts(ab_dict, bc_dict)
    single_dict_merged = mergeDicts(b_dict, c_dict)
    #print 'finished calculating q'
    writeEValsToFile(e_fileName, e_dict, pp_e_dict, signature_dict)
    #print 'finished writing e vals'
    word_count += start_count
    #word_count += start_count
    writeQVals(q_fileName, word_count,abc_dict, double_dict_merged, single_dict_merged, start_count)
    #print 'finished writing q vals'
   # print 'hey'

def getWordFromPair(pair):
    splitted_word = pair.rpartition('/')
    return splitted_word[0]


def sig(w, t):
    if any(c.isdigit() for c in w):
        return '^number ' + t
    elif w.endswith('ing'):
        return '^_ing' + ' ' + t
    elif w.endswith('ed'):
        return '^_ed'+ ' ' + t
    elif w.__len__() > 0 and w[0].isupper():
        return '^Aa' + ' ' + t
    elif '-' in w:
        return '^hasHyphen' + ' ' + t
    else:
        return '^UNK' + ' ' + t




def getRareWords(input_lines):
    seen_words = {}
    rare_words = {}
    for i in range (1, len(input_lines)/2):
        splitted_line = input_lines[i].split(' ')
        for word in splitted_line:
            splitted_word = word.rpartition('/')
            word = splitted_word[0]
            if word not in seen_words:
                seen_words[word] = 1
    for i in range(len(input_lines)/2 +1, len(input_lines)):
        splitted_line = input_lines[i].split(' ')
        for word in splitted_line:
            splitted_word = word.rpartition('/')
            word = splitted_word[0]
            if word not in seen_words:
                rare_words[word] = 1

    return rare_words



def mergeDicts(dict_a, dict_b):
    result = {}
    for key in dict_a:
        if key not in result:
            result[key] = dict_a[key]
        #else:
            #result[key] = dict_a[key]
    for key in dict_b:
        if key not in result:
            result[key] = dict_b[key]
        #else:
           # result[key] = dict_b[key]
    return result

def writeEValsToFile(e_file_name, e_dict_pairs, e_dict, sig_dict):
    f = open(e_file_name, 'w')
    for pair in e_dict_pairs:
        temp = pair.split('/')
        s = temp[0] + ' ' + temp[1] + '\t' + str(e_dict_pairs[pair])
        f.write(s + '\n')
    for key in e_dict:
        s = key + '\t' + str(e_dict[key])
        f.write(s + '\n')
    for key in sig_dict:
        s = key + '\t' + str(sig_dict[key])
        f.write(s + '\n')

def writeQVals(q_file_name, num_of_words, triple_dict, double_dict, single_dict, start_count):
    f = open(q_file_name, 'w')
    list_of_d = [triple_dict, double_dict, single_dict]
    for dictionary in list_of_d:
        for key in dictionary:
            s = key + '\t' + str(dictionary[key])
            f.write(s + '\n')
    s = '^numOfWords' + '\t' + str(num_of_words)
    f.write(s + '\n')


def calculateQValsTriple(listOfTags, q_dict):
    if len(listOfTags) < 3:
        return q_dict
    for i in range(2, len(listOfTags)):
        if i == 2:
            a = listOfTags[i-2]
            b = listOfTags[i-1]
            c = listOfTags[i]
        else:
            a = b
            b = c
            c = listOfTags[i]
        event = a + ' ' + b + ' ' + c
        if event in q_dict:
            q_dict[event] += 1
        else:
            q_dict[event] = 1
    return q_dict


def calculateQValsDouble(list_of_tags, q_val_dict):
    if len(list_of_tags) < 2:
        return q_val_dict
    for i in range(1, len(list_of_tags)):
        if i == 1:
            a = list_of_tags[i-1]
            b = list_of_tags[i]
        else:
            a = b
            b = list_of_tags[i]
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
    min_return_value = 0.000000001
    #calcute the q values:
    lambda1 = 0.15
    lambda2 = 0.25
    lambda3 = 0.6
    #lambda1 = 0.15
    #lambda2 = 0.15
    #lambda3 = 0.7


    #go over the file and find the counts needed
    abc = two_before_new + ' ' + one_before + ' ' + newTag
    ab = two_before_new + ' ' + one_before
    bc = one_before + ' ' + newTag
    b = one_before
    c = newTag
    numOfWords = '^numOfWords'
    events_of_interest = [abc, ab, bc, b, c, numOfWords]
    for event in events_of_interest:
        if str(event) in values_dict:
            continue
        else:
            values_dict[event] = 0

    #handle the different cases that can be
    p1 = 0.0
    p2 = 0.0
    p3 = 0.0


    if values_dict[ab] != 0:
        p1 =  lambda1 * (values_dict[abc] / (values_dict[ab]))
    if values_dict[b] != 0:
        p2 = lambda2 * (values_dict[bc] / (values_dict[b]))
    if values_dict[numOfWords] != 0:
        p3 = lambda3 * (values_dict[c] / values_dict[numOfWords])
    if p1 == p2 == p3 == 0:
        return min_return_value
    return (p1+p2+p3)



'''
compute e value according to the values given in the file e.mle
in case the denominator is zero, it will return 0

w- the word
t - the tag being checked
values_dict - the dictionary with values
'''
def computeE(w, t, values_dict, words_dict):
    min_return_value = 0.000000001
    count_wt = 0.0
    count_t = 0.0
    w_and_t = w + ' ' + t
    events_of_interest = [w_and_t, t]
    for event in events_of_interest:
        if event not in values_dict:
            values_dict[event] = 0
    count_t = float(values_dict[t])
    count_wt = float(values_dict[w_and_t])
    wordInDict = 0
    if w in words_dict:
        wordInDict = 1

    if wordInDict == 0:
        signature = sig(w,t)
        if signature in values_dict:
            count_wt = values_dict[signature]
        else:
            count_wt = 0
        if count_t != 0 and count_wt != 0:
            return (count_wt/count_t)
        else:
            return min_return_value
    if count_t == 0 or count_wt == 0:
        return min_return_value
    else:
        return (count_wt / count_t)

def main():
    if len(sys.argv) != 4:
        print 'needs 3 arguments'
    MLETrain(sys.argv[1], sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    main()