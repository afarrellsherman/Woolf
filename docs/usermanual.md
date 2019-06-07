# Woolf Model User Guide

## Introduction

In this tutorial, you will go through the steps to build a Woolf model
classifier that can classify a β-lactamase gene as either Class A
or not Class A (one of either class B, C, or D).

### What is a β-lactamase?

β-lactamases are used by a wide variety of bacteria to evade the toxic effect of β-lactam type antibiotics including penicillin family antibiotics and cephalosporins \[106\]. As the first drug ever developed to treat bacterial infection, penicillin and penicillin like drugs have been used to tread a wide verity of bacterial diseases since the 1930s \[107\]. Their long use history has allowed bacteria to evolve a number of different strategies to avoid β-lactams’ toxic effects \[107\]. These strategies are encoded in the bacteria’s DNA as a diverse set of antibiotic resistance genes, called β-lactamases, that are classified into 4 types based on the way they function \[108\]. The classes are labeled Class A, Class B, Class C, and Class D.

### Files Provided

<!-- Add instructions for downloading example files, see https://github.com/afarrellsherman/Woolf/issues/9 -->

-   FASTA amino acid sequence files
    -   `ClassA.fasta`
    -   `ClassBCD.fasta`
    -   `ClassA_test.fasta`
    -   `ClassBCD_test.fasta`
    -   `unknownClass.fasta`
-   Python Scripts
    -   `featureCSVfromFASTA.py`
    -   `trainWoolf.py`


## Installation

### Dependences

