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

#input_file = "CSVs/AvnotA_featureTable.csv"
input_file = "CSVs/AB_full.csv"
kNeighbors = 3

sequenceFeatureTable = pd.read_csv(input_file, header = 0)
seqTarget = sequenceFeatureTable['Class']
seqData = sequenceFeatureTable.drop(columns=['Class'])


# clf = neighbors.KNeighborsClassifier(kNeighbors, weights='uniform')
# scores = cross_val_score(clf, seqData, seqTarget, cv=5)

# print(seqTarget)
# print(seqData)
# print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))




knn2 = neighbors.KNeighborsClassifier(weights='uniform')

#create a dictionary of all values we want to test for n_neighbors
param_grid = {'n_neighbors': range(1, 20)}

#use gridsearch to test all values for n_neighbors
knn_gscv = GridSearchCV(knn2, param_grid, cv=5, scoring='roc_auc')

#fit model to data
knn_gscv.fit(seqData, seqTarget)

#check top performing n_neighbors value
#all results
#print(knn_gscv.cv_results_)
#
print("Best Estimator:" + str(knn_gscv.best_estimator_))
print("Best Score:" + str(knn_gscv.best_score_))
print("Best Params:" + str(knn_gscv.best_params_))
print("Best Index:" + str(knn_gscv.best_index_))
#X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.75, random_state=42)
