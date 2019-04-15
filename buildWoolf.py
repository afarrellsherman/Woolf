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
#import functions from other WoolfModel files
from calculateFeatures import featureTablefromFASTA
#import needed machine learning packages
from sklearn import neighbors #for the kNN
from sklearn.ensemble import RandomForestClassifier #for the randomforest

import pandas as pd #to import the csv datafile
from sklearn.model_selection import GridSearchCV # for parameter estimation
from sklearn.pipeline import Pipeline #to allow for normalization in cross validation
from sklearn.preprocessing import MinMaxScaler #minMax normalization
import numpy as np # to read in length as float64


def buildModel(classifierType, inputCSV):

    #MODEL FUNCTIONS THAT IT MIGHT BE USEFUL TO CHANGE:
    ## Scaler type
    ## scoring method -- is ROC_AOC okay??
    ## ranges in param_grids
    
	#Pipeline Component #1: Scaler
    scaler = MinMaxScaler() #scaler to normalize the data
    
    #Pipline Component #2: Classifier
    if classifierType == 'kNN':
        clf = neighbors.KNeighborsClassifier(weights='uniform')
        param_grid = {'clf__n_neighbors': range(1, 20)}

    elif classifierType == 'fOREST':
        clf = RandomForestClassifier(random_state=42)
        param_grid = {'clf__n_estimators': range(1, 20), 'clf__min_samples_leaf': range(10, 30, 5)}

    pipe = Pipeline([('minMax', scaler), ('clf', clf)])

    #use gridsearch to test all values for n_neighbors
    grid = GridSearchCV(pipe, param_grid, cv=5, scoring='f1')

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
        woolf = buildModel('kNN', args.featureTable)
    elif args.randomForest:
        woolf = buildModel('fOREST', args.featureTable)
    else:
        print('Please choose either kNN (-k) or Random Forest (-f)')

    if woolf != None:
        print('Building kNN') if args.kNN else print('Building Random Forest')
        print("Best Score:" + str(woolf.best_score_))
        print("Best Params:" + str(woolf.best_params_))
        
