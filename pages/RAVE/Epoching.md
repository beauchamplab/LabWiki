> **Navigation:** [Home](index.md) | [Install](Install.md) | [Help](Help.md)

# Epoching

|  |  |
| --- | --- |
| [RAVE logo](../../attachments/Epoching/RAVE_Logo_new.jpg "RAVE logo") | **R**eproducible **A**nalysis and **V**isualization of i**E**EG   ***RAVE*** |

### Epoching Data

iEEG is recorded as a continuous time series, but many experiments consist of discrete trials or epochs. RAVE reads the experimental design information from the epoch file. This file is located within the **meta** folder, and must be supplied for every subject. Epoch files must start with the string "epoch\_", e.g., a file coding the onsets of a picture stimuli, called epoch\_picture\_onset.csv would be located in the directory tree as:

```
 rave_data_dir/proj_name/subj_name/rave/meta/epoch_picture_onset.csv
```

Here is the contents of a simple epoch file (commas in the file have been converted to tabs for ease of reading):

```
Block	Time	Trial	Condition
8	5.3475	1	cat_buster.jpg
8	9.3685	2	cat_pepper.jpg
8	13.337	3	cat_hulu.jpg
8	17.5915	4	cat_pepper.jpg
12	1.4185	5	cat_buster.jpg
12	17.639	6	cat_wookie.jpg
12	29.912	7	cat_dongdong.jpg
```

The **Block** column is the raw data file that this epoch occurred in. iEEG data is typically recorded in short sessions ("blocks") to allow the participant to rest in-between. In this example, data for this project in this subject was recorded in block #8 and block #12.

The **Time** is the number of seconds from the beginning of the current block in seconds (time is “local” to the block). In this example, there are two different blocks, and the time resets to zero at the beginning of each block (local time is used to prevent confusion about the origin of the "global" time that may have elapsed between different blocks). All analysis occurs relative to the time of trial onset.

The values in the **Trial** column must be different for each epoch. Values may be skipped, for instance, if an epoch is known to be an outlier and should not be analyzed ([outliers can also be discarded after analysis in Power Explorer](ravebuiltins_powerexplorer_input_managetrialoutliers.md "RAVE:ravebuiltins:powerexplorer:input managetrialoutliers")). Unlike time, the trial number is "global" to the experiment.

The **Condition** column is a string label for each trial. In this example, in trial 1, a picture of the cat named Buster was presented, while in trial 2, a picture of the cat named Pepper was presented. The labels are used during the analysis process, e.g. to view the millisecond-by-millisecond response of all presentations of Buster compared with the response to all presentations of Pepper.

It is possible to have multiple events in a single epoch. Here is an excerpt from a more complex epoch.csv file:

```
Block,Time,Trial,Condition,Event_1stWord,Event_2ndWord,Event_3rdWord,Event_4thWord,Event_5thWord
017,32.4925,1,Dynamic,33.2675,33.6685,34.1625,35.0265,35.3335
017,40.237,2,Static,40.706,41.336,41.69,42.286,42.614
017,47.381,3,Static,47.928,48.397,48.732,49.44,49.878
017,54.0585,4,Dynamic,54.7015,55.0195,55.3245,55.9135,56.3955
018,474.7775,139,Static,475.1445,475.5735,475.8875,476.6045,477.1375
018,481.0935,140,Static,481.5245,482.1905,482.6605,483.3755,483.9085
019,16.7925,141,Dynamic,17.1865,17.7705,18.3025,18.7935,19.3555
019,24.0045,142,Dynamic,24.5455,24.8805,25.3495,25.7515,26.1805
```

In this experiment, sentences were presented. The **Time** column records the time of the onset of each sentence, local to the block. The **Event\_** columns record the time of onset of the first word in the sentence, the second word in the sentence, and so on. These times are also local to the block (not to the trial onset). This allows analysis to be time-locked either to the onset of the trial (as in the simple example above) or to the occurrence of various events within the trial.
Additional columns can be added by the user but will be ignored by RAVE. If an event did not occur within a trial, an NA value can be entered (e.g. time\_of\_event1,NA,time\_of\_event3 ) or a null value can be entered (time\_of\_event1,,time\_of\_event3).

At the time of data loading, an epoch file must be specified, and this epoch file is used for all analyses. For instance, in the example above, an alternative solution would be to have two epoch files, epoch\_1stword.csv (containing the time of the onset of the first word in each sentence) and epoch\_2ndword.csv (containing the time of the onset of the second word in each sentence).

```
 proj_name/subj_name/rave/meta/epoch_1stword.csv 
 proj_name/subj_name/rave/meta/epoch_2ndword.csv
```

At the time of data loading, RAVE presents a list of all epoch files in the directory. The initial "epoch\_" and final ".csv" is stripped and only the remainder of the filename is shown in the pull-down list. Switching between epoch files requires reloading data and makes it more difficult to compare across sub-components of an epoch (e.g. in the above example, response to the first word vs. response to the second word). **When possible, it is preferable to create one epoch file with multiple event types.**

### Creating Epoch Files

A simple way to create epoch files is in a spreadsheet program, such as Microsoft Excel--just be sure to save as CSV format. The value in the Block column must correspond exactly to the name of the directory containing data for that block. If your folder name has leading zeros (e.g., the folders containing the data for blocks 1, 2, and 3 are labelled 001, 002, and 003), spreadsheet software may remove the leading zeros. To force Excel to save leading zeros, enter the values as text rather than numeric by pre-prending an apostrophe to the block number. For instance, type '001 [return] rather than 001 [return]. Then, in Excel, save the spreadsheet as a CSV file and copy it into the /rave/meta directory. The leading apostrophe will not appear in the CSV file.

In some cases, users may wish to create epoch files from analog recordings from a microphone or photodiode. RAVE has experimental tools to make this easier:

```
 rave::rave_preprocess(beta=TRUE)
```

Choose 'STEP. Trial Epoch'

In the GUI, create epoch files block by block (you need to click and save the epoch time series for each block individually). This can be selected under the tab 'Block'.
The GUI should be set up as follows:

Epoch Name -- New Epoch;

Block -- Choose each block (RAVE allows you to do one block per time);

Epoch File -- Choose the photodio file (e.g., photodiode.mat);

Variable name -- This should be the same as your electrode sampling rate (the default 30000 is for BCM site EMU data);

Plot range -- 0 (keep as default);

Threshold select -- (optional);

Minimal trial duration(s) -- (optional)

---

*[Return to preprocessing overview](ravepreprocess.md "RAVE:ravepreprocess")*
