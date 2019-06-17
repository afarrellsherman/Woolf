#  The Woolf Classifier Building Pipeline: A Tool for Protein Differentiation through Machine Learning

This is a machine learning tool to classify the function of proteins from obscure datasets.

## Overview

The pipeline takes two lists of genes with some distinguishing characteristic, uses machine learning to categorize the difference between them, and then parses through a new unidentified gene set making predictions about which category genes belong to.   The tool can identify patterns in the data too complicated for humans to parse, and use them to identify potential functions in unidentified genes.

### Algorithms

The Woolf pipeline uses sci-kit learn to provide the following machine learning alrogithms:

* Random forest trees
* k nearest neighboor (kNN)

## Getting Started

For a complete tutorial please see the [User Guide](docs/usermanual.md).

### Dependancies

These dependancies should be installed automatically if they are not already present:
* pandas
* argparse
* biopython
* scikit-learn
* numpy

### Installation

```sh
$ pip install woolf
```

## Basic Usege

### Creating a Feature Table

Run the following on the comand line, with both FASTA files in the current working directory:

```
featureTable [-h] [-c COMPARISONFILENAME] [-f FOLDER]
                             [-b | -t] [-p POSFASTA [POSFASTA ...]]
                             [-n NEGFASTA [NEGFASTA ...]]
```

Options:

   **-h, --help** Show help message and exit.

   **-c, --comparisonFileName COMPARISONFILENAME** An identifying tag for all output files.

   **-f, --folder FOLDER** A folder to contain the output files.

   **-b, --binary** Creates a feature table with binary class markers.

   **-t, --predict** Creates a feature table with no class markers for use in prediction.

   **-p, --posFasta POSFASTA ...** One or more FASTA files containing amino acid sequences belonging to the positive class.

   **-n, --negFasta NEGFASTA...** One or more FASTA files containing amino acid sequences belonging to the negative class.

   **-u, --unknownFasta UNKNOWNFASTA...** One or more FASTA files containing amino acid sequences of unknown function.

Note that posFasta and negFasta should contain genes from a similar class with one distinct functional difference.

The output file outputFile will contain a feature table with percent composition amino acids and length as features.  Binary tables will also contain a binary class marker, predict tables will not.

### Training a Woolf Classifier:

Run the following on the comand line, with the feature table/tables in the current working directory:

```
trainWoolf [-h] [-k | -f] [-n NNEIGHBORS] [-t NTREES] [-l MINLEAFSIZE]
                  [-s FEATURESCALER] [-c CROSSVALIDATIONFOLDS]
                  [-a ACCURACYMETRIC] [-p PREDICTFEATURETABLE] [-e] [-v]
                  featureTable
```

Options:

  **-h, --help** Show help message and exit.

  **-k, --kNN** Select a kNN algorithm for training.

  **-f, --randomForest** Select a random forest algorithm for training.

  **-n, --nNeighbors NNEIGHBORS** Number of neighboors for kNN classifier. Ranges are expresed as `low-hi,jump` (`1-7,2` would test 1,3,5 and 7).

  **-t, --nTrees NTREES** Number of trees for random forest classifier. Ranges are expresed as `low-hi,jump` (`1-7,2` would test 1,3,5 and 7).

  **-l, --minLeafSize MINLEAFSIZE** Minimum size of leaves in each tree of the random forest classifier. Ranges are expresed as low-hi,jump (`1-7,2` would test 1,3,5 and 7).

  **-s, --featureScaler FEATURESCALER** A scikit learn scaler object to scale in the input features.

  **-c, --crossValidationFolds CROSSVALIDATIONFOLDS** The number of cross validation folds to execute.

  **-a, --accuracyMetric ACCURACYMETRIC** A scikit learn accuracy metric for training.

  **-p, --predictFeatureTable PREDICTFEATURETABLE** A unclassified feature table to be predicted by the model.

  **-e, --listErrors** Include to see a list of which sequences in the training dataset were missclassified.

  **-v, --verbose** Inlcude to get more detailed output.

## Lab presentations and Thesis Committee Presentations

These presentations were given to either the VKC Lab durring lab meetings, or to my thesis committee.  They contain background information, and document my working progress.

* **[12/11/18 Thesis Committee Meeting](https://docs.google.com/presentation/d/1OZpYLSVLtJjkjRIWPzZq9Kgmf1haGQ5GKNgLEdJppfw/edit?usp=sharing)**: an overview of my fall semester work 
* **[12/3/18 Machine Algorithm Research ](https://docs.google.com/presentation/d/1vzqHAOpl8-pdivN2k4VXTbsyU1kNXPKU85aiaMWQXeM/edit?usp=sharing)**: algorithms under consideration presented in lab meeting
* **[11/5/18 Biological Background and Initial Project Plan](https://docs.google.com/presentation/d/1WPKPLAls7jK-ASeTeBcvSeus5B9hmag5wgbUsmXXgLU/edit?usp=sharing)**: the biological introduction to the project
* **[10/2/18 Initial Project Proposals](https://docs.google.com/presentation/d/1i0C0qMyz5Mk9t9Hvk8EW0eZWVZhmnl1Se-tbBJAQS3I/edit?usp=sharing)**: the inial ideas for this project and other potential theses


## References

See [references.txt](https://github.com/afarrellsherman/Woolf/blob/master/references.txt)