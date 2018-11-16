import MLETrain
#Efrat Sofer, 304855125
STUDENT={'name': 'Efrat Sofer',
         'ID': '304855125'}

def ExtractFeatures(input_file, feature_file_name):
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
        for j in range(0, len(words)):
            event = ''
            if words[j] not in rare_words:
                event += handleNotRareWords(words[j],tags[j])
            else:
                event += handleRareWords(words[j],tags[j])
            event += addEventsForEveryWords(words, tags, j)
            features.append(event)
        feature_dict[i] = features

    print 'writing features to file'
    writeToFile(feature_file_name, feature_dict)


def handleNotRareWords(word,tag):
    event = ' word='+word +' tag='+tag
    return event

def handleRareWords(word, tag):
    suffix =set()
    prefix=set()
    event = ''
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

    event += ' prefix:'
    for p in prefix:
            event+=p+';'
    event += ' suffix:'
    for s in suffix:
        event += s+';'
    if any(c.isdigit() for c in word):
        event += ' containsDigit=' + 'true'
    if '-' in word:
        event += ' containsHyphen=' + 'true'
    if any(c.isupper() for c in word):
        event += ' containsUpperCase='+'true'
    event += ' tag='+tag
    return event


def addEventsForEveryWords(words, tags, word_index):
    event = ''
    if word_index > 0:
        event += ' pt=' + tags[word_index-1]
        event += ' pw='+words[word_index-1]
    if word_index > 1:
        event += ' ppt_pt=' + tags[word_index-2] +';'+tags[word_index-1]
        event += ' ppw=' + tags[word_index-2]
    if word_index <len(words)-1:
        event += ' nw='+words[word_index+1]
    if word_index < len(words)-2:
        event += ' nnw='+words[word_index+2]

    return event

def writeToFile(output_file, output_dict):
    written_lines = {}
    output_file = open(output_file, 'w')
    for key in output_dict:
        features = output_dict[key]
        for feature_line in features:
            if feature_line not in written_lines:
                output_file.write(feature_line + '\n')
                written_lines[feature_line] = 1



def main():
    ExtractFeatures('/home/efrat/Documents/nlp/ass1/data/ass1-tagger-train', 'extracted features')

if __name__ == "__main__":
    main()