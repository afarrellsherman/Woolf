# ############################### #
# calculateFunctionSites.py
# 
# Calculates the functional areas to be used as states in the HMM
#
# ONGOING EDITS
# - 
#
#
# 
# Anna Farrell-Sherman 2/8/19
# ############################### #


import numpy as np
from calculateFeatures import readfasta

aas = ['A','R','N','D','C','E','Q','G','H','I','L','K','M','F','P','S','T','W','Y','V']


#STILL WORKING ON!!! NOT AT ALL DONE, just copied from another file
def createTable(sequences):
	aaTable = numpy.empty(shape)
	for seq in sequences:
		for aa in aas:
			composition = []
		for a in aa:
			composition.append(a)
		aaTable.append(composition)
	return aaTable


#For testing, will be updated
def main():
	aGenesfile = "SampleData/classA.fasta"
	bGenesfile = "SampleData/classB.fasta"

	aSequences = readfasta(aGenesfile)
	bSequences = readfasta(bGenesfile)

	print(createTable(aSequences))
	
	print(aSequences)


main()