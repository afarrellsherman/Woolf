# ############################### #
# HMM.py
# 
# Creates an HMM based classifier based on two gene sets
#
# ONGOING EDITS
# - 
#
# Helpful : https://github.com/hmmlearn/hmmlearn/issues/70
#
# 
# Anna Farrell-Sherman 1/14/19
# ############################### #

from calculateFeatures import readfasta
from hmmlearn import hmm
import numpy as np


def main():
	#aGenesfile = "SampleData/classA.fasta"
	#bGenesfile = "SampleData/classB.fasta"

	#aSequences = readfasta(aGenesfile)
	#bSequences = readfasta(bGenesfile)


	#for now for testing
	np.random.seed(42)


	#States
	states = ["Background", "Functional"]
	nStates = len(states)

	#Features
	aa = ['A','R','N','D','C','E','Q','G','H','I','L','K','M','F','P','S','T','W','Y','V']
	nAA = len(aa)

	#Model Variables
	startProbs = np.array([0.95, 0.05])
	transMat = np.array([[0.5, 0.5],
						 [0.5, 0.5]])
	emmissionProbs = np.array([[0.07, 0.04, 0.06, 0.06, 0.01, 0.08, 0.03, 0.07, 0.03, 0.01, 0.1, 0.07, 0.01, 0.05, 0.05, 0.08, 0.06, 0.01, 0.03, 0.07],
							 [0.02, 0.09, 0.05, 0.07, 0.03, 0.06, 0.01, 0.09, 0.03, 0.04, 0.07, 0.07, 0.08, 0.01, 0.02, 0.08, 0.06, 0.01, 0.03, 0.07]])


	#Build the model
	model = hmm.MultinomialHMM(n_components=2, init_params="ste")
	
	model.startprob_ = startProbs
	model.transmat_ = transMat
	model.emissionprob_ = emmissionProbs

	#testSequence = np.array([['A','A','R','C','Q','G','H','I','V','D','D','V','P','S','M','W','V','V']]).T
	testSequence = np.array([[1, 14, 14, 1, 2, 3, 14, 19, 2, 15, 16, 7, 8, 3, 5, 4, 4, 5, 5, 16, 17, 15]]).T
	#model = model.fit(testSequence)

	logprob, functionPattern = model.decode(testSequence, algorithm="viterbi")

	print("\nTesting HMM classifier:\n")
	print("\tTest Sequence: " + str(testSequence) + '\n')
	print("\tResult: " + str(functionPattern) + '\n')



main()