#!/usr/bin/env python3

####################################
#
# unitTests.py
# Testing code for the Woolf Pipeline
#
####################################

import pytest
from woolf import featureTable
#from woolf import woolfClassifier
import os.path

###############################################################################################
# Testing 

def test_feadfasta_classA():
	infile = 'fastas/test_classA.fasta'
	seqs = featureTable.readfasta(infile)
	print(len(seqs))
	assert len(seqs) == 15
	assert len(seqs[1]) == 304

def test_binaryFeatureTable_AvB():
	infileA = ['fastas/test_classA.fasta']
	infileB = ['fastas/test_classB.fasta']
	
	bTable = featureTable.binaryFeatureTable(infileA, infileB)
	assert list(bTable.columns) == ['A', 'C', 'Class', 'D', 'E', 'F', 'G', 'H', 'I', 'ID', 'K', 'L', 'Length', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
	assert len(bTable.index) == 30

def test_binaryFeatureTable_AvNotA():
	infileA = ['fastas/test_classA.fasta']
	infileNotA = ['fastas/test_classB.fasta', 'fastas/test_classC.fasta', 'fastas/test_classD.fasta']
	
	bTable = featureTable.binaryFeatureTable(infileA, infileNotA)
	assert list(bTable.columns) == ['A', 'C', 'Class', 'D', 'E', 'F', 'G', 'H', 'I', 'ID', 'K', 'L', 'Length', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
	assert len(bTable.index) == 71

def test_predictFeatureTable_CD():
	infile = ['fastas/test_classD.fasta', 'fastas/test_classC.fasta']
	
	pTable = featureTable.predictFeatureTable(infile)
	assert list(pTable.columns) == ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'ID', 'K', 'L', 'Length', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
	assert len(pTable.index) == 41

def test_saveCSV_classC_predictTable():
	infile = ['fastas/test_classC.fasta']
	pTable = featureTable.predictFeatureTable(infile)
	outputfilename = "output/classC_predictTable"

	featureTable.saveCSV(pTable, outputfilename)
	assert os.path.isfile(outputfilename)

def test_saveCSV_classBD_binaryTable():
	infileB = ['fastas/test_classB.fasta']
	infileD = ['fastas/test_classD.fasta']
	bTable = featureTable.binaryFeatureTable(infileB, infileD)
	outputfilename = "output/classBD_binaryTable"

	featureTable.saveCSV(bTable, outputfilename)
	assert os.path.isfile(outputfilename)


#for use when writing testing cases
if __name__ == "__main__":

	#test_feadfasta_classA()
	test_binaryFeatureTable_AvB()