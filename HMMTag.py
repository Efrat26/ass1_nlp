#Efrat Sofer, 304855125
STUDENT={'name': 'Efrat Sofer',
         'ID': '304855125'}

import MLETrain
import GreedyTag
import numpy
import math
def HMMTag(input_file_name, q_events_file_name, e_events_file_name, out_file_name, extra_file_name):
    #get tag set & do a preprocess on the data given
    q_val_dict = GreedyTag.preprocessForQ(q_events_file_name)
    e_val_dict = GreedyTag.preprocessForE(e_events_file_name)
    list_of_tags = GreedyTag.getTagSet(q_val_dict)
    words = GreedyTag.wordDict(e_val_dict)
    list_of_tags.append('START')
    list_of_tags_dict = convertListToDict(list_of_tags)
    list_of_tags_ind_is_key = convertListToDictWhereKeyIsNum(list_of_tags)
    #pruning_dict = getPruningDict(q_val_dict)
    output_dict = {}
    pruning_e = pruningEVals(e_val_dict)
    # read all lines
    f_input = open(input_file_name, 'r')
    lines = f_input.read().split('\n')
    #go over all sentences
    index_of_start = list_of_tags_dict['START']
    for i in range(0, len(lines)):
        if i == (len(lines) - 1):
            break
        #split the line into words
        splitted_line = lines[i].split(' ')
        splitted_line.insert(0, 'start')
        splitted_line.insert(1, 'start')
        #define the matrices
        V = numpy.full((len(splitted_line)+1, len(list_of_tags), len(list_of_tags)), -999999999999999999999999999999999)
        bp = numpy.zeros((len(splitted_line)+1, len(list_of_tags), len(list_of_tags)))
        #recursion base case
        V[0, index_of_start, index_of_start] = 1
        for j in range(1, len(splitted_line)):
            for tag_key_r in list_of_tags_dict:
                if splitted_line[j] in pruning_e and tag_key_r not in pruning_e[splitted_line[j]]:
                    continue
                for tag_key_t in list_of_tags_dict:
                    [index_prev_tag, max_result] = findMaxTag(tag_key_t, tag_key_r, splitted_line[j], q_val_dict, e_val_dict,
                                                              V, j, list_of_tags_dict, words)
                    V[j, list_of_tags_dict[tag_key_t], list_of_tags_dict[tag_key_r]] = max_result
                    bp[j, list_of_tags_dict[tag_key_t], list_of_tags_dict[tag_key_r]] = index_prev_tag
        #find max sequence of tags
        max_r_ind = 0
        max_t_ind = 0
        max_val = None
        #find the two highest r and t in the last column
        for r in list_of_tags_dict:
            for t in list_of_tags_dict:
                current = V[j, list_of_tags_dict[t], list_of_tags_dict[r]]
                if current == 0:
                    continue
                if current > max_val:
                    max_val = current
                    max_r_ind = list_of_tags_dict[r]
                    max_t_ind = list_of_tags_dict[t]

        result_tags = [None] * len(splitted_line)
        result_tags[len(splitted_line)-1] = max_r_ind
        result_tags[len(splitted_line)-2] = max_t_ind
        for k in range(len(splitted_line) - 3, -1, -1):
            result_tags[k] = int(bp[k+2, result_tags[k+1], result_tags[k+2]])
        splitted_line.pop(0)
        splitted_line.pop(0)
        result_tags.pop(0)
        result_tags.pop(0)
        s = ''
        #write the lines to output:
        for p in range(0, len(splitted_line)):
            if p < (len(splitted_line) - 1):
                s += splitted_line[p] + "/" + list_of_tags_ind_is_key[result_tags[p]] + " "

            else:
                s += splitted_line[p] + "/" + list_of_tags_ind_is_key[result_tags[p]] + '\n'
                output_dict[i] = s

    # open output file
    f_output = open(out_file_name, 'w')
    for key in output_dict:
        f_output.write(output_dict[key])



def convertListToDict(list_of_tags):
    result = {}
    for i in range(0,len(list_of_tags)):
        result[list_of_tags[i]] = i
    return result


def convertListToDictWhereKeyIsNum(list_of_tags):
    result = {}
    for i in range(0,len(list_of_tags)):
        result[i] = list_of_tags[i]
    return result


def findMaxTag(prev_prev_tag, new_tag, word, q_vals, e_vals, matrix, col_ind, dict_tags, words):
    temp_res = 0.0
    max_result = None
    index_prev_tag = 0
    e_val = MLETrain.computeE(word, new_tag, e_vals, words)
    #for t_prev_tag in list_of_tags:
    for tag in dict_tags:
        q_val = MLETrain.computeQ(new_tag, prev_prev_tag, tag, q_vals)
        mat_val = matrix[col_ind - 1, dict_tags[tag], dict_tags[prev_prev_tag]]
        temp_res = math.log(q_val) + math.log(e_val) + mat_val
        #temp_res = q_val*e_val*mat_val
        if temp_res > max_result:
            max_result = temp_res
            index_prev_tag = dict_tags[tag]
    return [index_prev_tag, max_result]


'''
def getPruningDict(q_vals_dict):
    pruning = {}
    #pruning_start_end = {}
    for key in q_vals_dict:
        splitted_event = key.split(' ')
        if len(splitted_event) == 3:
            if key not in pruning:
                pruning[key] = 1
    return pruning
'''


def pruningEVals(e_vals_dict):
    result = {}
    for key in e_vals_dict:
        splitted_key = key.split(' ')
        if len(splitted_key) == 2 and splitted_key[0] in result:
            result[splitted_key[0]].add(splitted_key[1])
        elif len(splitted_key) == 2 and splitted_key[0] not in result:
            l = set()
            l.add(splitted_key[1])
            result[splitted_key[0]] = l

    return result

def main():
    '''
    HMMTag('/home/efrat/Documents/nlp/ass1/data/ass1-tagger-test-input (another copy)', 'q.mle', 'e.mle', 'output', 'extra')
    #print 'number of trigrams passed with pruning: ' + str(num_of_trigrams_pruning)
    #print 'number of trigrams generally: ' + str(general_num_of_trigrams)
    #print 'difference is: ' + str(general_num_of_trigrams - num_of_trigrams_pruning)
    print 'calculating accuracy'
    GreedyTag.calculateAccuracy('output', '/home/efrat/Documents/nlp/ass1/data/ass1-tagger-test (another copy)')
    '''
    HMMTag('/home/efrat/Documents/nlp/ass1/data/ass1-tagger-test-input', 'q.mle', 'e.mle', 'output', 'extra')
    #print 'number of trigrams passed with pruning: ' + str(num_of_trigrams_pruning)
    #print 'number of trigrams generally: ' + str(general_num_of_trigrams)
    #print 'difference is: ' + str(general_num_of_trigrams - num_of_trigrams_pruning)
    print 'calculating accuracy'
    GreedyTag.calculateAccuracy('output', '/home/efrat/Documents/nlp/ass1/data/ass1-tagger-test')
    #'''


if __name__ == "__main__":
    main()