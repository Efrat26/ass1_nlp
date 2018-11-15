#Efrat Sofer, 304855125
STUDENT={'name': 'Efrat Sofer',
         'ID': '304855125'}

def FeatureExtraction(input_file, feature_file_name):
    f_input = open(input_file, 'r')
    lines = f_input.read().split('\n')
    feature_dict = {}
    for i in range(0, len(lines)):
        splitted_line = lines[i].split(' ')
        splitted_line.insert(0, 'start/START')
        splitted_line.insert(1, 'start/START')
        tags = []
        words = []
        for word in splitted_line:
            splitted_word = word.rpartition('/')
            tags.append(splitted_word[-1])
            words.append(splitted_line[0])
        for j in range(0, len(words)):
            event = tags[j] + ' form=' +words[j]
            if j > 0:
                event += ' pt=' + tags[j-1]
            if j < (len(words)-1):
                event += ' nt=' + tags[j+1]
            if words[j].endswith('ing') or words[j].endswith('ial'):
                event += ' suff=' +words[j][:]



def main():
    FeatureExtraction('/home/efrat/Documents/nlp/ass1/data/ass1-tagger-train', 'extracted features')

if __name__ == "__main__":
    main()