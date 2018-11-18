import pickle
import ExtractFeatures
import MLETrain
import ConvertFeatures
#Efrat Sofer, 304855125
STUDENT={'name': 'Efrat Sofer',
         'ID': '304855125'}

def GreedyMaxEntTag(input_file_name, model_name, feature_map_file, out_file_name):
    #get list of tags
    list_of_tags = ['NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'WP', 'VB', 'VBD', 'VBG', 'VBN', 'VBZ', 'VBP', 'MD', 'TO',
                    'JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS', 'IN', 'WDT', 'DT', 'CC', 'RP', 'PRP$', 'POS', 'WRB',
                    'CD', 'PDT', 'FW', 'EX', 'SYM', 'LS', 'WP$', 'UH', '#', '.', ')', '(', '$', ',', ':',
                    '``', "''"]
    #load the model
    loaded_model = pickle.load(open(model_name, 'rb'))

    #open the file and read the lines
    label = None
    f_input = open(input_file_name, 'r')
    lines = f_input.read().split('\n')
    #get rare words
    rare_words = MLETrain.getRareWords(lines)
    for i in range(0, len(lines)):
        if i == len(lines)-1:
            break
        #split line according to space
        splitted_line = lines[i].split(' ')
        splitted_line.insert(0, 'start/START')
        splitted_line.insert(1, 'start/START')
        tags = []
        words = []
        features = []
        for word in splitted_line:
            splitted_word = word.rpartition('/')
            tags.append(splitted_word[-1])
            words.append(splitted_word[0])
        #go over the words
        for j in range(0, len(words)):
            for tag in list_of_tags:
                #extract features for the word:
                event = ''
                if words[j] in rare_words:
                    event += ExtractFeatures.handleRareWords(words[j], tag, set())
                else:
                    event += ExtractFeatures.handleNotRareWords(words[j], tag, set())
                event += ExtractFeatures.addEventsForEveryWords(words,list_of_tags[0:j-1] , j, set())
                #convert features to numbers according to feature map
                converted_feature = ConvertFeatures.ConvertFeaturesFromSentence(event, feature_map_file, tag )
                #insert to the trained model
                print 'hello'
                #check if it's bigger than







    print 'hello'

def main():
    GreedyMaxEntTag('/home/efrat/Documents/nlp/ass1/data/ass1-tagger-train', 'model_file', 'feature map file', 'output_greedy_memm')


if __name__ == "__main__":
    main()