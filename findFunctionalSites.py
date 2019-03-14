# ############################### #
# findFunctionalSites.py
# 
# Uses Clustal Omega sequence alighments to find the functional areas to be used as states in the HMM
#
# ONGOING EDITS
# - 
#
#
# 
# Anna Farrell-Sherman 2/8/19
# ############################### #


from calculateFeatures import readfasta #probably just for testing
import subprocess
from Bio import AlignIO #used to read clustal omega files

#for testing
aGenesfile = "SampleData/classA.fasta"
bGenesfile = "SampleData/classB.fasta"

#things to set
culstalOutName = "test3"

aSequences = readfasta(aGenesfile)
bSequences = readfasta(bGenesfile)


def readClustalAlignment(filename):
	seqs = []
	with open(filename, "rU") as handle:
		align = AlignIO.read(handle, "clustal")
		print(dir(align.column_annotations))
		print("-----------------------------------------------")
		print(align.column_annotations.items)
		print("-----------------------------------------------")
		# for record in AlignIO.read(handle, "clustal"):
		# 	print(record)
	return align


	    # with open(fileName, 'r') as clustal:
	# 	data = clustal.readlines()
	# 	for line in data:
	# 		#words = line.split()
	# 		print(line)




def main():

	#add feature to tell what input file is
	#if input == fasta:
		#create clustal with subprocess call
		#subprocess.call(["python", "clustalo.py", "--email",
		#				 "afarrel4@wellesley.edu", aGenesfile, "--stype",
		#				 "protein", "--quiet", "--outfile", culstalOutName])
	#else: 
		#use clustal file

	#Open clustal alighment file and 
	readClustalAlignment("test3.aln-clustal_num.clustal_num")






main()