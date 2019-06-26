#!/usr/bin/env python3

####################################
#
# test_featureTable.py
# Testing code for the Woolf Pipeline featureTable module
#
####################################

import pytest
from woolf import featureTable
import os.path

testdata = os.path.join(os.path.dirname(__file__), 'data')
outputdata = os.path.join(os.path.dirname(__file__), 'output')
testclasses = [os.path.join(testdata, f) for f in os.listdir(testdata)]
testclasses.sort()
classA, classB, classC, classD = testclasses[1:]

def test_file_order():
	assert classA.endswith("classA.fasta")
	assert classB.endswith("classB.fasta")
	assert classC.endswith("classC.fasta")
	assert classD.endswith("classD.fasta")

def test_feadfasta_classA():
	seqs = featureTable.readfasta(classA)

	assert len(seqs) == 15
	assert len(seqs[1]) == 304

def test_binaryFeatureTable_AvB():
	bTable = featureTable.binaryFeatureTable([classA], [classB])
	assert list(bTable.columns) == ['A', 'C', 'Class', 'D', 'E', 'F', 'G', 'H', 'I', 'ID', 'K', 'L', 'Length', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
	assert len(bTable.index) == 30

def test_binaryFeatureTable_AvNotA():
	bTable = featureTable.binaryFeatureTable([classA], [classB, classC, classD])
	assert list(bTable.columns) == ['A', 'C', 'Class', 'D', 'E', 'F', 'G', 'H', 'I', 'ID', 'K', 'L', 'Length', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
	assert len(bTable.index) == 71

def test_predictFeatureTable_CD():
	pTable = featureTable.predictFeatureTable([classD, classC])
	assert list(pTable.columns) == ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'ID', 'K', 'L', 'Length', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
	assert len(pTable.index) == 41

# def test_saveCSV_classC_predictTable():
# 	pTable = featureTable.predictFeatureTable([classC])
# 	outputfilename = os.path.join(outputdata, 'classC_predictTable')
#
# 	featureTable.saveCSV(pTable, outputfilename)
# 	assert os.path.isfile(outputfilename)
#
# def test_saveCSV_classBD_binaryTable():
# 	bTable = featureTable.binaryFeatureTable([classB], [classD])
# 	outputfilename = os.path.join(outputdata, 'classBD_binaryTable')
#
# 	featureTable.saveCSV(bTable, outputfilename)
# 	assert os.path.isfile(outputfilename)
