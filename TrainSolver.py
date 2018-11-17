from sklearn.datasets import load_svmlight_file
#Efrat Sofer, 304855125
STUDENT={'name': 'Efrat Sofer',
         'ID': '304855125'}

def TrainSolver(feature_vecs_file, model_file):
    #train
    X_train, y_train = load_svmlight_file(feature_vecs_file)
    #write to file
    model_f = open(model_file, 'w')
    model_x = open('model_x', 'w')
    model_y = open('model_y', 'w')
    print 'writing x train'
    '''
    for x in X_train:
        model_f.write(str(x))
        model_x.write(str(x))
    '''
    print 'writing y train'
    for y in y_train:
        model_f.write(str(y))
        model_y.write(str(y))


def main():
    TrainSolver('feature vec file', 'model_file')


if __name__ == "__main__":
    main()