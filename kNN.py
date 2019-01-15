# ############################### #
# kNN.py
# 
# Creates a k-nearest neighbor classifier based on two gene sets
# Used to calculate the features provided for feature based classification.
#
# ONGOING EDITS
# - needs to be made modular
#
# 
# Anna Farrell-Sherman 1/14/19
# ############################### #

from calculateFeatures import featureTablefromFASTA
from sklearn import neighbors


n_neighbors = 3


def main():
	aGenesfile = "SampleData/classA.fasta"
	bGenesfile = "SampleData/classB.fasta"

	aFeatures = featureTablefromFASTA(aGenesfile)
	bFeatures = featureTablefromFASTA(bGenesfile)

	allFeatures = aFeatures.append(bFeatures)

	#create array of responses
	categories = ([1]*len(aFeatures)) + ([0]*len(bFeatures))

	clf = neighbors.KNeighborsClassifier(n_neighbors, weights='uniform')
	clf.fit(allFeatures, categories)


	#Testing
	testfile = "SampleData/testing.fasta"
	testSeq = featureTablefromFASTA(testfile)

	testData = []
	for row in testSeq.iterrows():
		index, data = row
		testData.append(data)
	
	print("\nTesting kNN classifier:\n")
	print("\tResult should be: [1 1 1 1 0 0 0 0]")
	print("\tResult: " + str(clf.predict(testData)) + '\n')

main()