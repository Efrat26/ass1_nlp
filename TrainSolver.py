from sklearn.datasets import load_svmlight_file
from sklearn import linear_model
import pickle
#Efrat Sofer, 304855125
STUDENT={'name': 'Efrat Sofer',
         'ID': '304855125'}

def TrainSolver(feature_vecs_file, model_file):
    #train

    X_train, y_train = load_svmlight_file(feature_vecs_file)
    #regr = linear_model.LinearRegression()
    print 'train model'
    clf = linear_model.SGDClassifier(max_iter=1000)
    clf.fit(X_train, y_train)
    print 'serialize model'
    pickle.dump(clf, open(model_file, 'wb'))

    #regr.fit(X_train, y_train)
    '''
    #write to file
    model_f = open(model_file, 'w')
    model_x = open('model_x', 'w')
    model_y = open('model_y', 'w')
    print 'writing x train'

    for x in X_train:
        model_f.write(str(x))
        model_x.write(str(x))
    print 'writing y train'
    for y in y_train:
        model_f.write(str(y))
        model_y.write(str(y))

'''
def main():
    TrainSolver('feature vec file', 'model_file')


if __name__ == "__main__":
    main()


