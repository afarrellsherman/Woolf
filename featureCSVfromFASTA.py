# ############################### #
# featureCSVfromFASTA.py
# 
# Creates a feature table with class identificiations from multiple fasta files.
# 
# Anna Farrell-Sherman 3/31/19
# ############################### #

#import packages
from Bio import SeqIO #for fasta reading
from Bio.SeqUtils.ProtParam import ProteinAnalysis #for determining percentage composition
import pandas as pd #to create the CSV file
import argparse # to format command line arguments

#Globals
aa = ['A','R','N','D','C','E','Q','G','H','I','L','K','M','F','P','S','T','W','Y','V'] #Amino Acid Letters

### readfiles - opens files to read sequences
# filename: a file or path to a file containing sequence data in fasta format
# returns: an array of every sequence in the file
def readfasta(filename):
    seqs = list(SeqIO.parse(filename, "fasta"))
    return seqs
    

### featureTable - 
def featureTable(sequenceFiles):
	seqDicts = []

	#add each file with different class identifier
	sequenceClass = 0
	for file in sequenceFiles:
		records = readfasta(file)
		for rec in records:
			#aSeq = ProteinAnalysis(str(rec.seq))
			seqDict = ProteinAnalysis(str(rec.seq)).get_amino_acids_percent()
			seqDict['Class'] = sequenceClass
			seqDict['Length'] = len(rec.seq)
			seqDicts.append(seqDict)
		sequenceClass += 1

	return pd.DataFrame(seqDicts)

### saveCSV - saves a datatable in a file with a given name
def saveCSV(dataTable, filename):
	return dataTable.to_csv(filename,index=None, header=True)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Build a CVS feature table from amino acid FASTA files")

	#input fasta files
	parser.add_argument("fastaFiles", nargs='+', help="one or more fasta files")

	#Output file info (user specified output)
	parser.add_argument("-n", "--comparisonName", default="featureTable", help="an identifying tag for all output files")
	parser.add_argument("-f", "--folder", help="A folder to contain the output files")

	args = parser.parse_args()

	folderName = ""
	if args.folder:
		folderName = args.folder + "/"

	seqFeatureTable = featureTable(args.fastaFiles)
	saveCSV(seqFeatureTable, folderName+args.comparisonName+".csv")






