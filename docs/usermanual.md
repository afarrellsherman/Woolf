 {#section .ListParagraph}

User Manual {#user-manual .ListParagraph}
-----------

**Woolf Model User Guide**

In this tutorial, you will go through the steps to build a Woolf model
classifier that can classify a $\beta$-lactamase gene as either Class A
or not Class A (one of either class B, C, or D).

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **What is a** $\mathbf{\beta}$**-lactamase?**
  
  $\beta$-lactamases are used by a wide variety of bacteria to evade the toxic effect of $\beta$-lactam type antibiotics including penicillin family antibiotics and cephalosporins \[106\]. As the first drug ever developed to treat bacterial infection, penicillin and penicillin like drugs have been used to tread a wide verity of bacterial diseases since the 1930s \[107\]. Their long use history has allowed bacteria to evolve a number of different strategies to avoid $\beta$-lactams’ toxic effects \[107\]. These strategies are encoded in the bacteria’s DNA as a diverse set of antibiotic resistance genes, called $\beta$-lactamases, that are classified into 4 types based on the way they function \[108\]. The classes are labeled Class A, Class B, Class C, and Class D.
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Files Provided**

-   FASTA amino acid sequence files

    -   ClassA.fasta

    -   ClassBCD.fasta

    -   ClassA\_test.fasta

    -   ClassBCD\_test.fasta

    -   unknownClass.fasta

-   Python Scripts

    -   featureCSVfromFASTA.py

    -   trainWoolf.py

**Dependences**

The Woolf Classifier Building Pipeline has several dependences you will
want to install into your python environment. The commands for
installation and links to the documentation are provided below. Also
note that it is best practice to store python inside a virtual
environment (see
<https://packaging.python.org/guides/installing-using-pip-and-virtualenv/>)

*Python3*

> You will need Python 3 rather than Python 2.7. You can install 3 if
> you already have 2.7 by creating a virtual environment.

Install from: <https://realpython.com/installing-python/>

*Biopython*

Install with: pip install biopython

Documentation: <https://biopython.org/wiki/Packages>

*Scikit-Learn*

Install with: pip install -U numpy scipy scikit-learn

Documentation: <https://scikit-learn.org/0.16/install.html>

*Pandas*

Install with: pip install pandas

Documentation: https://pandas.pydata.org/pandas-docs/stable/install.html

*Argparse*

Only required if you have python &gt;3.2.

Install with: pip install argparse

Documentation: <https://pypi.org/project/argparse/>

*Sys* and *Ast*

May or may not need manual installation with:

Pip install sys

Pip install ast

**NOTE: Using the Command Line**

The scripts to build a Woolf Model run on the command line. The basic
structure of a command to run a script is:

\$ python scriptName.py arguments -option

To get help for any command, run it with the help option:

\$ python scriptName.py -h

**Overview: Steps in Building a Woolf Model**

Woolf Classifiers can be built using a few simple commands on the
command line in 6 steps.

\(1) Input FASTA files are converted into a feature table based on length
and amino acid composition before (2) being used to train a model with
either a kNN or random forest algorithm. The default parameters lead to
an initial report of accuracy and best parameters (3) which can then be
fine-tuned as inputs to the command (4). Users can also ask to see a
list of the protein sequences misclassified by the best scoring
classifier in each model (5) and predict the classes of unknown proteins
(6).

![](docs//media/image1.png){width="6.5in" height="3.5894389763779526in"}

**STEP 1: Creating the feature tables**

The FASTA files provided in the tutorial have already been split into
positive (Class A) and negative (Class B, C, and D), with test data
reserved for a final accuracy measure, and an unknown set of data. Use
featureCSVfromFasta.py to create three CSV based feature tables, one for
training, one final one for testing after you have made all the
modifications to the data, and one unlabeled table for prediction.

Training:

\$ python featureCSVfromFASTA.py --binary -c AvsNotA -f CSVfolder -pf
classA.fasta -nf classBCD.fasta

This command creates a binary (not prediction because it has class
labels) feature table that uses the Class A sequences as the positive
class, and the Class B, C, and D sequences as the negative class.

Testing:

\$ python featureCSVfromFASTA.py --binary -c AvsNotA\_TEST -f CSVfolder
-pf classA\_test.fasta -nf classBCD\_test.fasta

Prediction:

\$ python featureCSVfromFASTA.py --predict -c AvsNotA\_UNKNOWN -f
CSVfolder -pf unknownClass.fasta

After each command you should get confirmation from the command line
that the file created was the type of table you intended, and that it
has been saved to the folder with the filename you indicated. Check to
make sure the three feature table files are where you think they should
be, and that they contain feature data before continuing.

**STEP 2: Running Model with Default Parameters**

Now that you have your feature tables, you can build a model to
differentiate between Class A and non-Class A beta-lactamases.

First build a classifier using a kNN algorithm trained on the training
feature table:

\$ python trainWoolf.py -k CSVfolder/AvsNotA.csv

The output should look like this:

Building kNN Woolf Model...

Training Model...

\~\~\~\~\~\~ RESULTS \~\~\~\~\~\~

Score of best classifier: 0.832644774106317

Standard deviation of best score: 0.02979380521786959

Best Params:{'clf\_\_n\_neighbors': 1}

\~\~\~\~\~\~ \~\~\~\~\~\~

This indicates that the model achieved an f1-measure accuracy score of
0.91 using k=1 as an algorithm parameter. You can get more information
about the model by running the command with the $- v$ option. The
results should like this:

Building kNN Woolf Model...

Cross-validation Folds: 5

Scoring Metric: MCC

Scaler type: MinMaxScaler

Training Model...

\~\~\~\~\~\~ RESULTS \~\~\~\~\~\~

Score of best classifier: 0.832644774106317

Best Params:{'clf\_\_n\_neighbors': 1}

Range of classifier scores across hyperparameters:

Max: 0.832644774106317

Min: 0.8097974586532646

Range of training scores across hyperparameters:

Max: 1.0

Min: 0.919719472833318

\~\~\~\~\~\~ \~\~\~\~\~\~

**STEP 3: Accuracy Metric Evaluation**

There is no rule about what makes an accuracy metric “good,” but each
time you get results from the Woolf model, you can do some reasoning
about how well your classifier is working.

Classifiers that are doing well will generally:

-   Have accuracy measures above:

    -   50% accuracy

    -   0.5 f1-score

    -   0.3 MCC

-   Have $k$ values over 100x the number of instances

    -   Ex: if you have 200 instances, $k$ should be at least 2

    -   Greater values of $k$ indicate better separation between the
        classes.

-   Have fewer trees than the maximum argument provided

-   Have more instances per leaf than the minimum argument provided

However, the main goal of the Woolf Pipeline is to provide useful
hypothesis generating biologically relevant insight into protein
sequences, not to create the best possible computational model, so no
definitive number will be able to tell you if a classifier is “good
enough.”

**STEP 4: Modifying Default Parameters**

The parameters defined Table 4.1 can be specified by the user to improve
the classification power of Woolf Classifiers.

**Table 4.1** User specified parameters

  ---------------------------------------------------------------------------------------------------------------------------------------------
                                     Parameter                                         Default Option       Option Flag   How to Format Input
  ---------------------------------- ------------------------------------------------- -------------------- ------------- ---------------------
                                     Feature scaling type                              Min-Max Scaling      $- s$         StandardScaler
                                                                                                                          
                                                                                                                          MaxAbsScaler

                                     Cross-validation folds                            5                    $- c$         10
                                                                                                                          
                                                                                                                          20

                                     Accuracy metric                                   MCC                  $- a$         accuracy
                                                                                                                          
                                                                                                                          f1

  Algorithm Hyper-Parameter Ranges   Number of neighbors (kNN only)                    range from 1 to 20   $- n$         5
                                                                                                                          
                                                                                                                          1-20
                                                                                                                          
                                                                                                                          1-30,5

                                     Number of trees (random forest only)              range from 1 to 20   $- t$         5
                                                                                                                          
                                                                                                                          1-20
                                                                                                                          
                                                                                                                          1-30,5

                                     Minimum instances per leaf (random forest only)   10, 15, 20, 25, 30   $- l$         10
                                                                                                                          
                                                                                                                          10-50
                                                                                                                          
                                                                                                                          10-30,5
  ---------------------------------------------------------------------------------------------------------------------------------------------

**Hyperparameter Ranges**

These options control the hyperparameter values tested by the Woolf
Pipeline and optimized in your model. If you have a small dataset, all
the values will need to be smaller. $k$ values will self-regulate and
get smaller with smaller datasets, but you will need to impose upper and
lower limits for the number of trees and the minimum samples per leaf in
a random forest model to prevent overfitting. As a general rule of
thumb, try to have 20 instances per tree, and a minimum leaf size of
approximately 1/20 of the data. However, as stated above, the goal is
biological relevance, not machine learning perfection, so there is no
hard and fast rule.

For example, to create a kNN model that tests the $\text{k\ }$values of
1, 3, 5, and 7, you could use:

\$ python trainWoolf.py -k CSVfolder/AvsNotA.csv -n 1-7,2

**Cross-Validation Folds**

To create a model with 10 rather than 5 cross-validation folds, run the
command like this:

\$ python trainWoolf.py -k CSVfolder/AvsNotA.csv -c 10

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

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Table 4.2** Possible Scaler Types
  ------------------------------------- ------------------------------------------------------------------------------- -------------------------------------------------------------
  **Scaler Name**                       **Function**                                                                    **Suggested Use Cases**

  StandardScaler                        Scales each feature to zero mean and unit variance                              - General use

  MinMaxScaler                          Scales each feature to a range between 0 and 1                                  - Sparse data
                                                                                                                        
                                                                                                                        - Possible zeros in data
                                                                                                                        
                                                                                                                        - Small standard deviations

  MaxAbsScaler                          Scales each feature to a range between -1 and 1                                 - Sparse data
                                                                                                                        
                                                                                                                        - Possible negative data
                                                                                                                        
                                                                                                                        - Small standard deviations

  RobustScaler                          Scales using alternative center and range metrics that are robust to outliers   - Data with outliers

  None                                  No scaling                                                                      - Approximately normally distributed data in similar ranges
                                                                                                                        
                                                                                                                        - comparison to other methods
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

To change the scalar type from the default Min-Max Scalar to the
Standard Scalar, use this command:

\$ python trainWoolf.py -k CSVfolder/AvsNotA.csv -s StandardScaler

To remove scaling to create a random forest Model, use this command:

\$ python trainWoolf.py -f CSVfolder/AvsNotA.csv -s None

You should see results like this:

Building Random Forest Woolf Model...

Training Model...

\~\~\~\~\~\~ RESULTS \~\~\~\~\~\~

Score of best classifier: 0.8285663419177125

Best Params:{'clf\_\_min\_samples\_leaf': 13, 'clf\_\_n\_estimators':
11}

**Accuracy Metric**

There are five options to assess the accuracy of your classifier. These
metrics are used at each stage within cross validation and reported at
the end of the training. The default option is the Matthews Correlation
Coefficient (MCC), which has been shown to be good for small unbalanced
datasets where both the positive and negative class is important.

To use percentage accuracy as the accuracy metric instead of the default
MCC, use this command:

\$ python trainWoolf.py -k CSVfolder/AvsNotA.csv -v -a accuracy

All possible accuracy metrics are described in Table 4.3.

  **Table 4.3 Possible Accuracy Metrics.** All implementations come from the scikit-lean preprocessing package \[101\].
  ----------------------------------------------------------------------------------------------------------------------- ------------------------------------------------------------------------------------- ------------------------------------------------------------------------------------------- -----------------------------------------------------------------------------------
  **Metric**                                                                                                              **Description**                                                                       **Function**                                                                                **Suggested Use Cases**
  accuracy                                                                                                                Percentage of instances classified correctly                                          $$\frac{TP + TN}{TP + FP + FN + TN}$$                                                       Balanced class distributions of instances
  recall                                                                                                                  Proportion of actually positive instances that are correctly identified as positive   $$\frac{\text{TP}}{TP + FN}$$                                                               When the most important result it to identify all the positive cases
  precision                                                                                                               Proportion of predicted positive instances that are actually positive                 $$\frac{\text{TP}}{TP + FP}$$                                                               When it is important to make sure all the predicted positives are really positive
  f1                                                                                                                      Harmonic mean of recall and precision                                                 $$\frac{2(p \times r)}{p + r}$$                                                             When both recall and precision are important
  MCC                                                                                                                     Combination of all terms from confusion matrix                                        $$\frac{TP\  \times \ TN - FP\  \times FN}{\sqrt{(TP + FN)(TP + FP)(TN + FP)(TN + FN)}}$$   Small datasets in which both positive and negative classes are important

**STEP 5: Listing Misclassified Proteins**

To determine which proteins are misclassified by your final model, run
the script again with the $- e$ option. Assuming your final model was a
kNN trained with percentage accuracy and 3-10 as possible k values, you
would run the following command:

\$ python trainWoolf.py -k CSVfolder/AvsNotA.csv -a accuracy -n 4-10 -e

You should get results that look like this:

Building kNN Woolf Model...

Training Model...

\~\~\~\~\~\~ RESULTS \~\~\~\~\~\~

Score of best classifier: 0.9090318860447215

Best Params:{'clf\_\_n\_neighbors': 4}

\~\~\~\~\~\~ \~\~\~\~\~\~

Listing misclassified instances

misclassified as positive class:

\['EIT76073.1', 'WP\_121940274.1', 'SFE08607.1', 'KUK79721.1',
'SDU95206.1', 'SEE70256.1', 'SEE30393.1', 'WP\_013151481.1',
'WP\_101502916.1', 'WP\_012895319.1', 'WP\_026824192.1',
'WP\_128836872.1', 'WP\_127568596.1', 'WP\_123152110.1',
'WP\_008504272.1', 'WP\_011497575.1', 'WP\_012831211.1',
'WP\_013752449.1', 'WP\_012287432.1', 'WP\_011759294.1',
'WP\_086947865.1', 'AEK44086.1'\]

misclassified as negative class:

\['WP\_129745509.1', 'WP\_129745937.1', 'WP\_129749158.1',
'WP\_129654766.1', 'WP\_007481284.1', 'WP\_129584969.1',
'WP\_128916907.1', 'WP\_128919506.1', 'WP\_128943966.1',
'WP\_128945668.1', 'WP\_128946536.1', 'WP\_128911376.1',
'WP\_124394870.1', 'WP\_128836226.1', 'WP\_128836873.1',
'WP\_128837474.1', 'WP\_128797655.1', 'WP\_128795559.1',
'WP\_128617379.1', 'WP\_115702137.1', 'WP\_127566621.1',
'WP\_126411272.1', 'WP\_126337303.1', 'WP\_126404864.1',
'WP\_126634890.1', 'WP\_124325291.1', 'WP\_126411131.1',
'WP\_126167828.1', 'WP\_125469785.1', 'WP\_125148997.1',
'WP\_124114574.1', 'WP\_124114133.1', 'WP\_123939366.1',
'WP\_123291711.1', 'WP\_123637641.1', 'WP\_123679477.1',
'WP\_123657470.1', 'WP\_123591130.1', 'WP\_123438002.1',
'WP\_123069295.1', 'WP\_122443884.1', 'WP\_122497446.1',
'WP\_121211065.1', 'WP\_115300326.1', 'WP\_120215311.1',
'WP\_120218024.1', 'WP\_119700268.1', 'WP\_118763952.1',
'WP\_034241719.1', 'WP\_117176239.1', 'WP\_117395343.1',
'WP\_117174207.1', 'WP\_116675890.1', 'WP\_116612552.1',
'WP\_115181656.1', 'WP\_115653569.1', 'WP\_115327361.1',
'WP\_115320774.1', 'WP\_115272997.1', 'WP\_115297885.1',
'WP\_115222632.1', 'WP\_115303624.1', 'WP\_115241962.1',
'WP\_114980594.1', 'WP\_115175906.1', 'WP\_114889885.1',
'WP\_114910097.1', 'WP\_055392689.1', 'WP\_058032294.1',
'WP\_008620049.1', 'WP\_008624220.1', 'WP\_076381892.1',
'WP\_008546521.1', 'WP\_023978354.1', 'WP\_012225639.1'\]

The output lists the proteins in the training data that were either
misclassified as Type A, but actually belong to one of the other classes
(misclassified as positive), or were misclassified as not Type A, but in
fact are (misclassified as negative). These barcodes can be used to find
the original sequences for further analysis.

**STEP 6: Predicting New Proteins**

The final step in the Woolf Classification Building Pipeline is to
actually predict the function of new proteins. This is done with the
$- p$ option. Before you do, it is useful to get a final accuracy
measure with data that has never been through the model up until now.
This is done with the same option flag.

To test a model with the test data feature table you made in step one
use the following command:

\$ python trainWoolf.py -k CSVfolder/AvsNotA.csv -p
CSVfolder/AvsNotA\_TEST.csv

You should see results like this:

Building kNN Woolf Model...

Training Model...

\~\~\~\~\~\~ RESULTS \~\~\~\~\~\~

Score of best classifier: 0.832644774106317

Best Params:{'clf\_\_n\_neighbors': 1}

\~\~\~\~\~\~ \~\~\~\~\~\~

Predicting novel instances

{'WP\_013188475.1': 1, 'WP\_001931474.1': 1, 'WP\_015058868.1': 1,
'WP\_032277257.1': 1, 'WP\_011091028.1': 1, 'WP\_000239590.1': 1,
'WP\_025368620.1': 1, 'WP\_053444694.1': 1, 'WP\_001617865.1': 1,
'WP\_000027057.1': 1, 'WP\_015387340.1': 1, 'WP\_003015755.1': 1,
'WP\_003015518.1': 1, 'WP\_004197546.1': 1, 'WP\_002904004.1': 1,
'WP\_012477595.1': 1, 'WP\_130451746.1': 1, 'WP\_130333879.1': 1,
'WP\_066599917.1': 1, 'WP\_035895532.1': 1, 'WP\_005068900.1': 1,
'WP\_000352430.1': 1, 'WP\_003634596.1': 1, 'WP\_000874931.1': 1,
'WP\_001100753.1': 1, 'WP\_004179754.1': 1, 'WP\_013188473.1': 1,
'WP\_015058867.1': 1, 'WP\_004199234.1': 1, 'WP\_000733283.1': 1,
'WP\_000733271.1': 1, 'WP\_004176269.1': 1, 'WP\_129609116.1': 1,
'WP\_110123529.1': 1, 'WP\_116721879.1': 1, 'ORN50155.1': 1,
'WP\_075986622.1': 1, 'WP\_044662084.1': 1, 'WP\_020835015.1': 1,
'WP\_000733276.1': 1, 'WP\_063864653.1': 1, 'WP\_002164538.1': 1,
'WP\_002101021.1': 1, 'WP\_039493569.1': 0, 'WP\_039496288.1': 0,
'WP\_004201164.1': 0, 'WP\_039469786.1': 0, 'WP\_000742473.1': 0,
'WP\_129757379.1': 0, 'WP\_129749067.1': 0, 'WP\_129653498.1': 0,
'WP\_023408309.1': 0, 'WP\_000778180.1': 0, 'WP\_001367937.1': 0,
'WP\_001299465.1': 0, 'WP\_001339114.1': 0, 'WP\_001317579.1': 0,
'WP\_000976514.1': 0, 'WP\_001523751.1': 0, 'WP\_001339477.1': 0,
'WP\_001352591.1': 0, 'WP\_024225500.1': 0, 'WP\_001361488.1': 0,
'WP\_012139762.1': 0, 'WP\_001336292.1': 0, 'WP\_001460207.1': 0,
'WP\_001376670.1': 0, 'WP\_005053920.1': 0, 'WP\_005114784.1': 0,
'WP\_045149331.1': 0, 'WP\_005111907.1': 0, 'WP\_001300820.1': 0,
'WP\_009667650.1': 0, 'WP\_013850585.1': 0, 'WP\_006081706.1': 0,
'WP\_013169234.1': 0, 'WP\_009177260.1': 0, 'WP\_004714767.1': 0,
'WP\_015950416.1': 0, 'WP\_012587601.1': 0, 'WP\_012314241.1': 0,
'WP\_012018474.1': 0, 'WP\_011622707.1': 0, 'WP\_011626203.1': 0,
'WP\_011716980.1': 0, 'WP\_011919325.1': 0, 'WP\_011846786.1': 0,
'WP\_001531742.1': 0, 'WP\_001659360.1': 0, 'WP\_001711023.1': 0,
'WP\_001681940.1': 0, 'WP\_001417211.1': 0, 'WP\_009585129.1': 0,
'WP\_007675122.1': 0, 'WP\_007761109.1': 0, 'WP\_014007498.1': 0,
'WP\_003499687.1': 0, 'WP\_013691409.1': 0, 'WP\_013761358.1': 0,
'WP\_006384871.1': 0, 'WP\_013394930.1': 0, 'WP\_006220425.1': 0,
'WP\_013343304.1': 0, 'WP\_013091659.1': 0, 'WP\_006052187.1': 0,
'WP\_012250756.1': 0, 'WP\_012337063.1': 0, 'WP\_085779089.1': 0,
'WP\_020305829.1': 0, 'WP\_012052554.1': 0, 'WP\_085116644.1': 0,
'WP\_071849985.1': 1, 'WP\_048624885.1': 0, 'WP\_046101847.1': 0,
'WP\_041023628.1': 0, 'WP\_045489586.1': 0, 'WP\_035261877.1': 0,
'WP\_045460298.1': 0, 'WP\_025373271.1': 0, 'WP\_024092339.1': 0,
'WP\_023653734.1': 0, 'WP\_022562602.1': 0, 'WP\_020786480.1': 0,
'WP\_020443915.1': 0, 'WP\_020296865.1': 0, 'WP\_020288732.1': 0,
'WP\_020302602.1': 0, 'WP\_018611413.1': 0, 'WP\_008912959.1': 0,
'WP\_013812748.1': 0, 'WP\_013592279.1': 0, 'WP\_013509122.1': 0,
'WP\_006686288.1': 0, 'WP\_012145001.1': 0, 'WP\_011505503.1': 0,
'WP\_074072297.1': 0, 'WP\_060769150.1': 0, 'WP\_047213261.1': 0,
'WP\_006578319.1': 0, 'WP\_082929673.1': 0, 'WP\_065948248.1': 0,
'WP\_065872869.1': 0, 'WP\_065880648.1': 0, 'WP\_065890887.1': 0,
'WP\_065928025.1': 0, 'WP\_065895410.1': 0, 'WP\_065909522.1': 0,
'WP\_065885292.1': 0, 'WP\_065878451.1': 0, 'WP\_065869409.1': 0,
'WP\_065503970.1': 0, 'WP\_054452744.1': 0, 'WP\_064597896.1': 0,
'WP\_061555327.1': 0, 'WP\_082806966.1': 0, 'WP\_061541403.1': 0,
'WP\_033757684.1': 0, 'WP\_038492143.1': 0, 'WP\_035730667.1': 0,
'WP\_060419126.1': 0, 'WP\_067436871.1': 0, 'WP\_059182486.1': 0,
'WP\_058021331.1': 0, 'WP\_056784645.1': 0, 'WP\_054882571.1': 0,
'WP\_046237244.1': 0, 'WP\_071840539.1': 0, 'WP\_049601150.1': 0,
'WP\_060844168.1': 0, 'WP\_060840246.1': 0, 'WP\_033057352.1': 0,
'WP\_050680469.1': 0, 'WP\_050534676.1': 0, 'WP\_050540198.1': 0,
'WP\_049607872.1': 0, 'WP\_072089562.1': 0, 'WP\_049616313.1': 0,
'WP\_072082310.1': 0, 'WP\_048227211.1': 0, 'WP\_048236297.1': 0,
'WP\_048222344.1': 0, 'WP\_046855210.1': 0, 'WP\_050086780.1': 0,
'WP\_057620914.1': 0, 'WP\_044459295.1': 0, 'WP\_071841543.1': 0,
'WP\_035564089.1': 0, 'WP\_031376719.1': 0, 'WP\_065814057.1': 0,
'WP\_043018158.1': 0, 'WP\_032679412.1': 0, 'WP\_033638425.1': 0,
'WP\_024013480.1': 0, 'WP\_016656628.1': 0, 'WP\_015700263.1': 0,
'WP\_005122150.1': 0, 'WP\_004923631.1': 0, 'WP\_038489723.1': 0,
'WP\_033732716.1': 0, 'WP\_044550790.1': 0, 'WP\_037962530.1': 0,
'WP\_032887178.1': 0, 'WP\_047597435.1': 0, 'WP\_025339397.1': 0,
'WP\_005330568.1': 0, 'WP\_010458642.1': 0, 'WP\_007965416.1': 0,
'WP\_007742644.1': 0, 'WP\_020826741.1': 0, 'WP\_020724617.1': 0,
'WP\_016492932.1': 0, 'WP\_016151399.1': 0, 'WP\_016149438.1': 0,
'WP\_007748831.1': 0, 'WP\_013366957.1': 0, 'WP\_013357894.1': 0,
'WP\_013203868.1': 0, 'WP\_074064204.1': 0, 'WP\_047429863.1': 0,
'WP\_016542230.1': 0, 'WP\_016162495.1': 0, 'WP\_009508908.1': 0,
'WP\_007480812.1': 0, 'WP\_065506251.1': 0, 'WP\_081279377.1': 0,
'WP\_081277750.1': 0, 'WP\_061518155.1': 0, 'WP\_061524383.1': 0,
'WP\_061516136.1': 0, 'WP\_062573657.1': 0, 'WP\_058708125.1': 0,
'WP\_058701878.1': 0, 'WP\_047954938.1': 0, 'WP\_029307868.1': 0,
'WP\_057430086.1': 0, 'WP\_057397006.1': 0, 'WP\_054423529.1': 0,
'WP\_053010118.1': 0, 'WP\_072077720.1': 0, 'WP\_050135449.1': 0,
'WP\_050144425.1': 0, 'WP\_072136784.1': 0, 'WP\_072186958.1': 0,
'WP\_072078661.1': 0, 'WP\_044420034.1': 0, 'WP\_044390253.1': 0,
'WP\_042568790.1': 0, 'WP\_047715209.1': 0, 'WP\_071841717.1': 0,
'WP\_072089849.1': 0, 'WP\_072078020.1': 0, 'WP\_050088644.1': 0,
'WP\_072088286.1': 0, 'WP\_049607427.1': 0, 'WP\_072081726.1': 0,
'WP\_050073671.1': 0, 'WP\_048286820.1': 0, 'WP\_048273893.1': 0,
'WP\_048284614.1': 0, 'WP\_047355585.1': 0, 'WP\_045882124.1': 0,
'WP\_045792035.1': 0, 'WP\_045269678.1': 0, 'WP\_044293428.1': 0,
'WP\_042560048.1': 0, 'WP\_042086213.1': 0, 'WP\_020928562.1': 0,
'WP\_004910271.1': 0, 'WP\_047414966.1': 0, 'WP\_047500028.1': 0,
'WP\_039340300.1': 0, 'WP\_037140816.1': 0, 'WP\_035225479.1': 0,
'WP\_024474547.1': 0, 'WP\_038409596.1': 0, 'WP\_036966456.1': 0,
'WP\_036959629.1': 0, 'WP\_036974156.1': 0, 'WP\_036977846.1': 0,
'WP\_036948496.1': 0, 'WP\_025416832.1': 0, 'WP\_025395172.1': 0,
'WP\_023533520.1': 0, 'WP\_022625635.1': 0, 'WP\_021491540.1': 0,
'WP\_019692735.1': 0, 'WP\_020431495.1': 0, 'WP\_016500007.1': 0,
'WP\_004637248.1': 0, 'WP\_004262799.1': 0, 'WP\_045902232.1': 0,
'WP\_060460871.1': 0, 'WP\_060442301.1': 0, 'WP\_060431700.1': 0,
'WP\_060455639.1': 0, 'WP\_060437608.1': 0, 'WP\_060432983.1': 0,
'WP\_060438709.1': 0, 'WP\_060418500.1': 0, 'WP\_050880653.1': 0,
'WP\_050918486.1': 0, 'WP\_050162987.1': 0, 'WP\_050158303.1': 0,
'WP\_050130984.1': 0, 'WP\_050160138.1': 0, 'WP\_050321664.1': 0,
'WP\_050322708.1': 0, 'WP\_050335261.1': 0, 'WP\_048324983.1': 0,
'WP\_047360713.1': 0, 'WP\_048233629.1': 0, 'WP\_039570340.1': 0,
'WP\_043179244.1': 0, 'WP\_034622813.1': 0, 'WP\_038448376.1': 0,
'WP\_025207685.1': 0, 'WP\_025328859.1': 0, 'WP\_016453823.1': 0,
'WP\_016453249.1': 0, 'WP\_013983315.1': 0, 'WP\_011946603.1': 0,
'WP\_034196516.1': 0, 'WP\_034188536.1': 0, 'WP\_034040414.1': 0,
'WP\_014475645.1': 0, 'WP\_020914447.1': 0, 'WP\_057099948.1': 0,
'WP\_057992932.1': 0, 'WP\_057037937.1': 0, 'WP\_039124095.1': 0,
'WP\_044780371.1': 0, 'WP\_050460055.1': 0, 'WP\_032071425.1': 0,
'WP\_031955431.1': 0, 'WP\_032017448.1': 0, 'WP\_032046023.1': 0,
'WP\_031972720.1': 0, 'WP\_031991294.1': 0, 'WP\_032019111.1': 0,
'WP\_032026533.1': 0, 'WP\_031950449.1': 0, 'WP\_032039758.1': 0,
'WP\_033853219.1': 0, 'WP\_032045193.1': 0, 'WP\_032034494.1': 0,
'WP\_032061328.1': 0, 'WP\_032070286.1': 0, 'WP\_032015622.1': 0,
'WP\_032037742.1': 0, 'WP\_032027613.1': 0, 'WP\_032009364.1': 0,
'WP\_042757256.1': 0, 'WP\_031636917.1': 0, 'WP\_034324889.1': 0,
'WP\_011860820.1': 0, 'AOH51342.1': 0, 'WP\_013279374.1': 0,
'WP\_063862740.1': 0, 'WP\_063862735.1': 0, 'WP\_063862730.1': 0,
'WP\_063862729.1': 0, 'WP\_063862728.1': 0, 'WP\_063862727.1': 0,
'WP\_063862726.1': 0, 'WP\_063862725.1': 0, 'WP\_063862724.1': 0,
'WP\_063862723.1': 0, 'WP\_063862722.1': 0, 'WP\_063862721.1': 0,
'WP\_063862719.1': 0, 'WP\_063862420.1': 0, 'WP\_063862718.1': 0,
'WP\_063862408.1': 0, 'WP\_063862402.1': 0, 'WP\_047023509.1': 0,
'WP\_057625895.1': 0, 'WP\_057631141.1': 0, 'WP\_057627739.1': 0,
'WP\_071447731.1': 0, 'EAB9198241.1': 0, 'WP\_063086404.1': 0,
'WP\_001439279.1': 0, 'WP\_001350795.1': 0}

Score on test data: 0.987116201732058

The overall accuracy score is the last number printed.

Finally, to run the model to predict your unknown proteins, use the
following command. Remember that AvsNotA\_UNKNOWN.csv is a feature table
file you generated in step 1.

\$ python trainWoolf.py -k CSVfolder/AvsNotA.csv -p
CSVfolder/AvsNotA\_UNKNOWN.csv

The results should look like this:

Building kNN Woolf Model...

Training Model...

\~\~\~\~\~\~ RESULTS \~\~\~\~\~\~

Score of best classifier: 0.832644774106317

Best Params:{'clf\_\_n\_neighbors': 1}

\~\~\~\~\~\~ \~\~\~\~\~\~

Predicting novel instances

{'WP\_050067789.1': 0, 'WP\_021577770.1': 0, 'WP\_023224609.1': 1,
'WP\_017442020.1': 1, 'WP\_001630205.1': 0, 'WP\_001631316.1': 1,
'WP\_002852433.1': 0, 'WP\_002856956.1': 0, 'WP\_000830775.1': 0,
'WP\_001317977.1': 0, 'WP\_001082962.1': 1, 'WP\_000830777.1': 0,
'WP\_000830773.1': 0, 'WP\_000059908.1': 0, 'WP\_057991827.1': 0,
'WP\_000673293.1': 0, 'WP\_002776717.1': 0, 'WP\_000817293.1': 0,
'WP\_001082975.1': 1, 'WP\_001208005.1': 1, 'WP\_023216810.1': 1,
'WP\_023993659.1': 0, 'WP\_001667037.1': 0, 'WP\_000673298.1': 0,
'WP\_001208011.1': 1, 'WP\_000673287.1': 0, 'WP\_001520983.1': 0,
'WP\_001082970.1': 1, 'WP\_002865991.1': 0, 'WP\_020899073.1': 0,
'WP\_000830757.1': 0, 'WP\_001327042.1': 0, 'WP\_020837858.1': 1,
'WP\_000188069.1': 0, 'WP\_001082979.1': 1, 'WP\_022645952.1': 0,
'WP\_001299057.1': 0, 'WP\_001931474.1': 1, 'WP\_023259161.1': 0,
'WP\_111742248.1': 1}

And that is it! You have built a Woolf Classifier that can predict if
novel $\beta$-lacamases are Type A or not Type A. Using the barcodes
provided in by the $- p$ option, you can further study these sequences
using any conventional experimental or computational technique.
