import MLETrain
#Efrat Sofer, 304855125
STUDENT={'name': 'Efrat Sofer',
         'ID': '304855125'}

def ExtractFeatures(input_file, feature_file_name):
    tags_set = set()
    feature_set = set()
    f_input = open(input_file, 'r')
    lines = f_input.read().split('\n')
    rare_words = MLETrain.getRareWords(lines)
    feature_dict = {}
    for i in range(0, len(lines)):
        splitted_line = lines[i].split(' ')
        splitted_line.insert(0, 'start/START')
        splitted_line.insert(1, 'start/START')
        tags = []
        words = []
        features = []
        for word in splitted_line:
            splitted_word = word.rpartition('/')
            tags.append(splitted_word[-1])
            words.append(splitted_word [0])
            if splitted_word[-1] not in tags_set and splitted_word[-1] != '':
                tags_set.add(splitted_word[-1])
        for j in range(0, len(words)):
            event = ''
            if words[j] not in rare_words:
                res_event = handleNotRareWords(words[j],tags[j], feature_set)
                event += res_event
            else:
                res_event= handleRareWords(words[j],tags[j], feature_set)
                event += res_event

            event_res = addEventsForEveryWords(words, tags, j, feature_set)
            event += event_res
            features.append(event)
        feature_dict[i] = features

    print 'writing features to file'
    writeToFile(feature_file_name, feature_dict, feature_set, tags_set)


def handleNotRareWords(word, tag, features_set):
    event = tag + ' word='+word
    features_set.add('word=' + word)
    return event

def handleRareWords(word, tag, features_set):
    suffix = set()
    prefix = set()
    event = ''
    event += tag
    if len(word) >= 4:
        prefix.add(word[0])
        prefix.add(word[0:2])
        prefix.add(word[0:3])
        prefix.add(word[0:4])
        suffix.add(word[-1])
        suffix.add(word[-2:])
        suffix.add(word[-3:])
        suffix.add(word[-4:])
    elif len(word) < 4:
        if len(word) == 1:
            suffix.add(word)
            prefix.add(word)
        elif len(word) == 2:
            prefix.add(word[0])
            prefix.add(word)
            suffix.add(word)
            suffix.add(word[-1])
        elif len(word) == 3:
            prefix.add(word[0])
            prefix.add(word[0:2])
            prefix.add(word)
            suffix.add(word[-1])
            suffix.add(word[-2:])
            suffix.add(word)
    for p in prefix:
        event += ' prefix:'+p
        features_set.add('prefix:'+p)
    for s in suffix:
        event += ' suffix:'+s
        features_set.add('suffix:' + s)
    if any(c.isdigit() for c in word):
        event += ' containsDigit=' + 'true'
        features_set.add('containsDigit=true')
    else:
        event += ' containsDigit=' + 'false'
        features_set.add('containsDigit=false')
    if '-' in word:
        event += ' containsHyphen=' + 'true'
        features_set.add('containsHyphen=true')
    else:
        event += ' containsHyphen=' + 'false'
        features_set.add('containsHyphen=false')
    if any(c.isupper() for c in word):
        event += ' containsUpperCase='+'true'
        features_set.add('containsUpperCase=true')
    else:
        event += ' containsUpperCase=' + 'false'
        features_set.add('containsUpperCase=false')
    return event


def addEventsForEveryWords(words, tags, word_index, features_set):
    event = ''
    if word_index > 0:
        event += ' pt=' + tags[word_index-1]
        event += ' pw='+words[word_index-1]
        features_set.add('pt=' + tags[word_index-1])
        features_set.add('pw=' + words[word_index - 1])
    if word_index > 1:
        event += ' ppt_pt=' + tags[word_index-2] +';'+tags[word_index-1]
        event += ' ppw=' + tags[word_index-2]
        features_set.add('ppt_pt=' + tags[word_index-2] +';'+tags[word_index-1])
        features_set.add('ppw='+ tags[word_index-2])
    if word_index <len(words)-1:
        event += ' nw='+words[word_index+1]
        features_set.add('nw='+words[word_index+1])
    if word_index < len(words)-2:
        event += ' nnw='+words[word_index+2]
        features_set.add('nnw='+words[word_index+2])
    return event

def writeToFile(feature_file, feature_lines_dict,  feature_set, tags):
    written_lines = {}
    counter = 1

    feature_lines_output_file = open(feature_file, 'w')
    feature_vec_file = open('feature vec file', 'w')
    feature_map_file = open('feature map file', 'w')
    for key in feature_lines_dict:
        features = feature_lines_dict[key]
        for feature_line in features:
            if feature_line not in written_lines:
                feature_lines_output_file.write(feature_line + '\n')
                written_lines[feature_line] = 1

    for tag in tags:
        feature_vec_file.write(tag+'\n')
        feature_map_file.write(tag + ' ' + str(counter) + '\n')
        counter += 1
    for feature in feature_set:
        feature_vec_file.write(feature + '\n')
        feature_map_file.write(feature + ' ' + str(counter) + '\n')
        counter += 1



def main():
    ExtractFeatures('/home/efrat/Documents/nlp/ass1/data/ass1-tagger-train', 'extracted features')

if __name__ == "__main__":
    main()