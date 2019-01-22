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


nTrees = 5
minLeafSize = 10


def main():
	aGenesfile = "SampleData/classA.fasta"
	bGenesfile = "SampleData/classB.fasta"

	aFeatures = featureTablefromFASTA(aGenesfile)
	bFeatures = featureTablefromFASTA(bGenesfile)

	allFeatures = aFeatures.append(bFeatures)

	#create array of responses
	categories = ([1]*len(aFeatures)) + ([0]*len(bFeatures))

	clf = RandomForestClassifier(n_estimators=nTrees, min_samples_leaf=minLeafSize,random_state=1)
	clf.fit(allFeatures, categories)

	#Feature Importance
	print("\nFeature Importance:")
	print(clf.feature_importances_)

	#Testing
	testfile = "SampleData/testing.fasta"
	testSeq = featureTablefromFASTA(testfile)

	testData = []
	for row in testSeq.iterrows():
		index, data = row
		testData.append(data)
	
	print("\nTesting Random Forest classifier:\n")
	print("\tResult should be: [1 1 1 1 0 0 0 0]")
	print("\tResult: " + str(clf.predict(testData)) + '\n')

main()