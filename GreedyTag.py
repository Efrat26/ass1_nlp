#Efrat Sofer, 304855125
import MLETrain
def greedyTag(input_file_name, q, e, out_file_name, extra_file_name):
    #open the file
    '''
    with open(input_file_name) as f:
        for line in f:
            splitted_line = line.split(' ')
    '''
    q_val_dict = preprocessForQ(q)
    e_val_dict = preprocessForE(e)
    q_result = MLETrain.computeQ('NP', 'NNP', 'P', q_val_dict)
    print 'result from compute q is: ' + str(q_result)
    e_result = MLETrain.computeE('this', 'DT', e_val_dict)
    print 'result from compute e is: ' + str(e_result)


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
    greedyTag('/home/efrat/Documents/nlp/ass1/data/test', 'q.mle', 'e.mle', 'output', 'extra')

if __name__ == "__main__":
        main()
