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
    list_of_tags.append('START')
    pruning_dict = getPruningDict(q_val_dict)
    max_t = 0
    max_r = 0
    # read all lines
    f_input = open(input_file_name, 'r')
    lines = f_input.read().split('\n')
    #open output file
    f_output = open(out_file_name, 'w')
    #go over all sentences
    for i in range(0, len(lines)):
        if i == (len(lines)-1):
            break
        #go over all words in sentence
        col_index = 1
        splitted_line = lines[i].split(' ')
        result_matrix = numpy.zeros((len(splitted_line) + 1, len(list_of_tags), len(list_of_tags)))
        tag_result_matrix = numpy.zeros((len(splitted_line), len(list_of_tags), len(list_of_tags)))
        result_matrix[0, list_of_tags.index('START'), list_of_tags.index('START')] = 1
        #go over the words
        for word in splitted_line:
            max_result = -100000000000000000000.0
            temp_res = 0.0
            max_prev_tag = list_of_tags[0]
            for r_new_tag in list_of_tags:
                if r_new_tag == 'START':
                    continue
                for t_prev_prev_tag in list_of_tags:
                    if col_index > 1 and t_prev_prev_tag == 'START':
                        continue
                    for t_prev_tag in list_of_tags:
                        if t_prev_tag == 'START':
                            continue
                        event = t_prev_prev_tag + ' ' + t_prev_tag + ' ' + r_new_tag
                        if event not in pruning_dict:
                            continue
                        q_val = MLETrain.computeQ(r_new_tag,t_prev_prev_tag,t_prev_tag,q_val_dict)
                        e_val = MLETrain.computeE(word,r_new_tag,e_val_dict,{})
                        mat_val = result_matrix[col_index-1, list_of_tags.index(t_prev_tag), list_of_tags.index(t_prev_prev_tag)]
                        if mat_val <= 0:
                            mat_val = 0.000000001
                        temp_res = math.log(q_val)+ math.log(e_val) + math.log(mat_val)
                        if temp_res > max_result:
                            max_result = temp_res
                            max_prev_tag = t_prev_tag
                            #max_r = list_of_tags.index(r_new_tag)
                            #max_t = list_of_tags.index(t_prev_prev_tag)
                    result_matrix[col_index-1, list_of_tags.index(t_prev_prev_tag), list_of_tags.index(r_new_tag)] = max_result
                    tag_result_matrix[col_index - 1, list_of_tags.index(t_prev_prev_tag), list_of_tags.index(r_new_tag)] = list_of_tags.index(max_prev_tag)
                    max_result = -100000000000000000000.0
                    max_prev_tag = list_of_tags[0]
            col_index += 1
            #print 'max tag for word: ' + word +' is: '+ str(max_tag)

        tags = [r_new_tag, max_prev_tag]
        for j in range(len(splitted_line) -3, -1, -1):
            tags.append(list_of_tags[int((tag_result_matrix[j + 2, list_of_tags.index(tags[-1]),  list_of_tags.index(tags[-2])]))])
        tags.reverse()
        for j in range(0, len(splitted_line)):
            if j < (len(splitted_line)-1):
                s = splitted_line[j] + "/" + tags[j]+" "
            else:
                s = splitted_line[j] + "/" + tags[j]+'\n'

            f_output.write(s)


    print 'hey'

def getPruningDict(q_vals_dict):
    pruning = {}
    for key in q_vals_dict:
        splitted_event = key.split(' ')
        if len(splitted_event) == 3:
            if key not in pruning:
                pruning[key] = 1
    return pruning

def getScore(word, tage, prev_tag, prev_prev_tag):
    print 'hello'


def main():
    HMMTag('/home/efrat/Documents/nlp/ass1/data/ass1-tagger-test-input', 'q.mle', 'e.mle', 'output', 'extra')
    GreedyTag.calculateAccuracy('output', '/home/efrat/Documents/nlp/ass1/data/ass1-tagger-test')

if __name__ == "__main__":
    main()