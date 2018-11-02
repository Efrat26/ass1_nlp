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
    strForOtherStringsTags = "";
    strForOtherStrings = "";
    #read from file
    with open (input_file_name) as f:
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

    numOfWords = sum(value for key, value in pp_e_dict.iteritems())
    print numOfWords



    print "hello"


def main():
    print("hello world")
    computeQE("/home/efrat/Documents/nlp/ass1/data/ass1-tagger-train", "a", "b")


if __name__ == "__main__":
        main()