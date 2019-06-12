#!/usr/bin/env python3

####################################
#
# test_woolfClassifier.py
# Testing code for the Woolf Pipeline woolfClassifier module
#
####################################

import pytest
from woolf import woolfClassifier
import os.path


def test_buildWoolf_DefaultkNN():
	classifierType = 'kNN'
	scalerString = 'MinMaxScaler'
	cvFolds = 5
	scoringM = 'MCC'
	nNhrs = range(1,20)
	nTrs = range(1,15,2)
	minL = range(10,30,3)

	model = woolfClassifier.buildWoolf(classifierType, scalerString, cvFolds, scoringM, nNhrs, nTrs, minL)
	assert str(type(model)) == "<class 'sklearn.model_selection._search.GridSearchCV'>"

def test_buildWoolf_DefaultRandomForest():
	classifierType = 'fOREST'
	scalerString = 'MinMaxScaler'
	cvFolds = 5
	scoringM = 'MCC'
	nNhrs = range(1,20)
	nTrs = range(1,15,2)
	minL = range(10,30,3)

	model = woolfClassifier.buildWoolf(classifierType, scalerString, cvFolds, scoringM, nNhrs, nTrs, minL)
	assert str(type(model)) == "<class 'sklearn.model_selection._search.GridSearchCV'>"

def test_trainWoolf_DefaultkNN():
	classifierType = 'kNN'
	scalerString = 'MinMaxScaler'
	cvFolds = 5
	scoringM = 'MCC'
	nNhrs = [20]#range(1,20)
	nTrs = range(1,15,2)
	minL = range(10,30,3)
	inputCSV = 'data/classBD_binaryTable.csv'
	
	model = woolfClassifier.buildWoolf(classifierType, scalerString, cvFolds, scoringM, nNhrs, nTrs, minL)
	woolfClassifier.trainModel(model, inputCSV)
	print(model.best_score_)
	assert str(type(model)) == "<class 'sklearn.model_selection._search.GridSearchCV'>"

test_trainWoolf_DefaultkNN()



