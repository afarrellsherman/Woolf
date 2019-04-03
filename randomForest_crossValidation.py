# ############################### #
# randomForest_crossValidation.py
# 
# Creates a k-nearest neighbor classifier based on two gene sets using cross validation for accuracy testing.
#
# ONGOING EDITS
# - needs to be made modular
#
# 
# Anna Farrell-Sherman 3/31/19
# ############################### #

from sklearn.ensemble import RandomForestClassifier #for the randomForestClassifier
from sklearn.model_selection import cross_val_score #for cross validation
import pandas as pd #to import the csv datafile

input_file = "CSVs/AB_full.csv"
nTrees = 10
minLeafSize = 5

sequenceFeatureTable = pd.read_csv(input_file, header = 0)
seqTarget = sequenceFeatureTable['Class']
seqData = sequenceFeatureTable.drop(columns=['Class'])

clf = RandomForestClassifier(n_estimators=nTrees, min_samples_leaf=minLeafSize,random_state=42)
scores = cross_val_score(clf, seqData, seqTarget, cv=5)

print(seqTarget)
print(seqData)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))