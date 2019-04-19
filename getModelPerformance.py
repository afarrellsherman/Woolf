#getResults.py


import trainWoolf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler, MaxAbsScaler, RobustScaler #minMax normalization

#files to save to
accuracyFile = 'fOREST_Acc.csv'
sdFile = 'kOREST_SD.csv'

comparisons = ['CSVs/AvB.csv','CSVs/AvNotA.csv','CSVs/AvC.csv','CSVs/AvB.csv'] #paths to files
classifierType = 'fOREST' #'kNN' or 'fOREST'
#pGrid = {'clf__n_neighbors': range(1,31,5)}
pGrid = {'clf__n_estimators': range(1,20,3), 'clf__min_samples_leaf': range(1,20,3)}
scaler = MinMaxScaler()#, StandardScaler(), MaxAbsScaler(), RobustScaler(), None]
cvFolds = 5
scoringMs = ['f1','accuracy','average_precision','precision','recall','roc_auc']
nNhrs = nTrs = minL = 0 #not used because pGrid is used

resultsDictList = []
SDDictList = []

for comp in comparisons:
	for scoringM in scoringMs:
		infoDict = {'Comparison': comp, 'Scaler': scaler, 'CV Folds': cvFolds, 'Scoring Metric': scoringM}

		woolf = trainWoolf.buildWoolf(classifierType, pGrid, scaler, cvFolds, scoringM, nNhrs, nTrs, minL)
		trainedWoolf = trainWoolf.trainModel(woolf, comp)

		kValues = ['Trees:'+str(d['clf__n_estimators'])+'leaf'+str(d['clf__min_samples_leaf']) for d in trainedWoolf.cv_results_['params']]
		accuracies = list(trainedWoolf.cv_results_['mean_test_score'])
		sds = list(trainedWoolf.cv_results_['std_test_score'])

		resultsDict = dict(zip(kValues, accuracies))
		sdDict = dict(zip(kValues, sds))

		resultsDict.update(infoDict)
		sdDict.update(infoDict)

		resultsDictList.append(resultsDict)
		SDDictList.append(sdDict)

Accuracies = pd.DataFrame(resultsDictList)
SDs = pd.DataFrame(SDDictList)

def saveCSV(dataTable, filename):
	with open(filename, 'a') as f:
		dataTable.to_csv(f, header=False)

saveCSV(Accuracies, accuracyFile)
saveCSV(SDs, sdFile)



