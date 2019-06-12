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


def test_feadfasta_classA():
	infile = 'data/test_classA.fasta'
	seqs = featureTable.readfasta(infile)
	print(len(seqs))
	assert len(seqs) == 15
	assert len(seqs[1]) == 304

def test_binaryFeatureTable_AvB():
	infileA = ['data/test_classA.fasta']
	infileB = ['data/test_classB.fasta']
	
	bTable = featureTable.binaryFeatureTable(infileA, infileB)
	assert list(bTable.columns) == ['A', 'C', 'Class', 'D', 'E', 'F', 'G', 'H', 'I', 'ID', 'K', 'L', 'Length', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
	assert len(bTable.index) == 30

def test_binaryFeatureTable_AvNotA():
	infileA = ['data/test_classA.fasta']
	infileNotA = ['data/test_classB.fasta', 'data/test_classC.fasta', 'data/test_classD.fasta']
	
	bTable = featureTable.binaryFeatureTable(infileA, infileNotA)
	assert list(bTable.columns) == ['A', 'C', 'Class', 'D', 'E', 'F', 'G', 'H', 'I', 'ID', 'K', 'L', 'Length', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
	assert len(bTable.index) == 71

def test_predictFeatureTable_CD():
	infile = ['data/test_classD.fasta', 'data/test_classC.fasta']
	
	pTable = featureTable.predictFeatureTable(infile)
	assert list(pTable.columns) == ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'ID', 'K', 'L', 'Length', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
	assert len(pTable.index) == 41

def test_saveCSV_classC_predictTable():
	infile = ['data/test_classC.fasta']
	pTable = featureTable.predictFeatureTable(infile)
	outputfilename = "output/classC_predictTable"

	featureTable.saveCSV(pTable, outputfilename)
	assert os.path.isfile(outputfilename)

def test_saveCSV_classBD_binaryTable():
	infileB = ['data/test_classB.fasta']
	infileD = ['data/test_classD.fasta']
	bTable = featureTable.binaryFeatureTable(infileB, infileD)
	outputfilename = "output/classBD_binaryTable"

	featureTable.saveCSV(bTable, outputfilename)
	assert os.path.isfile(outputfilename)