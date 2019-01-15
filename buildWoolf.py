# ############################### #
# buildWoolf.py
# 
# Outline of script to build a woolf model.
# 
# Anna Farrell-Sherman 11/5/18
# ############################### #

### readdata - loads gene sequence data from input file
# returns: array of sequences
# WILL BE MODIFIED ONCE SEQUENCES ARE OBTAINED
def readdata(filename):
    data = [];
    for line in open(file,'r'):
        data.append(line)
    return data

def buildModel(aGenes, bGenes):
	#code here will build machine learning model basde on input sequences

def saveModel(model, modelOutFile):
	with open(modelOutFile, 'w'):
		#code here will save model to specified file


def main():
	aGenesFile = sys.argv[1]
    bGenesFile = sys.argv[2]
    modelOutFile = sys.argv[2]

    aGenes = readdata(aGenesFile)
    bGenes = readdata(bGenesFile)

    model = buildModel(aGenes, bGenes)

    saveModel(model, modelOutFile)

main()