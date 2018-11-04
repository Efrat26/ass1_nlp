#Efrat Sofer, 304855125
import MLETrain
from itertools import izip
def greedyTag(input_file_name, q_events_file_name, e_events_file_name, out_file_name, extra_file_name):
    #open the file
    q_val_dict = preprocessForQ(q_events_file_name)
    e_val_dict = preprocessForE(e_events_file_name)
    output_tags = []
    words = []
    with open(input_file_name) as f:
        for line in f:
            splitted_line = line.split(' ')
            for word in splitted_line:
                max_tag = findMaxTag(word, e_val_dict, q_val_dict, output_tags)
                #print 'max value for word: ' + word + '  is: ' + max_tag
                output_tags.append(max_tag)
                words.append(word)
    writeToOutput(out_file_name, words, output_tags)


def writeToOutput(outFileName, words, result):
    with open(outFileName, 'w') as f:
        for i in range(0, len(words)):
            s = words[i]+'/'+result[i]+' '
            f.write(s)


def calculateAccurecy(result_file, real_result_file):
    counter_total = 0.0
    counter_correct = 0.0
    for line_from_my_res, line_from_real_res in izip(open(result_file), open(real_result_file)):
        split_my_res = str(line_from_my_res).split(' ')
        split_real_res = str(line_from_real_res).split(' ')
        for i in range(0, len(split_my_res) -1):
            if split_my_res[i] == split_real_res[i]:
                counter_correct += 1
            counter_total += 1
    print 'accuracy result is: ' + str((counter_correct/counter_total)*100)





def findMaxTag (w, e_vals_dict, q_vals_dict, previousTags):
    listOfPossiblePP = ['NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'WP', 'VB', 'VBD', 'VBG', 'VBN', 'VBZ', 'VBP', 'MD', 'TO',
                        'JJ', 'JJR', 'JJS', 'RB', 'RBR','RBS', 'IN', 'WDT', 'DT', 'CC', 'RP', 'PRP$', 'POS', 'WRB',
                        'CD', 'PDT', 'FW', 'EX', 'SYM', 'LS', 'PDT', 'WP$', 'UH', '#', '.', ')', '(', '$', ',', ':',
                        '``', "''"]
    max_value = 0.0
    max_tag = listOfPossiblePP[0]
    for tag in listOfPossiblePP:
        resultQ = findQValue(tag, previousTags,q_vals_dict)
        resultE = findEValue(w,tag,e_vals_dict)
        temp = resultE*resultQ
        if temp > max_value:
            max_value = temp
            max_tag = tag
    return max_tag



def findEValue(word, tag, e_events_tags):

    result = MLETrain.computeE(word,tag,e_events_tags)
    return result

def findQValue(tag, previous_tags, q_events_dict):
    result = 0.0
    numOfWords = 40116
    if len(previous_tags) < 2:
        result = MLETrain.computeQ(tag,'JJ', 'NNS', q_events_dict,numOfWords)
    else:
        result = MLETrain.computeQ(tag, previous_tags[-2], previous_tags[-1], q_events_dict,numOfWords)
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
    #greedyTag('/home/efrat/Documents/nlp/ass1/data/input test', 'q.mle', 'e.mle', 'output', 'extra')
    greedyTag('/home/efrat/Documents/nlp/ass1/data/ass1-tagger-test-input', 'q.mle', 'e.mle', 'output', 'extra')
    calculateAccurecy('output', '/home/efrat/Documents/nlp/ass1/data/ass1-tagger-test')
if __name__ == "__main__":
        main()
