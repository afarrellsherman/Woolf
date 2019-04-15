# ############################### #
# buildWoolf.py
# 
# Script to build a woolf model.
# 
# Anna Farrell-Sherman 11/5/18
# ############################### #


#Things to think about adding:
## a way to choose features

#used to create command line inputs
import argparse

#import needed machine learning packages
from sklearn import neighbors #for the kNN
from sklearn.ensemble import RandomForestClassifier #for the randomforest

import pandas as pd #to import the csv datafile
from sklearn.model_selection import GridSearchCV # for parameter estimation
from sklearn.pipeline import Pipeline #to allow for normalization in cross validation
from sklearn.preprocessing import MinMaxScaler #minMax normalization
import numpy as np # to read in length as float64


class Woolf:
    def __init__ (self, classifierType):
        self.classifierType = classifierType

        ##Default pipeline options
        #Classifiers and Param Grids
        if self.classifierType == 'kNN':
            self.clf = neighbors.KNeighborsClassifier(weights='uniform')
            self.param_grid = {'clf__n_neighbors': range(1, 20)}
        elif self.classifierType == 'fOREST':
            self.clf = RandomForestClassifier(random_state=42)
            self.classifierType = {'clf__n_estimators': range(1, 20), 'clf__min_samples_leaf': range(10, 30, 5)}
        else:
             raise Exception("Unrecognized classifier type: " + self.classifierType)
        #Method to use to scale the data
        self.scaler = MinMaxScaler()
        #scoring metric to use in classifier construction
        self.scoringMetric = 'f1'

    def trainModel(self, inputCSV):
        pipe = Pipeline([('scaler', self.scaler), ('clf', self.clf)])

        #use gridsearch to test all values for n_neighbors
        grid = GridSearchCV(pipe, self.param_grid, cv=5, scoring=self.scoringMetric)

        #Set Up data
        sequenceFeatureTable = pd.read_csv(inputCSV, header = 0, dtype={'Length':  np.float64})
        seqTarget = sequenceFeatureTable['Class']
        seqData = sequenceFeatureTable.drop(columns=['Class'])

        #fit model to data
        grid.fit(seqData, seqTarget)

        return grid


if __name__ == '__main__':

    woolf = None

    parser = argparse.ArgumentParser(description="Create a Woolf Model based a feature table")
    parser.add_argument("featureTable", help="A CSV file containing feature data from a set of sequences")

    #choose machine learning algorithm
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-k", "--kNN", action="store_true")
    group.add_argument("-f", "--randomForest", action="store_true")

    #kNN arguments
    parser.add_argument("-n", "--nNeighbors", type=int, default=3, help="number of neighboors for kNN classifier")

    #random Forest arguments
    parser.add_argument("-t", "--nTrees", type=int, default=5, help="number of trees for random forest classifier")
    parser.add_argument("-l", "--minLeafSize", type=int, default=10, help="minimum size of leaves in each tree of the random forest classifier")

    #add verbose argument
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()

    if args.kNN:
        woolf = Woolf('kNN')
    elif args.randomForest:
        woolf = Woolf('fOREST')
    else:
        print('Please choose either kNN (-k) or Random Forest (-f)')

    if woolf != None:
        print('Building kNN Woolf Model') if args.kNN else print('Building Random Forest Woolf Model')

        results = woolf.trainModel(args.featureTable)

        print("Best Score:" + str(results.best_score_))
        print("Best Params:" + str(results.best_params_))



        
