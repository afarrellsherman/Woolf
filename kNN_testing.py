# ############################### #
# kNN.py
# 
# Creates a k-nearest neighbor classifier based on two gene sets
#
# ONGOING EDITS
# - needs to be made modular
#
# 
# Anna Farrell-Sherman 1/14/19
# ############################### #

from calculateFeatures import featureTablefromFASTA
from sklearn import neighbors
#used to create command line inputs
import argparse

#to write data into csv file
import csv
import os



n_neighbors = 25

def getTestDataNumbers(testDataFileName):
	counts = ((testDataFileName.split("_"))[-1]).split("-")
	return [int(''.join(i for i in num if i.isdigit())) for num in counts]


def buildModel(aFile, bFile, kNeighbors):
	aFeatures = featureTablefromFASTA(aFile)
	bFeatures = featureTablefromFASTA(bFile)
	#create array of responses
	categories = ([1]*len(aFeatures)) + ([0]*len(bFeatures))

	allFeatures = aFeatures.append(bFeatures)

	clf = neighbors.KNeighborsClassifier(kNeighbors, weights='uniform')
	clf.fit(allFeatures, categories)

	return clf

def testModel(classifier, testdatafile):
	testSeq = featureTablefromFASTA(testdatafile)

	testData = []
	for row in testSeq.iterrows():
		index, data = row
		testData.append(data)

	result = classifier.predict(testData)

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

	return (percentAcorrect, percentBcorrect, accuracy)




if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Perform kNN on two training data files and one test file")

	#input fasta files
	parser.add_argument("atrainFile", help="Train file 1")
	parser.add_argument("btrainFile", help="Train file 2")
	parser.add_argument("testFile", help="Testing data file")

	args = parser.parse_args()

	kVals = [1, 2, 3, 4, 5, 7, 10, 15, 20, 25, 30, 35]
	outfileName = 'kNN_testingAccuracy.csv'

	if (not os.path.isfile(outfileName)):
		with open(outfileName, 'w') as accFile:
			writer = csv.writer(accFile)
			writer.writerow(['Comparison', 'Gene Type'] + kVals)
		accFile.close()

	#Store accuracies of models
	accuracyDataA = [args.testFile, args.atrainFile]
	accuracyDataB = [args.testFile, args.btrainFile]
	accuracyTotal = [args.testFile, "combined"]

	for kval in kVals:
		clf = buildModel(args.atrainFile, args.btrainFile, kval)
		aAcc, bAcc, allAcc = testModel(clf, args.testFile)
		accuracyDataA.append(aAcc)
		accuracyDataB.append(bAcc)
		accuracyTotal.append(allAcc)

	with open(outfileName, 'a') as accFile:
		writer = csv.writer(accFile)
		writer.writerow(accuracyDataA)
		writer.writerow(accuracyDataB)
		writer.writerow(accuracyTotal)

		accFile.close()

	
