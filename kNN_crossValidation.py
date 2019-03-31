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

