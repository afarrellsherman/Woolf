#!/usr/bin/env python3

#getResults.py


import trainWoolf
import pandas as pd
#from sklearn.preprocessing import MinMaxScaler, StandardScaler, MaxAbsScaler, RobustScaler #minMax normalization

#files to save to
accuracyFile = 'performance_fOREST.csv'

comparisons = ['CSVs/AvNotA.csv','CSVs/AvB.csv','CSVs/AvC.csv','CSVs/AvD.csv'] #paths to files
classifierType = 'fOREST' #'kNN' or 'fOREST'
#pGrid = {'clf__n_neighbors': range(1,20)}
pGrid = {'clf__n_estimators': range(1,15,2), 'clf__min_samples_leaf': range(10,30,3)}
scalers = ['MinMaxScaler', 'StandardScaler', 'MaxAbsScaler', 'RobustScaler', 'None']
cvFolds = 5
scoringMs = ['f1','accuracy','MCC']
nNhrs = nTrs = minL = 0 #not used because pGrid is used

resultsDictList = []

for comp in comparisons:
	print("Now running: " + comp)
	for scoringM in scoringMs:
		print("\tMetric: " + scoringM)
		for scaler in scalers:
			print("\t\tScaler: " + scaler)
			infoDict = {'Comparison': comp, 'Scaler': scaler, 'CV Folds': cvFolds, 'Scoring Metric': scoringM}

			woolf = trainWoolf.buildWoolf(classifierType, pGrid, scaler, cvFolds, scoringM, nNhrs, nTrs, minL)
			trainedWoolf = trainWoolf.trainModel(woolf, comp)

			if classifierType == 'fOREST':
				kValues = ['Trees:'+str(d['clf__n_estimators'])+'leaf'+str(d['clf__min_samples_leaf']) for d in trainedWoolf.cv_results_['params']]
			elif classifierType == 'kNN':
				kValues = ['k:'+str(d['clf__n_neighbors']) for d in trainedWoolf.cv_results_['params']]

			accuracies = list(trainedWoolf.cv_results_['mean_test_score'])

			resultsDict = dict(zip(kValues, accuracies))

			resultsDict.update(infoDict)

			resultsDictList.append(resultsDict)

Accuracies = pd.DataFrame(resultsDictList)

def saveCSV(dataTable, filename):
	with open(filename, 'a') as f:
		dataTable.to_csv(f, header=True)

saveCSV(Accuracies, accuracyFile)
