from sklearn.datasets import load_svmlight_file
#Efrat Sofer, 304855125
STUDENT={'name': 'Efrat Sofer',
         'ID': '304855125'}

def TrainSolver(feature_vecs_file, model_file):
    X_train, y_train = load_svmlight_file(feature_vecs_file)
    print 'hey'


def main():
    TrainSolver('empty file', '')


if __name__ == "__main__":
    main()