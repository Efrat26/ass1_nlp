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
    max_t = 0
    max_r = 0
    # read all lines
    f_input = open(input_file_name, 'r')
    lines = f_input.read().split('\n')
    #open output file
    f_output = open(out_file_name, 'w')
    #go over all sentences
    for i in range(0, len(lines)):
        #go over all words in sentence
        col_index = 1
        splitted_line = lines[i].split(' ')
        #go over the words
        for word in splitted_line:
            max_result = 0.0
            temp_res = 0.0
            max_tag = list_of_tags[0]
            result_matrix = numpy.zeros((len(splitted_line)+1, len(list_of_tags), len(list_of_tags)))
            tag_result_matrix = numpy.zeros((len(splitted_line), len(list_of_tags), len(list_of_tags)))
            result_matrix[0, list_of_tags.index('START'), list_of_tags.index('START')] = 1
            for r_new_tag in list_of_tags:
                if r_new_tag == 'START':
                    continue
                for t_prev_prev_tag in list_of_tags:
                    if col_index > 1 and t_prev_prev_tag == 'START':
                        continue
                    for t_prev_tag in list_of_tags:
                        if t_prev_tag == 'START':
                            continue
                        q_val = MLETrain.computeQ(r_new_tag,t_prev_prev_tag,t_prev_tag,q_val_dict)
                        e_val = MLETrain.computeE(word,r_new_tag,e_val_dict,{})
                        mat_val = result_matrix[col_index-1, list_of_tags.index(t_prev_tag), list_of_tags.index(t_prev_prev_tag)]
                        temp_res = math.log(q_val)+ math.log(e_val) + math.log(mat_val)
                        if temp_res > max_result:
                            max_result = temp_res
                            max_prev_tag = t_prev_tag
                            max_r = list_of_tags.index(r_new_tag)
                            max_t = list_of_tags.index(t_prev_prev_tag)
            result_matrix[col_index-1, list_of_tags.index(t_prev_tag), list_of_tags.index(r_new_tag)] = max_result
            tag_result_matrix[col_index - 1, list_of_tags.index(t_prev_prev_tag), list_of_tags.index(r_new_tag)] = list_of_tags.index(max_tag)
            max_result = 0.0
            max_tag = list_of_tags[0]
            col_index += 1
            #print 'max tag for word: ' + word +' is: '+ str(max_tag)

        tags = [max_r, max_t]
        for i in range(len(splitted_line) -3, 1, -1):
            tags.append(tag_result_matrix[i + 2, max_t,  max_r])
        tags = tags.reverse()

    index_of_max_current_tag = 0
    index_of_max_previous_tag = 0
    max_value = 0.0
    temp_value = 0.0
    max_i = 0
    max_j = 0
    for i in range(0,len(list_of_tags)):
        for j in range(0,len(list_of_tags)):
            temp_value = result_matrix[len(lines[i])+1, 0 ,0]
            if temp_value > max_value:
                max_value = temp_value
                max_i = i
                max_j = j
    print 'max probability is: '+ str(max_value) + ' and the tags are: i: '+ list_of_tags[max_i] + ' and j: ' + list_of_tags[max_j]


    print 'max probability is: ' + str()



    print 'hey'

def getScore(word, tage, prev_tag, prev_prev_tag):
    print 'hello'


def main():
    HMMTag('/home/efrat/Documents/nlp/ass1/data/ass1-tagger-test-input', 'q.mle', 'e.mle', 'output', 'extra')


if __name__ == "__main__":
    main()