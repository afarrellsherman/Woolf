# ############################### #
# randomForest.py
# 
# Creates a random forest classifier based on two gene sets
#
# ONGOING EDITS
# - needs to be made modular
#
# 
# Anna Farrell-Sherman 1/14/19
# ############################### #

from calculateFeatures import featureTablefromFASTA
from sklearn.ensemble import RandomForestClassifier
#used to create command line inputs
import argparse

#to write data into csv file
import csv
import os

def getTestDataNumbers(testDataFileName):
	counts = testDataFileName.split("-")
	return [int(''.join(i for i in num if i.isdigit())) for num in counts]

def buildModel(aFile, bFile, nTrees, minLeafSize):
	aFeatures = featureTablefromFASTA(aFile)
	bFeatures = featureTablefromFASTA(bFile)
	#create array of responses
	categories = ([1]*len(aFeatures)) + ([0]*len(bFeatures))

	allFeatures = aFeatures.append(bFeatures)

	clf = RandomForestClassifier(n_estimators=nTrees, min_samples_leaf=minLeafSize,random_state=1)
	clf.fit(allFeatures, categories)

	return clf

def testModel(classifier, testdatafile):
	testSeq = featureTablefromFASTA(testdatafile)

	testData = []
	for row in testSeq.iterrows():
		index, data = row
		testData.append(data)

	#print("\nTesting Random Forest classifier:\n")

	result = classifier.predict(testData)

	#IMPORTANT I had this before and I think it worked:
	#result = classifier.predict(testData)
	#WHY?????


	# #Feature Importance
	# print("\nFeature Importance:")
	# print(clf.feature_importances_)

	numA, numB = getTestDataNumbers(testdatafile)

	nAcorrect = sum(result[0:numA])
	nBcorrect = (numB-sum(result[numA:numA+numB]))

	percentAcorrect = nAcorrect/numA
	percentBcorrect = nBcorrect/numB
	accuracy = (nAcorrect+nBcorrect)/(numA+numB)

	# print("\tResult: " + str(result) + '\n')
	# print("\tPercentage A Correct: " + str(percentAcorrect))
	# print("\tPercentage C Correct: " + str(percentBcorrect))
	# print("\t% Accuracy: " + str(accuracy))

	return accuracy


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Perform kNN on two training data files and one test file")

	#input fast files
	parser.add_argument("atrainFile", help="Train file 1")
	parser.add_argument("btrainFile", help="Train file 2")
	#user specified output string
	parser.add_argument("testFile", help="Testing data file")

	args = parser.parse_args()

	# aGenesfile = args.atrainFile
	# bGenesfile = args.btrainFile

	nTrees_toTest = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45]
	#minLeafSize = 6
	minLeafSize = 10
	max_minLeafSize = 30

	if (not os.path.isfile('testingAccuracy.csv')):
		with open('testingAccuracy.csv', 'w') as accFile:
			writer = csv.writer(accFile)
			writer.writerow(['Classes', 'minLeafSize'] + nTrees_toTest)
		accFile.close()

	while minLeafSize <= max_minLeafSize:
		accuracyData = [args.testFile, minLeafSize]
		for nTrees in nTrees_toTest:
			clf = buildModel(args.atrainFile, args.btrainFile, nTrees, minLeafSize)
			accuracyData.append(testModel(clf, args.testFile))

		with open('testingAccuracy.csv', 'a') as accFile:
			writer = csv.writer(accFile)
			writer.writerow(accuracyData)

		accFile.close()


		minLeafSize += 10


	# accuracyData = pandas.DataFrame(accuracyData)
	# accuracyData.to_csv('testingAccuracy.csv')



	#clf = buildModel(args.atrainFile, args.btrainFile, nTrees, minLeafSize)

	

	
	