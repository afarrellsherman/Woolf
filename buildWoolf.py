# ############################### #
# buildWoolf.py
# 
# Outline of script to build a woolf model.
# 
# Anna Farrell-Sherman 11/5/18
# ############################### #


#Things to think about adding:
## a way to choose features

#used to create command line inputs
import argparse
#import functions from other WoolfModel files
from calculateFeatures import featureTablefromFASTA
#import needed machine learning packages
from sklearn import neighbors
from sklearn.ensemble import RandomForestClassifier

#ADD AS ARGUMENT
n_neighbors = 3

# ------------------------------------------------------------------------------------------------
# FUNCTIONS

# ### readdata - loads gene sequence data from input file
# # returns: array of sequences
# def readdata(filename):
#     data = [];
#     for line in open(file,'r'):
#         data.append(line)
#     return data

# returns feature table and array of binary coded category labels for the table
def buildFeatureTable(aGenes, bGenes):
    aFeatures = featureTablefromFASTA(aGenes)
    bFeatures = featureTablefromFASTA(bGenes)

    allFeatures = aFeatures.append(bFeatures)

    #create array of responses
    categories = ([1]*len(aFeatures)) + ([0]*len(bFeatures))

    return allFeatures, categories

def buildModel(aGenes, bGenes):
	#code here will build machine learning model basde on input sequences
    return NONE

def saveModel(model, modelOutFile):
	#with open(modelOutFile, 'w'):
		#code here will save model to specified file
    return NONE

# ------------------------------------------------------------------------------------------------
# MAIN

def main():

    parser = argparse.ArgumentParser(description="Create a Woolf Model based on two gene files")
    parser.add_argument("aGenesFile", help="first of two amino acid fasta files")
    parser.add_argument("bGenesFile", help="second of two amino acid fasta files")

    #choose machine learning algorithm
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-k", "--kNN", action="store_true")
    group.add_argument("-f", "--randomForest", action="store_true")

    #kNN arguments
    parser.add_argument("-n", "--nNeighbors", type=int, default=3, help="number of neighboors for kNN classifier")

    #random Forest arguments
    parser.add_argument("-t", "--nTrees", type=int, default=5, help="number of trees for random forest classifier")
    parser.add_argument("-l", "--minLeafSize", type=int, default=10, help="minimum size of leaves in each tree of the random forest classifier")

    #add argument here to save model

    #add argument here to run model on given test

    #add verbose argument
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()

    featureTable, categories = buildFeatureTable(args.aGenesFile, args.bGenesFile)

    if args.kNN:
        clf = neighbors.KNeighborsClassifier(args.nNeighbors, weights='uniform')
    elif args.randomForest:
        clf = RandomForestClassifier(n_estimators=args.nTrees, min_samples_leaf=args.minLeafSize,random_state=1)

    #fit the model!
    clf.fit(featureTable, categories)

    #Testing
    testfile = "SampleData/testing.fasta"
    testSeq = featureTablefromFASTA(testfile)

    testData = []
    for row in testSeq.iterrows():
        index, data = row
        testData.append(data)

    results = clf.predict(testData)

    if args.verbose:
        if args.randomForest:
            #Feature Importance
            print("\nFeature Importance:")
            print(clf.feature_importances_)
    
        print("\nTesting classifier:\n")
        print("Result should be: [1 1 1 1 0 0 0 0]")
        print("Result: \t  " + str(results) + '\n')
    else:
        print(results)

main()