# ECogAnalysis

> **Navigation:** [Home](index.md) | [Publications](Publications.md) | [Resources](DataSharing.md)

## eCog Processing Notes

by Adam Burch, July 2010

## Processing Data from Ping Sun

Please note, all work with the ECoG data will be done in MATLAB. First, get the data files from Ping.
Yoshor data files are stored using the patient's initials e.g. JP, followed by the datafile #. The datafiles are ordered sequentially as they are collected, and notes about each file are in Ping's lab notebook Microsoft Word document.
Beauchamp Lab stores the data with an anonymized letter code. The correspondence between them is in the ExperimentSummary spreadsheet.
There is one data file per channel, which will be entitled fileName\_ch#.mat (e.g. "JPDatafile006\_ch15.mat", where JPDatafile006 is fileName and 15 is the channel number in question). In addition, a time stamp file is needed, named fileName\_timeStamp.mat (e.g. JPDatafile006\_timeStamp.mat). These files should be uploaded into the correct directory on the server
e.g. for JP, they are in

```
 /Volumes/data1/UT/HJ/HJ_rawdata
```

Once these files are uploaded to the server, one must create a setting file in MATLAB called OBJSettingForAll\_new.mat. This is done by the generateOBJSetting\_new.m. This setting file will encode the information particular to that subject's experiment. Of particular importance to edit is the list of channel names (S.chanDesList), as this changes for every patient. For example, for JPDatafile006, the channel list is:

`S.chanDesList = {'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'g13', 'G14', 'G15', 'G16', 'G17', 'G18', 'G19', 'G20', 'G21', 'G22', 'G23', 'G24', 'G25', 'G26', 'G27', 'G28', 'G29', 'G30', 'g31', 'G32', 'AF1', 'AF2', 'AF3', 'AF4', 'AIT1', 'AIT2', 'AIT3', 'AIT4', 'MIT1', 'MIT2', 'MIT3', 'MIT4', 'PIT1', 'PIT2', 'PIT3', 'PIT4', 'SPLT1', 'SPLT2', 'SPLT3', 'SPLT4', 'SPLT5', 'SPLT6', 'IPLT1', 'IPLT2', 'IPLT3', 'IPLT4', 'IPLT5', 'IPLT6', 'IPLT7', 'IPLT8', 'EKG1', 'EKG2'};`

As long as the same experiment is being done and the equipment doesn't change, nothing else should need to be edited. If it were to change, examine items such as S.images, S.imageNames, S.sampleHZ, etc. Additional comments can be found in the code itself.
The version used to process each subject is found in that subject's directory.
The most up-to-date version (as of August 7th) is in

```
 /Volumes/data1/UT/AdamsMatlabCode
```

## Processing Data from Ping Sun

A function should be written to do all of the below commands with a single function.

## Gamma Band Response

The Gamma Band Response (GBR) measures activity in the gamma band of oscillations. This method is modeled after the method Lachaux's group uses. The GBR can then be treated as an LFP. To calculate the GBR, power spectral analysis is performed on the LFP data using a multitaper frequency transformation on each trial using frequency bins of 2 Hz from 30 to 150 Hz and a time window of 10 ms. A baseline level is computed by averaging the power spectra across frequencies and then taking the median across the pre-stimulus time, retaining different values for each trial. A test level is computed similarly at each time point in the series, and then these two groups are compared using the Wilcoxon rank-sum Z-test. To complete all this analysis:

1. Organize the LFP data. This is done by doLFPvoltage.m
2. Calculate the Power Spectra. This is done by doPowerSpectra.m
3. Calculate the Gamma Band Response. This is done by doGBR.m
4. In addition, we calculate z-scores for the LFP data to make them more comparable.

### doLFPvoltage

To analyze the data, the first step is to organize the raw analog traces into a structure relating to the trial number. This is done by the function doLFPvoltage.m. To run analysis on all channels and save the data:

Find the directory you wish to save the data in. The best way to do this is to create a new folder for each type of data with the filename (e.g. JPDatafile006 LFPvoltage). Make this the current directory in MATLAB.
Type the following into the MATLAB command window:

`for c = 1:<number of channels>   
 doLFPvoltage('<fileName>', c, 'none', 1);   
 c   
 end`

This can take many minutes, depending on the number of channels. After it has gone through all channels, be sure to update the MATLAB path so that these files are accessible to other functions as the analysis continues.

### doPowerSpectra

The next step of the analysis is to calculate Power Spectra. This is done by doPowerSpectra.m. To run Power Analysis and save the data:

Find the directory you wish to save the data in. The best way to do this is to create a new folder for each type of data with the filename (e.g. JPDatafile006 Power Spectra). Make this the current directory in MATLAB.
Type the following into the MATLAB command window:

