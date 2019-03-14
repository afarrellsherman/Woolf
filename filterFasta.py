# ############################### #
# filterFasta.py
# 
# Takes a gene set and filters for particular gene names.
# 
# Anna Farrell-Sherman 1/14/19
# ############################### #

#import packages
from Bio import SeqIO
import random
#used to create command line inputs
import argparse

def readFastaFiltered(filename, searchTerm):
    data = []
    for record in SeqIO.parse(filename, "fasta"):
    	if searchTerm in record.description:
    		data.append(record)
    return data


def saveFilteredFasta(filename, searchTerm, outfilename):
	filteredData = [] # Setup an empty list
	for record in SeqIO.parse(filename, "fasta"):
		if searchTerm in record.description:
			filteredData.append(record)

	print(("Found %i sequences labeled \"" + searchTerm + "\"") % len(filteredData))

	out = outfilename + "-" + str(len(filteredData)) + ".fasta"

	SeqIO.write(filteredData, out, "fasta")

def multipleTrials(file1, file2, compName, fName, numTrials):
	while int(numTrials) > 0:
		trialName = compName + "_trial" + str(numTrials) + "_"
		createTrainTestFasta(file1, file2, trialName, fName)
		numTrials -= 1

def createTrainTestFasta(file1, file2, compName, fName):
	#arrays for results
	trainData1 = []
	trainData2 = []
	testData = []

	#counters to record number of sequences in each file
	count1 = count2 = test1 = test2 = 0
	# count2 = 0
	# test1 = 0
	# test1 = 0

	#for the first file
	for record in SeqIO.parse(file1, "fasta"):
		if random.randint(1,101) <= 25:
			testData.append(record)
			test1 += 1
		else:
			trainData1.append(record)
			count1 += 1

	#for the second file
	for record in SeqIO.parse(file2, "fasta"):
		if random.randint(1,101) <= 25:
			testData.append(record)
			test2 += 1
		else:
			trainData2.append(record)
			count2 += 1

	train1fileName = fName + "train1_" + compName + str(count1) + ".fasta"
	train2fileName = fName + "train2_" + compName + str(count2) + ".fasta"
	testOutFileName =  fName + "test_" + compName + str(test1)+"-"+str(test2) + ".fasta"

	SeqIO.write(testData, testOutFileName, "fasta")
	SeqIO.write(trainData1, train1fileName, "fasta")
	SeqIO.write(trainData2, train2fileName, "fasta")



#saveFilteredFasta(longFile, "class A", "SampleData/classA-full")

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Filter two fasta files to create two train files and one est file")

	#input fasta files
	parser.add_argument("aGenesFile", help="path to fasta file containing the first gene set")
	parser.add_argument("bGenesFile", help="path to fasta file containing the second gene set")

	#option to do multiple splits
	parser.add_argument("-s", "--splits", help="number of trial splits to create files for")

	#Output file info (user specified output)
	parser.add_argument("comparisonName", help="an identifying tag for all output files")
	parser.add_argument("-f", "--folder", help="A folder to contain the output files")

	args = parser.parse_args()

	folderName = ""
	if args.folder:
		folderName = args.folder + "/"

	if int(args.splits) > 1:
		multipleTrials(args.aGenesFile, args.bGenesFile, args.comparisonName, folderName, int(args.splits))
	else:
		createTrainTestFasta(args.aGenesFile, args.bGenesFile, args.comparisonName, folderName)


