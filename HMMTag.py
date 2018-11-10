#Efrat Sofer, 304855125
STUDENT={'name': 'Efrat Sofer',
         'ID': '304855125'}
import MLETrain
import GreedyTag

def HMMTag(input_file_name, q_events_file_name, e_events_file_name, out_file_name, extra_file_name):
    #get tag set & do a preprocess on the data given
    q_val_dict = GreedyTag.preprocessForQ(q_events_file_name)
    e_val_dict = GreedyTag.preprocessForE(e_events_file_name)
    list_of_tags = GreedyTag.getTagSet(q_val_dict)
    # read all lines
    f_input = open(input_file_name, 'r')
    lines = f_input.read().split('\n')
    dims = [len(lines)-2, len(list_of_tags), len(list_of_tags)]
    n = 4
    y = [[[] for i in range(n)] for i in range(n)]
   # output[len(lines) - 2][len(list_of_tags)][len(list_of_tags)]
    print 'hello'

def getScore(word, tage, prev_tag, prev_prev_tag):



def main():
    HMMTag('/home/efrat/Documents/nlp/ass1/data/ass1-tagger-test-input', 'q.mle', 'e.mle', 'output', 'extra')


if __name__ == "__main__":
    main()