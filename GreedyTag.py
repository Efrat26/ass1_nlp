#Efrat Sofer, 304855125
import MLETrain
import time
from itertools import izip
def greedyTag(input_file_name, q_events_file_name, e_events_file_name, out_file_name, extra_file_name):
    #open the file
    q_val_dict = preprocessForQ(q_events_file_name)
    e_val_dict = preprocessForE(e_events_file_name)
    output_tags = []
    words = []
    #read all lines
    f_input = open(input_file_name, 'r')
    lines = f_input.read().split('\n')

    f_output = open(out_file_name, 'w')
    ''' go over the lines and find the max tag for each word'''
    print 'len of lines is: ' + str(len(lines))
    for j in range(0, len(lines)):
    #for line in lines:
        line =[]
        line = lines[j]
        tags = findMaxTag(line,q_val_dict, e_val_dict)
        splitted_line = line.split(' ')
        if j == 1700:
            break
        for i in range(0, len(splitted_line)):
            if i < (len(splitted_line)-1):
                s = splitted_line[i] + "/" + tags[i]+" "
            else:
                s = splitted_line[i] + "/" + tags[i]+'\n'

            f_output.write(s)
        #time.sleep(0.1)
        #f_output.write('\n')

    time.sleep(5)

    #print 'hey'





def findMaxTag(line, q_vals, e_vals):
    list_of_tags = ['NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'WP', 'VB', 'VBD', 'VBG', 'VBN', 'VBZ', 'VBP', 'MD', 'TO',
                        'JJ', 'JJR', 'JJS', 'RB', 'RBR','RBS', 'IN', 'WDT', 'DT', 'CC', 'RP', 'PRP$', 'POS', 'WRB',
                        'CD', 'PDT', 'FW', 'EX', 'SYM', 'LS', 'PDT', 'WP$', 'UH', '#', '.', ')', '(', '$', ',', ':',
                        '``', "''"]
    tags = []
    max_value = 0.0
    temp_res = 0.0
    max_tag = list_of_tags[0]
    tag_before = ''
    two_tags_before = ''
    splitted_line = line.split(' ')
    for word in splitted_line:
         for tag in list_of_tags:
             #if it's the first two tags
                if len(tags) > 2:
                    tag_before = tags[-1]
                    two_tags_before = tags[-2]
                    resultq = MLETrain.computeQ(tag,two_tags_before, tag_before,q_vals)
                    resulte = MLETrain.computeE(word,tag, e_vals)

                elif len(tags) == 0:
                    resultq = MLETrain.computeQ(tag, 'START', 'START', q_vals)
                    resulte = MLETrain.computeE(word, tag, e_vals)
                elif len(tags) == 1:
                    resultq = MLETrain.computeQ(tag, 'START', tags[-1], q_vals)
                    resulte = MLETrain.computeE(word, tag, e_vals)

                temp_res = resulte * resultq
                if temp_res > max_value:
                    max_value = resulte * resultq
                    max_tag = tag
         tags.append(max_tag)
    return tags



def calculateAccuracy(out_file_name, true_res):
    true_res_file = open(true_res, 'r')
    lines_true = true_res_file.read().split('\n')
    time.sleep(2)
    my_res_file = open(out_file_name, 'r')
    lines_my = my_res_file.read().split('\n')
    time.sleep(2)
    count_words = 0
    count_true = 0
    if not(len(lines_true) == (len(lines_my))):
        print 'result files arent the same length'
        return
    for i in range(0, len(lines_true)):
        splitted_line_true = lines_true[i].split(' ')
        splitted_line_my = lines_my[i].split(' ')
        for j in range(0, len(splitted_line_my)):
            temp_true = splitted_line_true[j].split('/')
            temp_my = splitted_line_my[j].split('/')
            if temp_true[-1] == temp_my[-1]:
                count_true += 1
        count_words += len(splitted_line_true)
    result = 0.0
    result = (float(count_true)/float(count_words))
    print 'accuracy results: ' + str(result*100)



def preprocessForQ(qEventsFileName):
    q_events_dict = {}
    with open(qEventsFileName) as f:
        for line in f:
            splitted_line = line.split('\t')
            if (len(splitted_line) < 2):
                print 'error in splitting line according to \t in q calculation\nline is: ' + line + '\n'
                continue
            q_events_dict[splitted_line[0]] = float(splitted_line[1])
    return q_events_dict


def preprocessForE(eEventsFileName):
    e_events_dict = {}
    with open(eEventsFileName) as f:
        for line in f:
            splitted_line = line.split('\t')
            if (len(splitted_line) < 2):
                print 'error in splitting line according to \t in q calculation\nline is: ' + line + '\n'
                continue
            e_events_dict[splitted_line[0]] = float(splitted_line[1])
    return e_events_dict


def main():
    #print 'hello world'
    #greedyTag('/home/efrat/Documents/nlp/ass1/data/input test', 'q.mle', 'e.mle', 'output', 'extra')
    #calculateAccurecy('output', '/home/efrat/Documents/nlp/ass1/data/test result')
    greedyTag('/home/efrat/Documents/nlp/ass1/data/ass1-tagger-test-input', 'q.mle', 'e.mle', 'output', 'extra')
    calculateAccuracy('output', '/home/efrat/Documents/nlp/ass1/data/ass1-tagger-test')
    #calculateAccurecy('output', '/home/efrat/Documents/nlp/ass1/data/ass1-tagger-test')
if __name__ == "__main__":
        main()
