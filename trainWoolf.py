# ############################### #
# trainWoolf.py
# 
# Script to build a woolf model.
# 
# Anna Farrell-Sherman 11/5/18
# ############################### #

#used to create command line inputs
from argparse import ArgumentParser, ArgumentTypeError

#import needed machine learning packages
from sklearn import neighbors #for the kNN
from sklearn.ensemble import RandomForestClassifier #for the randomforest
from sklearn.metrics import matthews_corrcoef, make_scorer

from sklearn.model_selection import GridSearchCV # for parameter estimation
from sklearn.pipeline import Pipeline #to allow for normalization in cross validation
from sklearn.preprocessing import MinMaxScaler, StandardScaler, MaxAbsScaler, RobustScaler #minMax normalization

#other functionality
import pandas as pd #to import the csv datafile
import numpy as np # to read in length as float64
from ast import literal_eval #to decode dictionaries entered for parameter grids
import sys # for error handeling


def buildWoolf(classifierType, pGrid, scalerString, cvFolds, scoringM, nNhrs, nTrs, minL):
	'''Creates the Woolf Model with all user given parameters '''

    #Classifiers and Param Grids
	if classifierType == 'kNN':
		clf = neighbors.KNeighborsClassifier(weights='uniform')
		param_grid = {'clf__n_neighbors': nNhrs} if pGrid == None else pGrid
	elif classifierType == 'fOREST':
		clf = RandomForestClassifier(random_state=42)
		param_grid = {'clf__n_estimators': nTrs, 'clf__min_samples_leaf': minL} if pGrid == None else pGrid
	else:
		raise NameError("Unrecognized classifier type: " + classifierType)

	scaler = scaler_selector(scalerString)
	accM = accM_selector(scoringM)

    #create pipe to allow for scaling in cross-validation
	pipe = Pipeline([('scaler', scaler), ('clf', clf)])

    #create grid for hyperparameter searching
	gridModel = GridSearchCV(pipe, param_grid, cv=cvFolds, scoring=accM, return_train_score=True, iid=False)

	return gridModel
        


def trainModel(woolfModel, inputCSV):
	'''Train a woolf model with a binary class feature table'''

    #Set Up data
	sequenceFeatureTable = pd.read_csv(inputCSV, header = 0, dtype={'Length':  np.float64})
	seqTarget = sequenceFeatureTable['Class']
	seqIDs = sequenceFeatureTable['ID']
	seqData = sequenceFeatureTable.drop(columns=['Class', 'ID'])

    #fit model to data on provided parameter grid
	woolfModel.fit(seqData, seqTarget)

	return woolfModel

def findMisclassified(woolfModel, inputCSV):
	'''Find all the missclassified items in a binary class feature table'''

    #Set Up data
	sequenceFeatureTable = pd.read_csv(inputCSV, header = 0, dtype={'Length':  np.float64})
	seqTarget = sequenceFeatureTable['Class']
	seqIDs = sequenceFeatureTable['ID']
	seqData = sequenceFeatureTable.drop(columns=['Class', 'ID'])

    #Grid model to data
	predictions = woolfModel.predict(seqData)

	misAsPos = []
	misAsNeg = []
	for i in range(len(seqIDs)):
		if seqTarget[i] == 0 and predictions[i] == 1:
			misAsPos.append(seqIDs[i])
		elif seqTarget[i] == 1 and predictions[i] == 0:
			misAsNeg.append(seqIDs[i]) 

	return misAsPos, misAsNeg


