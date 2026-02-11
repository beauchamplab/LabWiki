---
layout: default
title: "DirectoryStructure"
parent: RAVE
---

# DirectoryStructure

|  |  |
| --- | --- |
| [RAVE logo](../../attachments/DirectoryStructure/RAVE_Logo_new.jpg "RAVE logo") | **R**eproducible **A**nalysis and **V**isualization of i**E**EG   ***RAVE*** |

|  |
| --- |
| RAVE Directory and File Structure RAVE uses a directory hierarchy to organize data. The top level of the hierarchy contains three directories. By default, they are named "raw\_dir", "data\_dir" and "other". These names and the locations of these directories can be changed using the rave::rave\_options() command. Raw data is placed into raw\_dir by the user, then RAVE pre-processes the data and places it into data\_dir. The "other" directory contains cortical surface models for visualizing the analyzed data and other ancillary files. The directory hierarchy has a specified structure. In iEEG studies, one subject may participate in many different experiments. For instance, the same subject could be asked to perform a working memory task and a language task. These files are collected close in time but must be analyzed differently. RAVE sorts raw data by subject (as data is collected participant by participant) but processed data is sorted by project/experiment, since analysis and manuscript preparation is typically performed on one experiment at a time, across participants. The raw data directory structure is the following (where XXX is the base of the data storage directory tree):   ```  XXX/raw_dir/subject_code/block_label ```   Where subject\_code refers to the individual subject and block\_number is a single data acquisition session. In the above example,   ``` XXX/raw_dir/subject_AAA/workingmemoryrun1 XXX/raw_dir/subject_AAA/workingmemoryrun2 XXX/raw_dir/subject_AAA/workingmemoryrun3 ```   Would contain data from three repetitions of a working memory task and   ``` XXX/raw_dir/subject_AAA/languagerun1 XXX/raw_dir/subject_AAA/languagerun2 XXX/raw_dir/subject_AAA/languagerun3 ```   Would contain data from three repetitions of a language task for the same participant. Each of these directories should contain one .mat file per channel   ```  subject_codeDatafileblock_label_chX.mat ```   where X is the electrode number. e.g. subject\_AAADatafileworkingmemoryrun1\_ch17.mat Within this file is a one row matrix named analogTraces with the voltage values over time. After preprocessing, data is placed into a new directory organized by project (experiment) followed by subject\_code. In the example, it could be:   ``` XXX/data_dir/working_memory_task/subject_AAA XXX/data_dir/language_task/subject_AAA ```   *Return to [Other Notes](index.md#Other_Notes "RAVE").* |
