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

def test_scaler_selector_MaxAbs():
	testString = 'MaxAbsScaler'
	assert str(woolfClassifier.scaler_selector(testString)) == "MaxAbsScaler(copy=True)"

def test_scaler_selector_Error():
	testString = 'MaxAbs'
	with pytest.raises(TypeError):
		woolfClassifier.scaler_selector(testString)

def test_accM_selector_f1():
	testString = 'f1'
	assert str(woolfClassifier.accM_selector(testString)) == "f1"

def test_accM_selector_Error():
	testString = 'f'
	with pytest.raises(TypeError):
		woolfClassifier.accM_selector(testString)

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
	assert model.cv == 5
	assert not hasattr(model, 'best_estimator_ ')

def test_buildWoolf_cv3RandomForest():
	classifierType = 'fOREST'
	scalerString = 'MinMaxScaler'
	cvFolds = 3
	scoringM = 'MCC'
	nNhrs = range(1,20)
	nTrs = range(1,15,2)
	minL = range(10,30,3)

	model = woolfClassifier.buildWoolf(classifierType, scalerString, cvFolds, scoringM, nNhrs, nTrs, minL)
	assert str(type(model)) == "<class 'sklearn.model_selection._search.GridSearchCV'>"
	assert model.cv == 3
	assert not hasattr(model, 'best_estimator_ ')

def test_trainModel_k915kNN():
	classifierType = 'kNN'
	scalerString = 'MinMaxScaler'
	cvFolds = 5
	scoringM = 'MCC'
	nNhrs = [9,10,11,12,13,14,15]
	nTrs = range(1,15,2)
	minL = range(10,30,3)
	inputCSV = 'data/classBD_binaryTable.csv'
	
	model = woolfClassifier.buildWoolf(classifierType, scalerString, cvFolds, scoringM, nNhrs, nTrs, minL)
	woolfClassifier.trainModel(model, inputCSV)
	assert str(type(model)) == "<class 'sklearn.model_selection._search.GridSearchCV'>"
	assert model.cv == 5
	assert hasattr(model, 'best_estimator_')
	assert model.best_score_ == 0.9581138830084189

def test_findMisclassified_accuracykNN():
	classifierType = 'kNN'
	scalerString = 'None'
	cvFolds = 5
	scoringM = 'accuracy'
	nNhrs = range(15,20)
	nTrs = range(1,15,2)
	minL = range(10,30,3)
	inputCSV = 'data/classBD_binaryTable.csv'
	
	model = woolfClassifier.buildWoolf(classifierType, scalerString, cvFolds, scoringM, nNhrs, nTrs, minL)
	woolfClassifier.trainModel(model, inputCSV)
	misAsPos, misAsNeg = woolfClassifier.findMisclassified(model, inputCSV)
	assert model.best_score_ == 0.5972222222222221
	assert len(misAsPos) == 10
	assert misAsNeg == ['AJP08641.1', 'AKZ20823.1']

def test_predictWoolf_f1fOREST():
	classifierType = 'fOREST'
	scalerString = 'None'
	cvFolds = 5
	scoringM = 'accuracy'
	nNhrs = range(15,20)
	nTrs = range(1,15,2)
	minL = range(10,30,3)
	inputCSV = 'data/classBD_binaryTable.csv'
	
	model = woolfClassifier.buildWoolf(classifierType, scalerString, cvFolds, scoringM, nNhrs, nTrs, minL)
	woolfClassifier.trainModel(model, inputCSV)
	resultsDict, score = woolfClassifier.predictWoolf(model, inputCSV)
	assert model.best_score_ == 0.9777777777777779
	assert resultsDict['AAM63403.1'] == 1
	assert score == 1
