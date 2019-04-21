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
import sys

### readfiles - opens files to read sequences
# filename: a file or path to a file containing sequence data in fasta format
# returns: an array of every sequence in the file
def readfasta(filename):
    seqs = list(SeqIO.parse(filename, "fasta"))
    return seqs
    

### binaryFeatureTable - 
def binaryFeatureTable(PosSeqFiles, NegSeqFiles):
	seqDicts = []

	#add sequences from each file in positive group
	sequenceClass = 1
	for file in PosSeqFiles:
		records = readfasta(file)
		for rec in records:
			#aSeq = ProteinAnalysis(str(rec.seq))
			seqDict = ProteinAnalysis(str(rec.seq)).get_amino_acids_percent()
			seqDict['Class'] = sequenceClass
			seqDict['Length'] = len(rec.seq)
			seqDict['ID'] = rec.id
			seqDicts.append(seqDict)
	
	#add sequences from each file in negative group
	sequenceClass = 0
	for file in NegSeqFiles:
		records = readfasta(file)
		for rec in records:
			#aSeq = ProteinAnalysis(str(rec.seq))
			seqDict = ProteinAnalysis(str(rec.seq)).get_amino_acids_percent()
			seqDict['Class'] = sequenceClass
			seqDict['Length'] = len(rec.seq)
			seqDict['ID'] = rec.id
			seqDicts.append(seqDict)

	return pd.DataFrame(seqDicts)

### predictDataFeatureTable - 
def predictDataFeatureTable(sequenceFiles):
	seqDicts = []

	#add each file with NO class identifier
	for file in sequenceFiles:
		records = readfasta(file)
		for rec in records:
			seqDict = ProteinAnalysis(str(rec.seq)).get_amino_acids_percent()
			seqDict['Length'] = len(rec.seq)
			seqDict['ID'] = rec.id
			seqDicts.append(seqDict)

	return pd.DataFrame(seqDicts)

### saveCSV - saves a datatable in a file with a given name
def saveCSV(dataTable, filename):
	return dataTable.to_csv(filename,index=None, header=True)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Build a CVS feature table from amino acid FASTA files")

	#Output file info (user specified output)
	parser.add_argument("-c", "--comparisonName", default="featureTable", help="an identifying tag for all output files")
	parser.add_argument("-f", "--folder", help="A folder to contain the output files")

	#choose machine learning algorithm
	group = parser.add_mutually_exclusive_group()
	group.add_argument("-b", "--binary", action="store_true")
	group.add_argument("-p", "--predict", action="store_true")
	
	#parser.add_argument('binaryFeatureTable', help='Create a binary class feature table with one class for the first group of fasta files and another class for the second group')
	parser.add_argument("-pf", "--posFasta", nargs='+', help="a single fasta file for a Binary Feature Table, or a set of one or more fasta files for a multiClass Feature Table")
	parser.add_argument("-nf", "--negFasta", nargs='+', help="one or more fasta files containing the negative class sequences for a multiClass Feature Table")


	args = parser.parse_args()

	if len(sys.argv)==1:
		parser.print_help(sys.stderr)
		sys.exit(1)

	folderName = ""
	if args.folder:
		folderName = args.folder + "/"

	fileName = folderName+args.comparisonName+".csv"

	if args.binary:
		if args.posFasta and args.negFasta:
			seqFeatureTable = binaryFeatureTable(args.posFasta, args.negFasta)
			saveCSV(seqFeatureTable, fileName)
			print('Binary Table')
			print('Saved csv file to: ' + fileName)
		else:
			print("For a binary feature table please provide both positive and negative class fasta files with [-pf] and [-nf]")
	elif args.predict:
		if args.posFasta:
			print(args.posFasta)
			seqFeatureTable = predictDataFeatureTable(args.posFasta)
			saveCSV(seqFeatureTable, fileName)
			print('Prediction Table')
			print('Saved csv file to: ' + fileName)
		else:
			print("For a prediction feature table please provide a fasta file with [-pf]")
	else:
		parser.print_help(sys.stderr)

	





