# ############################### #
# calculateFeatures.py
# 
# Takes a gene set and creates a table of features calculated for each gene.
# Used to calculate the features provided for feature based classification.
# 
# Anna Farrell-Sherman 1/14/19
# ############################### #

#import packages
from Bio import SeqIO
import pandas as pd


### readfiles - opens files to read sequences
# filename: a file or path to a file containing sequence data in fasta format
# returns: an array of every sequence in the file
def readfasta(filename):
    data = []
    for record in SeqIO.parse(filename, "fasta"):
        data.append(record.seq)
    return data

#Amino Acid Letters
aa = ['A','R','N','D','C','E','Q','G','H','I','L','K','M','F','P','S','T','W','Y','V']

### length
def seqLength(sequences):
	lengths = []
	for seq in sequences:
		lengths.append(len(seq))
	return lengths

def percentComposition(character, sequence):
	return sequence.count(character)/len(sequence)

def aaCompsitionTable(sequences):
	aaTable = []
	for seq in sequences:
		composition = []
		for a in aa:
			composition.append(percentComposition(a, seq))
		aaTable.append(composition)
	return aaTable


def featureTable(sequences):

	fTable = pd.DataFrame(aaCompsitionTable(sequences))
	fTable.columns = aa
	fTable['length'] = pd.Series(seqLength(sequences))

	return fTable

def featureTablefromFASTA(filename):
	myData = readfasta(filename)
	return featureTable(myData)