def predictWoolf(woolfModel, predictCSV):
	'''Predict the class of new feature sets with a created woolf model'''

	#Set Up data
	sequenceFeatureTable = pd.read_csv(predictCSV, header = 0, dtype={'Length':  np.float64})
	seqIDs = sequenceFeatureTable['ID']
	seqData = sequenceFeatureTable.drop(columns=['ID'])

	#determine if class labels are in dataframe
	classLabled = True if 'Class' in list(sequenceFeatureTable) else False
	score = None

	#if there are class labels in dataframe
	if classLabled:
		correctClass = sequenceFeatureTable['Class']
		seqData = seqData.drop(columns=['Class'])
		score = woolfModel.score(seqData, correctClass)

	#print(list(sequenceFeatureTable))

    #predict classes
	predictions = woolfModel.predict(seqData)

	#Attach IDs to predictions
	resultsDict = dict(zip(seqIDs, predictions))

	return resultsDict, score


def parseRange(rangeString):
	'''Looks at inputed range from command line and parses it into a python object'''
	try:
		if ',' in rangeString:
			lo, hi = rangeString.split('-')
			hi, jump = hi.split(',')
			res = list(range(int(lo), int(hi)+1, int(jump)))
		elif '-' in rangeString:
			lo, hi = rangeString.split('-')
			res = list(range(int(lo), int(hi)+1))
		elif rangeString.isdigit():
			res = [int(rangeString)]
	except:
		raise ArgumentTypeError("'" + rangeString + "' is not a valid range of numbers. Expected formats: '1' '1-10' or '1-10,2'.")
	return res

def scaler_selector(inputString):
	'''determine which scaling type was selected'''
	scalers = {'MinMaxScaler': MinMaxScaler(), 'StandardScaler': StandardScaler(), 
		'MaxAbsScaler': MaxAbsScaler(), 'RobustScaler': RobustScaler(), 'None': None}
	scaler = scalers.get(inputString , '')
	if scaler == '': #raise error if not found
		raise TypeError(inputString)
	return scaler

def accM_selector(inputString):
	'''#determine which accuracy metric type was selected'''
	accMs = {'MCC': make_scorer(matthews_corrcoef), 'f1': 'f1', 
		'accuracy': 'accuracy', 'precision': 'precision', 'recall': 'recall'}
	accM = accMs.get(inputString , '')
	if accM == '': #raise error if not found
		raise TypeError(inputString)
	return accM