The Woolf Classifier Building Pipeline has several dependences you will
want to install into your python environment. The commands for
installation and links to the documentation are provided below. Also
note that it is best practice to store python inside a virtual
environment (see
<!-- Note: `conda` has a different virtual environment setup, might be worth changing this link -->
<https://packaging.python.org/guides/installing-using-pip-and-virtualenv/>)



#### `Python3`

You will need Python 3 rather than Python 2.7. You can install 3 if
you already have 2.7 by creating a virtual environment.

Install from: <https://realpython.com/installing-python/>

#### `Biopython`

Install with:

```sh
$ pip install biopython
```

Documentation: <https://biopython.org/wiki/Packages>

#### `Scikit-Learn`

Install with:

```sh
$ pip install -U numpy scipy scikit-learn
```

Documentation: <https://scikit-learn.org/0.16/install.html>

#### `Pandas`

Install with:

```sh
$ pip install pandas
```

Documentation: https://pandas.pydata.org/pandas-docs/stable/install.html

#### `Argparse`

Only required if you have python >3.2.

Install with:

```sh
$ pip install argparse
```

Documentation: <https://pypi.org/project/argparse/>

#### `Sys` and `Ast`

May or may not need manual installation with:

```sh
$ pip install sys
```

```sh
$ pip install ast
```

### NOTE: Using the Command Line

The scripts to build a Woolf Model run on the command line. The basic
structure of a command to run a script is:

```sh
$ python scriptName.py arguments -option
```

To get help for any command, run it with the help option:

```sh
$ python scriptName.py -h
```

## Overview: Steps in Building a Woolf Model

Woolf Classifiers can be built using a few simple commands on the
command line in 6 steps.

(1) Input FASTA files are converted into a feature table based on length
and amino acid composition before (2) being used to train a model with
either a kNN or random forest algorithm. The default parameters lead to
an initial report of accuracy and best parameters (3) which can then be
fine-tuned as inputs to the command (4). Users can also ask to see a
list of the protein sequences misclassified by the best scoring
classifier in each model (5) and predict the classes of unknown proteins
(6).

![](media/image1.png)

### STEP 1: Creating the feature tables

The FASTA files provided in the tutorial have already been split into
positive (Class A) and negative (Class B, C, and D), with test data
reserved for a final accuracy measure, and an unknown set of data. Use
featureCSVfromFasta.py to create three CSV based feature tables, one for
training, one final one for testing after you have made all the
modifications to the data, and one unlabeled table for prediction.

Training:

```sh
$ python featureCSVfromFASTA.py --binary -c AvsNotA -f CSVfolder -pf classA.fasta -nf classBCD.fasta
```

This command creates a binary (not prediction because it has class
labels) feature table that uses the Class A sequences as the positive
class, and the Class B, C, and D sequences as the negative class.

Testing:

```sh
$ python featureCSVfromFASTA.py --binary -c AvsNotA_TEST -f CSVfolder -pf classA_test.fasta -nf classBCD_test.fasta
```

Prediction:

```sh
$ python featureCSVfromFASTA.py --predict -c AvsNotA_UNKNOWN -f CSVfolder -pf unknownClass.fasta
```

After each command you should get confirmation from the command line
that the file created was the type of table you intended, and that it
has been saved to the folder with the filename you indicated. Check to
make sure the three feature table files are where you think they should
be, and that they contain feature data before continuing.

### STEP 2: Running Model with Default Parameters

Now that you have your feature tables, you can build a model to
differentiate between Class A and non-Class A β-lactamases.

First build a classifier using a kNN algorithm trained on the training
feature table:

```sh
$ python trainWoolf.py -k CSVfolder/AvsNotA.csv
```

The output should look like this:

```
Building kNN Woolf Model...
Training Model...
~~~~~~ RESULTS ~~~~~~
Score of best classifier: 0.832644774106317
Standard deviation of best score: 0.02979380521786959
Best Params:{'clf__n_neighbors': 1}
~~~~~~ ~~~~~~
```

This indicates that the model achieved an f1-measure accuracy score of
0.91 using `k=1` as an algorithm parameter. You can get more information
about the model by running the command with the `-v` option. The
results should like this:

```
Building kNN Woolf Model...
Cross-validation Folds: 5
Scoring Metric: MCC
Scaler type: MinMaxScaler
Training Model...
~~~~~~ RESULTS ~~~~~~
Score of best classifier: 0.832644774106317
Best Params:{'clf__n_neighbors': 1}
Range of classifier scores across hyperparameters:
Max: 0.832644774106317
Min: 0.8097974586532646
Range of training scores across hyperparameters:
Max: 1.0
Min: 0.919719472833318
~~~~~~ ~~~~~~
```

### STEP 3: Accuracy Metric Evaluation

There is no rule about what makes an accuracy metric “good,” but each
time you get results from the Woolf model, you can do some reasoning
about how well your classifier is working.

Classifiers that are doing well will generally:

-   Have accuracy measures above:
    -   50% accuracy
    -   0.5 f1-score
    -   0.3 MCC
-   Have `k` values over 100x the number of instances
    -   Ex: if you have 200 instances, `k` should be at least 2
    -   Greater values of `k` indicate better separation between the
        classes.
-   Have fewer trees than the maximum argument provided
-   Have more instances per leaf than the minimum argument provided

However, the main goal of the Woolf Pipeline is to provide useful
hypothesis generating biologically relevant insight into protein
sequences, not to create the best possible computational model, so no
definitive number will be able to tell you if a classifier is “good
enough.”

### STEP 4: Modifying Default Parameters

The parameters defined Table 4.1 can be specified by the user to improve
the classification power of Woolf Classifiers.

**Table 4.1** User specified parameters

  | Parameter                                                         | Default Option     | Option Flag | How to Format Input
--|-------------------------------------------------------------------|--------------------|-------------|--------------------
  | Feature scaling type                                              | Min-Max Scaling    | `-s`        | StandardScaler<br>MaxAbsScaler
  | Cross-validation folds                                            | 5                  | `-c`        | 10<br>20
  | Accuracy metric                                                   | MCC                | `-a`        | accuracy<br>f1
  | Number of neighbors (kNN only) | range from 1 to 20 | `-n`        | 5<br>1-20<br>1-30,5
  | Number of trees (random forest only)                              | range from 1 to 20 | `-t`        | 5<br>1-20<br>1-30,5
  | Minimum instances per leaf (random forest only)                   | 10, 15, 20, 25, 30 | `-l`        | 10<br>10-0<br>10-30,5


**Hyperparameter Ranges**

These options control the hyperparameter values tested by the Woolf
Pipeline and optimized in your model. If you have a small dataset, all
the values will need to be smaller. `k` values will self-regulate and
get smaller with smaller datasets, but you will need to impose upper and
lower limits for the number of trees and the minimum samples per leaf in
a random forest model to prevent overfitting. As a general rule of
thumb, try to have 20 instances per tree, and a minimum leaf size of
approximately 1/20 of the data. However, as stated above, the goal is
biological relevance, not machine learning perfection, so there is no
hard and fast rule.

For example, to create a kNN model that tests the `k` values of
1, 3, 5, and 7, you could use:

```sh
$ python trainWoolf.py -k CSVfolder/AvsNotA.csv -n 1-7,2
```

**Cross-Validation Folds**

To create a model with 10 rather than 5 cross-validation folds, run the
command like this:

```sh
$ python trainWoolf.py -k CSVfolder/AvsNotA.csv -c 10
```

Note that the number of cross validation folds must be greater than 1 so
that the data can be split at least once. In general, greater numbers of
cross-validation folds take longer to run, but give better estimates of
the model’s accuracy. If the number of folds is too high for the
dataset, you may get an error because there is not enough training data
in each split to train the model.

**Scalar Value**

Scaling is the process of modifying the center and range of the data in
each feature. It is used to modify input data distributions to meet the
assumptions most algorithms make about their input data \[100\]. Random
forests are tree based and do not require scaling, however, with
algorithms like kNNs scaling the data prevents features with different
ranges from unduly influencing the prediction \[100\].

Table 4.2 shows the range of different scalar types and when they might
be useful.
**Table 4.2** Possible Scaler Types

Scaler Name    | Function                                                                      | Suggested Use Cases
---------------|-------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------
StandardScaler | Scales each feature to zero mean and unit variance                            | - General use
MinMaxScaler   | Scales each feature to a range between 0 and 1                                | - Sparse data<br>- Possible zeros in data<br>- Small standard deviations
MaxAbsScaler   | Scales each feature to a range between -1 and 1                               | - Sparse data<br>- Possible negative data<br>- Small standard deviations
RobustScaler   | Scales using alternative center and range metrics that are robust to outliers | - Data with outliers
None           | No scaling                                                                    | - Approximately normally distributed data in similar ranges<br>- comparison to other methods

To change the scalar type from the default Min-Max Scalar to the
Standard Scalar, use this command:

```sh
$ python trainWoolf.py -k CSVfolder/AvsNotA.csv -s StandardScaler
```

To remove scaling to create a random forest Model, use this command:

```sh
$ python trainWoolf.py -f CSVfolder/AvsNotA.csv -s None
```

You should see results like this:

```
Building Random Forest Woolf Model...
Training Model...
~~~~~~ RESULTS ~~~~~~
Score of best classifier: 0.8285663419177125
Best Params:{'clf__min_samples_leaf': 13, 'clf__n_estimators':
11}
```

**Accuracy Metric**

There are five options to assess the accuracy of your classifier. These
metrics are used at each stage within cross validation and reported at
the end of the training. The default option is the Matthews Correlation
Coefficient (MCC), which has been shown to be good for small unbalanced
datasets where both the positive and negative class is important.

To use percentage accuracy as the accuracy metric instead of the default
MCC, use this command:

```sh
$ python trainWoolf.py -k CSVfolder/AvsNotA.csv -v -a accuracy
```

All possible accuracy metrics are described in Table 4.3.

 **Table 4.3 Possible Accuracy Metrics.** All implementations come from the scikit-lean preprocessing package \[101\].
<!-- TODO: Equations need fixing, see https://stackoverflow.com/questions/35498525/latex-rendering-in-readme-md-on-github -->

Metric    | Description                                                                         | Function                                                                                  | Suggested Use Cases
----------|-------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------
accuracy  | Percentage of instances classified correctly                                        | $$\frac{TP + TN}{TP + FP + FN + TN}$$                                                     | Balanced class distributions of instances
recall    | Proportion of actually positive instances that are correctly identified as positive | $$\frac{\text{TP}}{TP + FN}$$                                                             | When the most important result it to identify all the positive cases
precision | Proportion of predicted positive instances that are actually positive               | $$\frac{\text{TP}}{TP + FP}$$                                                             | When it is important to make sure all the predicted positives are really positive
f1        | Harmonic mean of recall and precision                                               | $$\frac{2(p \times r)}{p + r}$$                                                           | When both recall and precision are important
MCC       | Combination of all terms from confusion matrix                                      | $$\frac{TP\  \times \ TN - FP\  \times FN}{\sqrt{(TP + FN)(TP + FP)(TN + FP)(TN + FN)}}$$ | Small datasets in which both positive and negative classes are important

### STEP 5: Listing Misclassified Proteins

To determine which proteins are misclassified by your final model, run
the script again with the `-e` option. Assuming your final model was a
kNN trained with percentage accuracy and 3-10 as possible k values, you
would run the following command:

```sh
$ python trainWoolf.py -k CSVfolder/AvsNotA.csv -a accuracy -n 4-10 -e
```

You should get results that look like this:

```
Building kNN Woolf Model...
Training Model...
~~~~~~ RESULTS ~~~~~~
Score of best classifier: 0.9090318860447215
Best Params:{'clf__n_neighbors': 4}
~~~~~~ ~~~~~~
Listing misclassified instances
misclassified as positive class:

['EIT76073.1', 'WP_121940274.1', 'SFE08607.1', 'KUK79721.1',
'SDU95206.1', 'SEE70256.1', 'SEE30393.1', 'WP_013151481.1',
'WP_101502916.1', 'WP_012895319.1', 'WP_026824192.1',
'WP_128836872.1', 'WP_127568596.1', 'WP_123152110.1',
'WP_008504272.1', 'WP_011497575.1', 'WP_012831211.1',
'WP_013752449.1', 'WP_012287432.1', 'WP_011759294.1',
'WP_086947865.1', 'AEK44086.1'\]

misclassified as negative class:

['WP_129745509.1', 'WP_129745937.1', 'WP_129749158.1',
'WP_129654766.1', 'WP_007481284.1', 'WP_129584969.1',
'WP_128916907.1', 'WP_128919506.1', 'WP_128943966.1',
'WP_128945668.1', 'WP_128946536.1', 'WP_128911376.1',
'WP_124394870.1', 'WP_128836226.1', 'WP_128836873.1',
'WP_128837474.1', 'WP_128797655.1', 'WP_128795559.1',
'WP_128617379.1', 'WP_115702137.1', 'WP_127566621.1',
'WP_126411272.1', 'WP_126337303.1', 'WP_126404864.1',
'WP_126634890.1', 'WP_124325291.1', 'WP_126411131.1',
'WP_126167828.1', 'WP_125469785.1', 'WP_125148997.1',
'WP_124114574.1', 'WP_124114133.1', 'WP_123939366.1',
'WP_123291711.1', 'WP_123637641.1', 'WP_123679477.1',
'WP_123657470.1', 'WP_123591130.1', 'WP_123438002.1',
'WP_123069295.1', 'WP_122443884.1', 'WP_122497446.1',
'WP_121211065.1', 'WP_115300326.1', 'WP_120215311.1',
'WP_120218024.1', 'WP_119700268.1', 'WP_118763952.1',
'WP_034241719.1', 'WP_117176239.1', 'WP_117395343.1',
'WP_117174207.1', 'WP_116675890.1', 'WP_116612552.1',
'WP_115181656.1', 'WP_115653569.1', 'WP_115327361.1',
'WP_115320774.1', 'WP_115272997.1', 'WP_115297885.1',
'WP_115222632.1', 'WP_115303624.1', 'WP_115241962.1',
'WP_114980594.1', 'WP_115175906.1', 'WP_114889885.1',
'WP_114910097.1', 'WP_055392689.1', 'WP_058032294.1',
'WP_008620049.1', 'WP_008624220.1', 'WP_076381892.1',
'WP_008546521.1', 'WP_023978354.1', 'WP_012225639.1']
```

The output lists the proteins in the training data that were either
misclassified as Type A, but actually belong to one of the other classes
(misclassified as positive), or were misclassified as not Type A, but in
fact are (misclassified as negative). These barcodes can be used to find
the original sequences for further analysis.

### STEP 6: Predicting New Proteins

The final step in the Woolf Classification Building Pipeline is to
actually predict the function of new proteins. This is done with the
`-p` option. Before you do, it is useful to get a final accuracy
measure with data that has never been through the model up until now.
This is done with the same option flag.

To test a model with the test data feature table you made in step one
use the following command:

```sh
$ python trainWoolf.py -k CSVfolder/AvsNotA.csv -p CSVfolder/AvsNotA_TEST.csv
```

You should see results like this:

```
Building kNN Woolf Model...
Training Model...

~~~~~~ RESULTS ~~~~~~
Score of best classifier: 0.832644774106317
Best Params:{'clf__n_neighbors': 1}
~~~~~~ ~~~~~~

Predicting novel instances

{'WP_013188475.1': 1, 'WP_001931474.1': 1, 'WP_015058868.1': 1,
'WP_032277257.1': 1, 'WP_011091028.1': 1, 'WP_000239590.1': 1,
'WP_025368620.1': 1, 'WP_053444694.1': 1, 'WP_001617865.1': 1,
'WP_000027057.1': 1, 'WP_015387340.1': 1, 'WP_003015755.1': 1,
'WP_003015518.1': 1, 'WP_004197546.1': 1, 'WP_002904004.1': 1,
'WP_012477595.1': 1, 'WP_130451746.1': 1, 'WP_130333879.1': 1,
'WP_066599917.1': 1, 'WP_035895532.1': 1, 'WP_005068900.1': 1,
'WP_000352430.1': 1, 'WP_003634596.1': 1, 'WP_000874931.1': 1,
'WP_001100753.1': 1, 'WP_004179754.1': 1, 'WP_013188473.1': 1,
'WP_015058867.1': 1, 'WP_004199234.1': 1, 'WP_000733283.1': 1,
'WP_000733271.1': 1, 'WP_004176269.1': 1, 'WP_129609116.1': 1,
'WP_110123529.1': 1, 'WP_116721879.1': 1, 'ORN50155.1': 1,
'WP_075986622.1': 1, 'WP_044662084.1': 1, 'WP_020835015.1': 1,
'WP_000733276.1': 1, 'WP_063864653.1': 1, 'WP_002164538.1': 1,
'WP_002101021.1': 1, 'WP_039493569.1': 0, 'WP_039496288.1': 0,
'WP_004201164.1': 0, 'WP_039469786.1': 0, 'WP_000742473.1': 0,
'WP_129757379.1': 0, 'WP_129749067.1': 0, 'WP_129653498.1': 0,
'WP_023408309.1': 0, 'WP_000778180.1': 0, 'WP_001367937.1': 0,
'WP_001299465.1': 0, 'WP_001339114.1': 0, 'WP_001317579.1': 0,
'WP_000976514.1': 0, 'WP_001523751.1': 0, 'WP_001339477.1': 0,
'WP_001352591.1': 0, 'WP_024225500.1': 0, 'WP_001361488.1': 0,
'WP_012139762.1': 0, 'WP_001336292.1': 0, 'WP_001460207.1': 0,
'WP_001376670.1': 0, 'WP_005053920.1': 0, 'WP_005114784.1': 0,
'WP_045149331.1': 0, 'WP_005111907.1': 0, 'WP_001300820.1': 0,
'WP_009667650.1': 0, 'WP_013850585.1': 0, 'WP_006081706.1': 0,
'WP_013169234.1': 0, 'WP_009177260.1': 0, 'WP_004714767.1': 0,
'WP_015950416.1': 0, 'WP_012587601.1': 0, 'WP_012314241.1': 0,
'WP_012018474.1': 0, 'WP_011622707.1': 0, 'WP_011626203.1': 0,
'WP_011716980.1': 0, 'WP_011919325.1': 0, 'WP_011846786.1': 0,
'WP_001531742.1': 0, 'WP_001659360.1': 0, 'WP_001711023.1': 0,
'WP_001681940.1': 0, 'WP_001417211.1': 0, 'WP_009585129.1': 0,
'WP_007675122.1': 0, 'WP_007761109.1': 0, 'WP_014007498.1': 0,
'WP_003499687.1': 0, 'WP_013691409.1': 0, 'WP_013761358.1': 0,
'WP_006384871.1': 0, 'WP_013394930.1': 0, 'WP_006220425.1': 0,
'WP_013343304.1': 0, 'WP_013091659.1': 0, 'WP_006052187.1': 0,
'WP_012250756.1': 0, 'WP_012337063.1': 0, 'WP_085779089.1': 0,
'WP_020305829.1': 0, 'WP_012052554.1': 0, 'WP_085116644.1': 0,
'WP_071849985.1': 1, 'WP_048624885.1': 0, 'WP_046101847.1': 0,
'WP_041023628.1': 0, 'WP_045489586.1': 0, 'WP_035261877.1': 0,
'WP_045460298.1': 0, 'WP_025373271.1': 0, 'WP_024092339.1': 0,
'WP_023653734.1': 0, 'WP_022562602.1': 0, 'WP_020786480.1': 0,
'WP_020443915.1': 0, 'WP_020296865.1': 0, 'WP_020288732.1': 0,
'WP_020302602.1': 0, 'WP_018611413.1': 0, 'WP_008912959.1': 0,
'WP_013812748.1': 0, 'WP_013592279.1': 0, 'WP_013509122.1': 0,
'WP_006686288.1': 0, 'WP_012145001.1': 0, 'WP_011505503.1': 0,
'WP_074072297.1': 0, 'WP_060769150.1': 0, 'WP_047213261.1': 0,
'WP_006578319.1': 0, 'WP_082929673.1': 0, 'WP_065948248.1': 0,
'WP_065872869.1': 0, 'WP_065880648.1': 0, 'WP_065890887.1': 0,
'WP_065928025.1': 0, 'WP_065895410.1': 0, 'WP_065909522.1': 0,
'WP_065885292.1': 0, 'WP_065878451.1': 0, 'WP_065869409.1': 0,
'WP_065503970.1': 0, 'WP_054452744.1': 0, 'WP_064597896.1': 0,
'WP_061555327.1': 0, 'WP_082806966.1': 0, 'WP_061541403.1': 0,
'WP_033757684.1': 0, 'WP_038492143.1': 0, 'WP_035730667.1': 0,
'WP_060419126.1': 0, 'WP_067436871.1': 0, 'WP_059182486.1': 0,
'WP_058021331.1': 0, 'WP_056784645.1': 0, 'WP_054882571.1': 0,
'WP_046237244.1': 0, 'WP_071840539.1': 0, 'WP_049601150.1': 0,
'WP_060844168.1': 0, 'WP_060840246.1': 0, 'WP_033057352.1': 0,
'WP_050680469.1': 0, 'WP_050534676.1': 0, 'WP_050540198.1': 0,
'WP_049607872.1': 0, 'WP_072089562.1': 0, 'WP_049616313.1': 0,
'WP_072082310.1': 0, 'WP_048227211.1': 0, 'WP_048236297.1': 0,
'WP_048222344.1': 0, 'WP_046855210.1': 0, 'WP_050086780.1': 0,
'WP_057620914.1': 0, 'WP_044459295.1': 0, 'WP_071841543.1': 0,
'WP_035564089.1': 0, 'WP_031376719.1': 0, 'WP_065814057.1': 0,
'WP_043018158.1': 0, 'WP_032679412.1': 0, 'WP_033638425.1': 0,
'WP_024013480.1': 0, 'WP_016656628.1': 0, 'WP_015700263.1': 0,
'WP_005122150.1': 0, 'WP_004923631.1': 0, 'WP_038489723.1': 0,
'WP_033732716.1': 0, 'WP_044550790.1': 0, 'WP_037962530.1': 0,
'WP_032887178.1': 0, 'WP_047597435.1': 0, 'WP_025339397.1': 0,
'WP_005330568.1': 0, 'WP_010458642.1': 0, 'WP_007965416.1': 0,
'WP_007742644.1': 0, 'WP_020826741.1': 0, 'WP_020724617.1': 0,
'WP_016492932.1': 0, 'WP_016151399.1': 0, 'WP_016149438.1': 0,
'WP_007748831.1': 0, 'WP_013366957.1': 0, 'WP_013357894.1': 0,
'WP_013203868.1': 0, 'WP_074064204.1': 0, 'WP_047429863.1': 0,
'WP_016542230.1': 0, 'WP_016162495.1': 0, 'WP_009508908.1': 0,
'WP_007480812.1': 0, 'WP_065506251.1': 0, 'WP_081279377.1': 0,
'WP_081277750.1': 0, 'WP_061518155.1': 0, 'WP_061524383.1': 0,
'WP_061516136.1': 0, 'WP_062573657.1': 0, 'WP_058708125.1': 0,
'WP_058701878.1': 0, 'WP_047954938.1': 0, 'WP_029307868.1': 0,
'WP_057430086.1': 0, 'WP_057397006.1': 0, 'WP_054423529.1': 0,
'WP_053010118.1': 0, 'WP_072077720.1': 0, 'WP_050135449.1': 0,
'WP_050144425.1': 0, 'WP_072136784.1': 0, 'WP_072186958.1': 0,
'WP_072078661.1': 0, 'WP_044420034.1': 0, 'WP_044390253.1': 0,
'WP_042568790.1': 0, 'WP_047715209.1': 0, 'WP_071841717.1': 0,
'WP_072089849.1': 0, 'WP_072078020.1': 0, 'WP_050088644.1': 0,
'WP_072088286.1': 0, 'WP_049607427.1': 0, 'WP_072081726.1': 0,
'WP_050073671.1': 0, 'WP_048286820.1': 0, 'WP_048273893.1': 0,
'WP_048284614.1': 0, 'WP_047355585.1': 0, 'WP_045882124.1': 0,
'WP_045792035.1': 0, 'WP_045269678.1': 0, 'WP_044293428.1': 0,
'WP_042560048.1': 0, 'WP_042086213.1': 0, 'WP_020928562.1': 0,
'WP_004910271.1': 0, 'WP_047414966.1': 0, 'WP_047500028.1': 0,
'WP_039340300.1': 0, 'WP_037140816.1': 0, 'WP_035225479.1': 0,
'WP_024474547.1': 0, 'WP_038409596.1': 0, 'WP_036966456.1': 0,
'WP_036959629.1': 0, 'WP_036974156.1': 0, 'WP_036977846.1': 0,
'WP_036948496.1': 0, 'WP_025416832.1': 0, 'WP_025395172.1': 0,
'WP_023533520.1': 0, 'WP_022625635.1': 0, 'WP_021491540.1': 0,
'WP_019692735.1': 0, 'WP_020431495.1': 0, 'WP_016500007.1': 0,
'WP_004637248.1': 0, 'WP_004262799.1': 0, 'WP_045902232.1': 0,
'WP_060460871.1': 0, 'WP_060442301.1': 0, 'WP_060431700.1': 0,
'WP_060455639.1': 0, 'WP_060437608.1': 0, 'WP_060432983.1': 0,
'WP_060438709.1': 0, 'WP_060418500.1': 0, 'WP_050880653.1': 0,
'WP_050918486.1': 0, 'WP_050162987.1': 0, 'WP_050158303.1': 0,
'WP_050130984.1': 0, 'WP_050160138.1': 0, 'WP_050321664.1': 0,
'WP_050322708.1': 0, 'WP_050335261.1': 0, 'WP_048324983.1': 0,
'WP_047360713.1': 0, 'WP_048233629.1': 0, 'WP_039570340.1': 0,
'WP_043179244.1': 0, 'WP_034622813.1': 0, 'WP_038448376.1': 0,
'WP_025207685.1': 0, 'WP_025328859.1': 0, 'WP_016453823.1': 0,
'WP_016453249.1': 0, 'WP_013983315.1': 0, 'WP_011946603.1': 0,
'WP_034196516.1': 0, 'WP_034188536.1': 0, 'WP_034040414.1': 0,
'WP_014475645.1': 0, 'WP_020914447.1': 0, 'WP_057099948.1': 0,
'WP_057992932.1': 0, 'WP_057037937.1': 0, 'WP_039124095.1': 0,
'WP_044780371.1': 0, 'WP_050460055.1': 0, 'WP_032071425.1': 0,
'WP_031955431.1': 0, 'WP_032017448.1': 0, 'WP_032046023.1': 0,
'WP_031972720.1': 0, 'WP_031991294.1': 0, 'WP_032019111.1': 0,
'WP_032026533.1': 0, 'WP_031950449.1': 0, 'WP_032039758.1': 0,
'WP_033853219.1': 0, 'WP_032045193.1': 0, 'WP_032034494.1': 0,
'WP_032061328.1': 0, 'WP_032070286.1': 0, 'WP_032015622.1': 0,
'WP_032037742.1': 0, 'WP_032027613.1': 0, 'WP_032009364.1': 0,
'WP_042757256.1': 0, 'WP_031636917.1': 0, 'WP_034324889.1': 0,
'WP_011860820.1': 0, 'AOH51342.1': 0, 'WP_013279374.1': 0,
'WP_063862740.1': 0, 'WP_063862735.1': 0, 'WP_063862730.1': 0,
'WP_063862729.1': 0, 'WP_063862728.1': 0, 'WP_063862727.1': 0,
'WP_063862726.1': 0, 'WP_063862725.1': 0, 'WP_063862724.1': 0,
'WP_063862723.1': 0, 'WP_063862722.1': 0, 'WP_063862721.1': 0,
'WP_063862719.1': 0, 'WP_063862420.1': 0, 'WP_063862718.1': 0,
'WP_063862408.1': 0, 'WP_063862402.1': 0, 'WP_047023509.1': 0,
'WP_057625895.1': 0, 'WP_057631141.1': 0, 'WP_057627739.1': 0,
'WP_071447731.1': 0, 'EAB9198241.1': 0, 'WP_063086404.1': 0,
'WP_001439279.1': 0, 'WP_001350795.1': 0}

Score on test data: 0.987116201732058
```

The overall accuracy score is the last number printed.

Finally, to run the model to predict your unknown proteins, use the
following command. Remember that `AvsNotA_UNKNOWN.csv` is a feature table
file you generated in step 1.

```sh
$ python trainWoolf.py -k CSVfolder/AvsNotA.csv -p CSVfolder/AvsNotA_UNKNOWN.csv
```

The results should look like this:

```
Building kNN Woolf Model...
Training Model...

~~~~~~ RESULTS ~~~~~~
Score of best classifier: 0.832644774106317
Best Params:{'clf__n_neighbors': 1}
~~~~~~ ~~~~~~

Predicting novel instances

{'WP_050067789.1': 0, 'WP_021577770.1': 0, 'WP_023224609.1': 1,
'WP_017442020.1': 1, 'WP_001630205.1': 0, 'WP_001631316.1': 1,
'WP_002852433.1': 0, 'WP_002856956.1': 0, 'WP_000830775.1': 0,
'WP_001317977.1': 0, 'WP_001082962.1': 1, 'WP_000830777.1': 0,
'WP_000830773.1': 0, 'WP_000059908.1': 0, 'WP_057991827.1': 0,
'WP_000673293.1': 0, 'WP_002776717.1': 0, 'WP_000817293.1': 0,
'WP_001082975.1': 1, 'WP_001208005.1': 1, 'WP_023216810.1': 1,
'WP_023993659.1': 0, 'WP_001667037.1': 0, 'WP_000673298.1': 0,
'WP_001208011.1': 1, 'WP_000673287.1': 0, 'WP_001520983.1': 0,
'WP_001082970.1': 1, 'WP_002865991.1': 0, 'WP_020899073.1': 0,
'WP_000830757.1': 0, 'WP_001327042.1': 0, 'WP_020837858.1': 1,
'WP_000188069.1': 0, 'WP_001082979.1': 1, 'WP_022645952.1': 0,
'WP_001299057.1': 0, 'WP_001931474.1': 1, 'WP_023259161.1': 0,
'WP_111742248.1': 1}
```

And that is it! You have built a Woolf Classifier that can predict if
novel β-lacamases are Type A or not Type A. Using the barcodes
provided in by the `-p` option, you can further study these sequences
using any conventional experimental or computational technique.