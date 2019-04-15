# ############################### #
# kNN_crossValidation.py
# 
# Creates a k-nearest neighbor classifier based on two gene sets using cross validation for accuracy testing.
#
# ONGOING EDITS
# - needs to be made modular
#
# 
# Anna Farrell-Sherman 3/31/19
# ############################### #

from sklearn import neighbors #for the kNN
from sklearn.model_selection import cross_val_score #for cross validation
import pandas as pd #to import the csv datafile
from sklearn.model_selection import GridSearchCV # for parameter estimation
from sklearn.pipeline import Pipeline #to allow for normalization in cross validation
from sklearn.preprocessing import MinMaxScaler #minMax normalization
import numpy as np # to read in length as float64
#from sklearn import metrics

input_file = "CSVs/AvNotA_notNormalized.csv"
#input_file = "CSVs/AB_full.csv"
#kNeighbors = 3

#Set up pipeline
scaler = MinMaxScaler()
clf = neighbors.KNeighborsClassifier(weights='uniform')

pipe = Pipeline([('minMax', scaler), ('clf', clf)])

#create a dictionary of all values we want to test for n_neighbors
param_grid = {'clf__n_neighbors': range(1, 20)}

#use gridsearch to test all values for n_neighbors
#print(sorted(metrics.SCORERS.keys()))
grid = GridSearchCV(pipe, param_grid, cv=5, scoring='f1')

#Set Up data
sequenceFeatureTable = pd.read_csv(input_file, header = 0, dtype={'Length':  np.float64})
seqTarget = sequenceFeatureTable['Class']
seqData = sequenceFeatureTable.drop(columns=['Class'])

#fit model to data
grid.fit(seqData, seqTarget)

#check top performing n_neighbors value
#all results
#print(grid.cv_results_)
#
print("Best Estimator:" + str(grid.best_estimator_))
print("Best Score:" + str(grid.best_score_))
print("Best Params:" + str(grid.best_params_))
print("Best Index:" + str(grid.best_index_))


# from: https://scikit-learn.org/stable/auto_examples/compose/plot_compare_reduction.html#sphx-glr-auto-examples-compose-plot-compare-reduction-py
mean_scores = np.array(grid.cv_results_['mean_test_score'])
# select score for best C
#mean_scores = mean_scores.max(axis=0)
print(mean_scores)





