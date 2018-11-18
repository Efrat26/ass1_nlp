import pickle
import ExtractFeatures
import MLETrain
import ConvertFeatures
import GreedyTag
import array
#Efrat Sofer, 304855125
STUDENT={'name': 'Efrat Sofer',
         'ID': '304855125'}

def GreedyMaxEntTag(input_file_name, model_name, feature_map_file, out_file_name):
    #extract features from feature_map_file
    feature_count_dict = {}
    # read the feature mapping
    feature_mapping_file = open(feature_map_file, 'r')
    features_dict = {}
    # open the file and extract all values
    feature_mapping_lines = feature_mapping_file.read().split('\n')
    for line in feature_mapping_lines:
        if line != '' or line != '\n':
            splitted_line = line.split(' ')
            if len(splitted_line) != 2:
                # print 'length of splitted line isnt 2, line: ' + line
                continue
            features_dict[splitted_line[0]] = splitted_line[1]

    #get list of tags
    list_of_tags = ['NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'WP', 'VB', 'VBD', 'VBG', 'VBN', 'VBZ', 'VBP', 'MD', 'TO',
                    'JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS', 'IN', 'WDT', 'DT', 'CC', 'RP', 'PRP$', 'POS', 'WRB',
                    'CD', 'PDT', 'FW', 'EX', 'SYM', 'LS', 'WP$', 'UH', '#', '.', ')', '(', '$', ',', ':',
                    '``', "''"]
    result_dict = {}
    #load the model
    loaded_model = pickle.load(open(model_name, 'rb'))

    #open the file and read the lines
    f_input = open(input_file_name, 'r')
    lines = f_input.read().split('\n')
    #get rare words
    rare_words = MLETrain.getRareWords(lines)
    max_result = 0.0
    max_label = None
    for i in range(0, len(lines)):
        if i == len(lines)-1:
            break
        #split line according to space
        words = lines[i].split(' ')
        words.insert(0, 'start')
        words.insert(1, 'start')
        tags = []

        #go over the words
        for j in range(0, len(words)):
            max_result = 0.0
            max_label = None
            for tag in list_of_tags:
                #extract features for the word:
                event = ''
                if words[j] in rare_words:
                    event += ExtractFeatures.handleRareWords(words[j], '', set())
                else:
                    event += ExtractFeatures.handleNotRareWords(words[j], '', set())
                event += ExtractFeatures.addEventsForEveryWords(words,tags , j, set())
                #convert features to numbers according to feature map
                converted_feature = ConvertFeatures.ConvertFeaturesFromSentence(event, feature_map_file, tag, features_dict)
                #insert to the trained model
                result = loaded_model.predict([converted_feature])
                print result
                if result > max_result:
                    max_result = result
                    max_label = tag
                #check if it's bigger than
                #print 'hello'
            tags.insert(j, max_label)

        sentence = createSentence(words[2:], tags[2:])
        result_dict[i] = sentence
    writeToOutputFile(result_dict, len(lines), out_file_name)


    print 'hello'


def createSentence(words, tags):
    sentence = ''
    for i in range(0,len(words)):
        if i < len(words) -1:
            sentence += words[i] + '/' + tags[i] + ' '
        else:
            sentence += words[i] + '/' + tags[i] + '\n'
    return sentence

def writeToOutputFile(result_dict, len_lines, out_file_name):
    f_output = open(out_file_name, 'w')
    for i in range(0,len_lines):
        f_output.write(result_dict[i])

def main():
    GreedyMaxEntTag('/home/efrat/Documents/nlp/ass1/data/ass1-tagger-test-input', 'model_file', 'feature map file', 'output_greedy_memm')
    GreedyTag.calculateAccuracy('output_greedy_memm', '/home/efrat/Documents/nlp/ass1/data/ass1-tagger-test')


if __name__ == "__main__":
    main()