`for c = 1:<number of channels>   
 doPowerSpectra('<fileName>', c, 'none', 1);   
 c   
 end`

This loop will take roughly 2-4 minutes per channel, making this the longest step by far of the analysis. After it has gone through all channels, be sure to update the MATLAB path so that these files are accessible to other functions as the analysis continues.

### doGBR

The final step of the analysis is to calculate the GBR. The GBR can be calculated by category (audio only, AV congruent, AV incongruent, video only) or by image (drive V-only, drive AVcongruent, etc...). In addition, a simple method of computing the Gamma Band power by trial is included in doGBR. This method compares the percentage of power at each time point to the baseline, and reports it as a percent change. Because of this, we must create three directories for each set of data and run a for loop three times. To fully complete the analysis, calculate all GBRs, and save the data:

Find the directory you wish to save the data in. The best way to do this is to create a new folder for each type of data with the filename (e.g. JPDatafile006 GBR Category). Make this the current directory in MATLAB.
Type the following into the MATLAB command window:

`for c = 1:<number of channels>   
 doGBR('<fileName>', c, 'category', 1, 0);   
 c   
 end`

This will take roughly 20-30 seconds per channel. After the for loop is complete, create another directory and run the for loop again, changing 'category' to 'image' and then to 'trial'. In total, doGBR will be run 3 times per channel.

After it has gone through all channels, be sure to update the MATLAB path so that these files are accessible to other functions as the analysis continues.

This can be automated to run the analysis as follows:
analysistype = {'cat',*}*
mkdir analysistype{1}
'category' = analysistype{1}

### doLFPwilcoxon

This step is not necessary to the others, and only requires doLFPvoltage to have been completed. The LFP z-scores can be calculated by category or image. If it is called with trial data, a z-score cannot be computed because there is only one data point and Wilcoxon requires medians. Instead, for trial data, each time point is given a value equal to its percentage of maximum. To calculate the LFP z-scores:

Find the directory you wish to save the data in. The best way to do this is to create a new folder for each type of data with the filename (e.g. JPDatafile006 LFPwilcoxon Category). Make this the current directory in MATLAB.
Type the following into the MATLAB command window:

`for c = 1:<number of channels>   
 doLFPwilcoxon('<fileName>', c, 'category', 1, 0);   
 c   
 end`

This will take roughly 20-30 seconds per channel. After the for loop is complete, create another directory and run the for loop again, changing 'category' to 'image' and then to 'trial'. In total, doGBR will be run 3 times per channel.

After it has gone through all channels, be sure to update the MATLAB path so that these files are accessible to other functions as the analysis continues.

## Broadband Power

The broadband power is similar to the GBR in that it calculates the power in the gamma band of oscillations. The method for its calculation is more complex. The LFP data is bandpass filtered from 30 to 150 Hz, and the Hilbert transform is then taken. A standard z-score is taken of the logarithm of the Hilbert transform. This data is then smoothed by convolution. The z-score is taken again and then re-exponentiated to obtain the final result. This method was created by Kai J Miller. To complete this analysis, use a function called doKJManalysis.m.

### doKJManalysis

To calculate the broadband power for all channels:

Find the directory you wish to save the data in. The best way to do this is to create a new folder for each type of data with the filename (e.g. JPDatafile006 BB power). Make this the current directory in MATLAB.
Type the following into the MATLAB command window:

`for c = 1:<number of channels>   
 doKJManalysis('<fileName>', c, 'none', 1);   
 c   
 end`

This will take around 2-4 minutes per channel. However, unlike the GBR calculation, this is all one step. Be sure to update the MATLAB path after all files are completed. The results may be viewed with the "BBpower" option below.

## Viewing Plots

Each function mentioned above can also be used to plot the data as it is calculated. In order to be more convenient however, one function called plotECOG.m can plot all types of ECoG data.
The format for the function is plotECOG(fileName, chan, dataType, plotType); This function makes plots from previously calculated ECOG data. fileName refers to the file prefix (e.g. JPDatafile006). chan is the channel number to be plotted. dataType can be 'LFPvoltage', 'PowerSpectra', 'GBR', 'BBpower', or 'LFPwilcoxon'. plotType can be 'category', 'image', or 'trial'. Not all plotTypes can apply to each dataType.
Sample command lines.
For instance, the plot the GBR response from all AVincongruent trials for ch 22, type

```
 plotECOG('JPDatafile006', 22, 'GBR', 'category');
```

## Other Functions

PlotAllComparisons - This function compares BB power, GBR, and LFP for AVc and AVi for a particular channel electrode.

PlotDifferences
This would be a good program to plot the DIFFERENCE between two stimuli type in a specific electrode.
