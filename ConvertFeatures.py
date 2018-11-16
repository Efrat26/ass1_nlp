#Efrat Sofer, 304855125
STUDENT={'name': 'Efrat Sofer',
         'ID': '304855125'}

def ConvertFeatures(feature_file_name, feature_vec_file, feature_map_file):
    features_dict = {}
    log_linear_output_dict = {}
    extracted_features_file = open(feature_file_name, 'r')
    feature_mapping_file = open(feature_map_file, 'r')
    #read the lines from the mapping and put it in a dict
    feature_mapping_lines = feature_mapping_file.read().split('\n')
    for line in feature_mapping_lines:
        if line != '' or line != '\n':
            splitted_line = line.split(' ')
            if len(splitted_line) != 2:
                print 'length of splitted line isnt 2, line: ' + line
                continue
            features_dict[splitted_line[0]] = splitted_line[1]
    #go over the feature in the feature_file_name and write it in a log linear form:
    extracted_features_lines = extracted_features_file.read().split('\n')
    for i in range(0, len(extracted_features_lines)):
        if i == len(extracted_features_lines)-1:
            break
        output_line = ''
        line_features_dict = {}
        splitted_line = extracted_features_lines[i].split(' ')
        if splitted_line[0] != 'START':
            output_line += features_dict[splitted_line[0]]
        for j in range(1,len(splitted_line)):
            feature = splitted_line[j]
            feature_as_number = features_dict[feature]
            if features_dict[splitted_line[j]] in line_features_dict:
                line_features_dict[feature_as_number] += 1
            else:
                line_features_dict[feature_as_number] = 1
        for key in line_features_dict:
            output_line += ' ' + key + ':' + str(line_features_dict[key])
        log_linear_output_dict[i] = output_line
    #write to file
    written_features = set()
    print 'writing to file'
    log_linear_format_file = open(feature_vec_file, 'w')
    for key in log_linear_output_dict:
        if log_linear_output_dict[key] not in written_features:
            log_linear_format_file.write(log_linear_output_dict[key] + '\n')
            written_features.add(log_linear_output_dict[key])






def main():
    ConvertFeatures('extracted features', 'feature vec file', 'feature map file')

if __name__ == "__main__":
    main()