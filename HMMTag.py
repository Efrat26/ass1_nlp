from __future__ import division
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
    pruning_dict = getPruningDict(q_val_dict)
    # read all lines
    f_input = open(input_file_name, 'r')
    lines = f_input.read().split('\n')
    #open output file
    f_output = open(out_file_name, 'w')
    #go over all sentences
    index_of_start = list_of_tags.index('START')
    for i in range(0, len(lines)):
        if i == (len(lines)-1):
            break
        #go over all words in sentence
        col_index = 1
        splitted_line = lines[i].split(' ')
        splitted_line.insert(0, 'start')
        splitted_line.insert(1, 'start')
        result_matrix = numpy.zeros((len(splitted_line)+1, len(list_of_tags), len(list_of_tags)))
        tag_result_matrix = numpy.zeros((len(splitted_line)+1, len(list_of_tags), len(list_of_tags)))
        result_matrix[0, index_of_start, index_of_start] = 1

        #go over the words
        for word in splitted_line:
            for new_tag in list_of_tags:
                index_r_new_tag = list_of_tags_dict[new_tag]
                for prev_prev_tag in list_of_tags:
                    [max_prev_tag_ind, max_res] = findMaxTag(list_of_tags_dict[prev_prev_tag], list_of_tags_dict[new_tag],
                                                         word, q_val_dict, e_val_dict,
                                                         result_matrix, col_index, list_of_tags, pruning_dict, words)
                    result_matrix[col_index, list_of_tags_dict[prev_prev_tag], list_of_tags_dict[new_tag]] = max_res
                    tag_result_matrix[col_index , list_of_tags_dict[prev_prev_tag], list_of_tags_dict[new_tag]] = \
                        max_prev_tag_ind
            col_index += 1
        max_r_ind = 0
        max_t_ind = 0
        max_val = None
        for k in range(0,len(list_of_tags)):
            for m in range(0,len(list_of_tags)):
                if result_matrix[col_index-1, k , m] > max_val:
                    max_val = result_matrix[col_index-1, k , m]
                    max_r_ind=k
                    max_t_ind = m
        splitted_line.pop(0)
        splitted_line.pop(0)
        tags = [None]*len(splitted_line)
        tags [len(splitted_line) -1 ] = list_of_tags[max_r_ind]
        tags[len(splitted_line) - 2] = list_of_tags[max_t_ind]
        tags_indeces =  [None]*len(splitted_line)
        tags_indeces[len(splitted_line) - 1] = max_r_ind
        tags_indeces[len(splitted_line) - 2] = max_t_ind

        for j in range(len(splitted_line) -3, -1, -1):
            tags[j]= (list_of_tags[int((tag_result_matrix[j + 2, tags_indeces[j+1],  tags_indeces[j+2]]))])
            tags_indeces[j] = list_of_tags.index(tags[j])
        for j in range(0, len(splitted_line)):
            if j < (len(splitted_line)-1):
                s = splitted_line[j] + "/" + tags[j]+" "
            else:
                s = splitted_line[j] + "/" + tags[j]+'\n'

            f_output.write(s)


    print 'hey'

def convertListToDict(list_of_tags):
    result = {}
    for i in range(0,len(list_of_tags)):
        result[list_of_tags[i]] = i
    return result


def findMaxTag(prev_prev_tag_index, new_tag_index, word, q_vals, e_vals, matrix, col_ind, list_of_tags, pruning, words):
    temp_res = 0.0
    max_result = None
    index_prev_tag = 0
    #for t_prev_tag in list_of_tags:
    for i in range(0, len(list_of_tags)):
        event = list_of_tags[prev_prev_tag_index] + ' ' + list_of_tags[i] + ' ' + list_of_tags[new_tag_index]
        if event in pruning:
            q_val = MLETrain.computeQ(list_of_tags[new_tag_index], list_of_tags[prev_prev_tag_index], list_of_tags[i], q_vals)
            e_val = MLETrain.computeE(word, list_of_tags[new_tag_index], e_vals, words)
            mat_val = matrix[col_ind - 1, i, prev_prev_tag_index]
            if mat_val <= 0:
                mat_val = 0.000000001
            temp_res = math.log(q_val) + math.log(e_val) + math.log(mat_val)
            if temp_res > max_result:
                max_result = temp_res
                index_prev_tag = i
    return [index_prev_tag, max_result]





def getPruningDict(q_vals_dict):
    pruning = {}
    for key in q_vals_dict:
        splitted_event = key.split(' ')
        if len(splitted_event) == 3:
            if key not in pruning:
                pruning[key] = 1
    return pruning

def main():
    HMMTag('/home/efrat/Documents/nlp/ass1/data/ass1-tagger-test-input (copy)', 'q.mle', 'e.mle', 'output', 'extra')
    GreedyTag.calculateAccuracy('output', '/home/efrat/Documents/nlp/ass1/data/ass1-tagger-test (copy)')
    #HMMTag('/home/efrat/Documents/nlp/ass1/data/ass1-tagger-test-input', 'q.mle', 'e.mle', 'output', 'extra')
    #GreedyTag.calculateAccuracy('output', '/home/efrat/Documents/nlp/ass1/data/ass1-tagger-test')

if __name__ == "__main__":
    main()