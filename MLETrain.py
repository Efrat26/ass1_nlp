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
    with open(input_file_name) as f:
        for line in f:
            splitted_line = line.split()
            for pair in splitted_line:
                words[count] = getWordFromPair(pair, '/')
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
    #calcute the q values:
    lambda1 = 0.33
    lambda2 = 0.33
    lambda3 = 0.34

    for key, value in count_abc_dict.iteritems():
        temp = key.split(", ")
        ab = temp[0] + ', ' + temp[1]
        bc = temp[1] + ', ' + temp[2]
        newKey = temp[2]+'|' + temp[0] + ', ' + temp[1]
        q_val_dict[newKey] = lambda1*(count_abc_dict[key]/count_ab_dict[ab]) + \
                             lambda2*(count_bc_dict[bc]/count_b_dict[temp[1]]) + lambda3*(count_c_dict[temp[2]]/numOfWords2)


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

def main():
    print("hello world")
   # computeQE("/home/efrat/Documents/nlp/ass1/data/ass1-tagger-train", "a", "b")
    computeQE("/home/efrat/Documents/nlp/ass1/data/test", "a", "b")

if __name__ == "__main__":
        main()