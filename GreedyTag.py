#Efrat Sofer, 304855125
import MLETrain
from itertools import izip
def greedyTag(input_file_name, q_events_file_name, e_events_file_name, out_file_name, extra_file_name):
    #open the file
    q_val_dict = preprocessForQ(q_events_file_name)
    e_val_dict = preprocessForE(e_events_file_name)
    output_tags = []
    words = []
    index_to_add_enter = 0
    needToAddEnter = 0
    len_splitted_line = 0
    with open(input_file_name) as f:
        for line in f:
            splitted_line = line.split(' ')
            for i in range(0, len(splitted_line)):
                if i == 0:
                    len_splitted_line = len(splitted_line)
            #for word in splitted_line:
                last_index = -1
                temp = splitted_line[i]
                temp2 = temp[-1].isalpha()
                last_char = temp[-1]
                if last_char == '\n':
                    temp2 = temp[-2].isalpha()
                    last_char = temp[-2]
                    last_index = -2
                    index_to_add_enter = i+1
                    needToAddEnter = 1
                if not temp2:
                    temp = (splitted_line[i])[:last_index]
                    splitted_line[i] = temp
                    splitted_line.insert(i+1, last_char)

                max_tag = findMaxTag(splitted_line[i], e_val_dict, q_val_dict, output_tags)
                #print 'max value for word: ' + word + '  is: ' + max_tag
                output_tags.append(max_tag)
                words.append(splitted_line[i])
                if(needToAddEnter and i == index_to_add_enter):
                    t = words[-1] + '\n'
                    words[-1] = t
                    needToAddEnter = 0
                if needToAddEnter and index_to_add_enter > len_splitted_line :
                    max_tag = findMaxTag(splitted_line[index_to_add_enter], e_val_dict, q_val_dict, output_tags)
                    # print 'max value for word: ' + word + '  is: ' + max_tag
                    output_tags.append(max_tag)
                    words.append(splitted_line[index_to_add_enter] + '\n')
                    needToAddEnter = 0


    writeToOutput(out_file_name, words, output_tags)


def writeToOutput(outFileName, words, result):
    temp = words
    endsWithEnter=0
    with open(outFileName, 'w') as f:
        for i in range(0, len(temp)):
            if temp[i].endswith('\n'):
                temp[i] = (temp[i])[:-1]
                endsWithEnter = 1
            s = temp[i]+'/'+result[i]+' '
            if endsWithEnter:
                s += '\n'
                endsWithEnter = 0
            f.write(s)


def calculateAccurecy(result_file, real_result_file):
    counter_total = 0.0
    counter_correct = 0.0
    for line_from_my_res, line_from_real_res in izip(open(result_file), open(real_result_file)):
        split_my_res = str(line_from_my_res).split(' ')
        split_real_res = str(line_from_real_res).split(' ')
        for i in range(0, len(split_my_res)):
            if(split_my_res[i] == '\n'):
                continue
            if split_my_res[i] == split_real_res[i]:
                counter_correct += 1
            counter_total += 1
    print 'accuracy result is: ' + str((counter_correct/counter_total)*100)





def findMaxTag (w, e_vals_dict, q_vals_dict, previousTags):
    listOfPossiblePP = ['NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'WP', 'VB', 'VBD', 'VBG', 'VBN', 'VBZ', 'VBP', 'MD', 'TO',
                        'JJ', 'JJR', 'JJS', 'RB', 'RBR','RBS', 'IN', 'WDT', 'DT', 'CC', 'RP', 'PRP$', 'POS', 'WRB',
                        'CD', 'PDT', 'FW', 'EX', 'SYM', 'LS', 'PDT', 'WP$', 'UH', '#', '.', ')', '(', '$', ',', ':',
                        '``', "''"]
    result = 0.0
    max_tag = listOfPossiblePP[0]
    max_result = 0.0
    for tag in listOfPossiblePP:
        if len(previousTags) >= 2:
            result = calculateMaxAccordingToTag(w, tag, previousTags[-2], previousTags[-1], q_vals_dict, e_vals_dict)
            if result > max_result:
                max_result = result
                max_tag = tag
        elif len(previousTags) == 1:
            for possibleTag in listOfPossiblePP:
                result = calculateMaxAccordingToTag(w, tag, previousTags[-1], possibleTag, q_vals_dict,
                                                    e_vals_dict)
                if result > max_result:
                    max_result = result
                    max_tag = tag
        elif len(previousTags) == 0:
            for i in range(0,len(listOfPossiblePP)):
                for j in range(0, len(listOfPossiblePP)):
                    result = calculateMaxAccordingToTag(w, tag, listOfPossiblePP[i], listOfPossiblePP[j], q_vals_dict,
                                                        e_vals_dict)
                    if result > max_result:
                        max_result = result
                        max_tag = tag
    return max_tag




def calculateMaxAccordingToTag(w,new_t,two_before,one_before,q_vals, e_vals):
    resultQ = findQValue(new_t,two_before,one_before, q_vals)
    resultE = findEValue(w, new_t, e_vals)
    return resultE * resultQ

def findEValue(word, tag, e_events_tags):

    result = MLETrain.computeE(word,tag,e_events_tags)
    return result

def findQValue(new_t,two_before,one_before, q_events_dict):
    result = 0.0

    result = MLETrain.computeQ(new_t,two_before,one_before, q_events_dict)
    return result



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
    print 'hello world'
    greedyTag('/home/efrat/Documents/nlp/ass1/data/input test', 'q.mle', 'e.mle', 'output', 'extra')
    calculateAccurecy('output', '/home/efrat/Documents/nlp/ass1/data/test result')
    #greedyTag('/home/efrat/Documents/nlp/ass1/data/ass1-tagger-test-input', 'q.mle', 'e.mle', 'output', 'extra')
    #calculateAccurecy('output', '/home/efrat/Documents/nlp/ass1/data/ass1-tagger-test')
if __name__ == "__main__":
        main()