if __name__ == '__main__':

	#print(scaler_selector('MinMaxScaler'))

	##################################################################################
	#Default Values
	# If you know enough python to alter the script, you can change the default values
	# here instead of on the command line.  
	##################################################################################
	scalingType = 'MinMaxScaler' # EX: 'StandardScaler'
	scoringMetric = 'MCC' #EX: ‘f1’
	crossFolds = 5 #EX: 10
	nNeighbors = range(1,20)
	nTrees = range(1,15,2)
	minLeafSize = range(10,30,3)

	#The parameter grid can take the place of the algorithm inputs above, and allows
	# adjustment of more parameters in the classifier algorithm
	pGrid = None
	#EX: {'clf__n_estimators': range(1,20), 'clf__min_samples_leaf': range(3,30,3)}
	##################################################################################
	##################################################################################

	parser = ArgumentParser(description="Create a Woolf Model based a feature table")
	parser.add_argument("featureTable", help="A CSV file containing feature data from a set of sequences")

	#choose machine learning algorithm
	group = parser.add_mutually_exclusive_group()
	group.add_argument("-k", "--kNN", action="store_true")
	group.add_argument("-f", "--randomForest", action="store_true")

	#kNN arguments
	parser.add_argument("-n", "--nNeighbors", type=parseRange, help="number of neighboors for kNN classifier.  Ranges are expresed as low-hi,jump (1-7,2 would test 1,3,5 and 7")

	#random Forest arguments
	parser.add_argument("-t", "--nTrees", type=parseRange, help="number of trees for random forest classifier.  Ranges are expresed as low-hi,jump (1-7,2 would test 1,3,5 and 7")
	parser.add_argument("-l", "--minLeafSize", type=parseRange, help="minimum size of leaves in each tree of the random forest classifier.  Ranges are expresed as low-hi,jump (1-7,2 would test 1,3,5 and 7")

	#set up learning parameters
	parser.add_argument("-s", "--featureScaler", help="A scikit learn scaler object to scale in the input features")
	parser.add_argument("-c", "--crossValidationFolds", help="The number of cross validation folds to execute")
	parser.add_argument("-a", "--accuracyMetric", help="A scikit learn accuracy metric for training")

	#add functionality
	parser.add_argument("-p", "--predictFeatureTable", help="A unclassified feature table to be predicted by the model")
	parser.add_argument("-e", "--listErrors", action="store_true", help="Include to see a list of which sequences in the training dataset were missclassified")


	#add verbose argument
	parser.add_argument("-v", "--verbose", action="store_true", help="Inlcude to get more detailed output")

	args = parser.parse_args()

	##################################################################################

	#Check that arugments were provided
	if len(sys.argv)==1:
		parser.print_help(sys.stderr)
		sys.exit(1)

	#update learning parameters if needed
	scalingType = args.featureScaler if args.featureScaler else scalingType
	scoringMetric = args.accuracyMetric if args.accuracyMetric else scoringMetric
	crossFolds = args.crossValidationFolds if args.crossValidationFolds else crossFolds
	nNeighbors = args.nNeighbors if args.nNeighbors else nNeighbors
	nTrees = args.nTrees if args.nTrees else nTrees
	minLeafSize = args.minLeafSize if args.minLeafSize else minLeafSize

	#Determine which classifier type was selected
	if args.kNN:
		classifierType = 'kNN'
		print('Building kNN Woolf Model...')
	elif args.randomForest:
		classifierType = 'fOREST'
		print('Building Random Forest Woolf Model...')
	else:
		print('ERROR: Please choose either kNN (-k) or Random Forest (-f)')
		exit()

	if args.verbose:
		print("Cross-validation Folds: " + str(crossFolds))
		print("Scoring Metric: " + str(scoringMetric))
		print("Scaler type: " + str(scalingType))

	try:
		#Build the model
		woolf = buildWoolf(classifierType, pGrid, scalingType, int(crossFolds), scoringMetric, nNeighbors, nTrees, minLeafSize)

		#Train the model
		print("Training Model...")
		results = trainModel(woolf, args.featureTable)
	except (ValueError, TypeError) as e:
		print("Invalid Input: " + str(e))
		exit()


	#OUTPUT
	print("~~~~~~    RESULTS    ~~~~~~")
	print("Score of best classifier: " + str(results.best_score_))
	#print("Standard deviation of best score: " + str(results.cv_results_['std_test_score'][results.best_index_]))
	print("Best Params:" + str(results.best_params_))
	if args.verbose:
		print("Range of classifier scores across hyperparameters:")
		print("\tMax: " + str(results.best_score_))
		print("\tMin: " + str(min(results.cv_results_['mean_test_score'])))
		#print("\tParams: " + str(results.cv_results_['params']))
		#print("\tValues: " + str(results.cv_results_['mean_test_score']))
		#print("\tSD: " + str(results.cv_results_['std_test_score']))
		print("Range of training scores across hyperparameters:")
		print("\tMax: " + str(max(results.cv_results_['mean_train_score'])))
		print("\tMin: " + str(min(results.cv_results_['mean_train_score'])))
	print("~~~~~~               ~~~~~~")

	#Print misclassified sequences
	if args.listErrors:
		print("Listing misclassified instances")
		posErrors, negErrors = findMisclassified(woolf, args.featureTable)
		print("misclassified as positive class:\n " + str(posErrors))
		print("misclassified as negative class:\n " + str(negErrors))

	#Predict new instances
	if args.predictFeatureTable:
		print("Predicting novel instances")
		try:
			prediction, score = predictWoolf(woolf, args.predictFeatureTable)
			print(prediction)
			if score:
				print("Score on test data: " + str(score))
		except FileNotFoundError:
			print("ERROR: Feature Table not found: " + args.predictFeatureTable)
        



        
