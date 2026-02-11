---
title: NED
parent: Beauchamp
---
# NED

## Estimating amounts of McGurk Fusion across Stimuli

### System setup

1. Install [GNU R](http://cran.cnr.berkeley.edu)
2. Download the [McG Code Zip file](../../attachments/NED/Mcg_code_pack.zip)
3. Extract the zip file to your Desktop/ or other preferred location

### Data setup

The model code assumes the data are stored in a matrix format with rows as subjects and each column a separate stimulus. The first row is used as labels for the columns. Each cell stores the proportion of times the subject reported a fused perception for the given stimulus. If there are 20 subjects and 14 stimuli, the file will have 21 rows (1st row is header row) and 14 columns. See *data.csv* in the code pack for a sample of the data (full data available on request) used in Magnotti & Beauchamp.

If you are unfamiliar with R, the best approach is to run through all the model building steps using the included data.csv file, and then try with your own data.

### Program setup

We need to ensure R can find the data and code files

1. Launch R

2. Open the file **fit\_model.R**: File-> Open Document

3. We need to make 2 changes before running the code. See the comments in the code file for additional direction

Set the path to be the location of the downloaded files. If you extracted the code pack to your desktop, the path may already be correct

```
  setwd('~/Desktop/mcg_code_pack/')
```

Set the filename of the data to be fit. If you are using the example data, the filename is already correct

```
  mcg_data = read.csv(file='data.csv', row.names=NULL)
```

4. Run the setup code to make sure there are no errors

1. Highlight lines 1 through 9 using the mouse (click and drag to highlight)
2. Execute the code by using the R menu: Edit -> Execute

### Fitting the model

Highlight and execute each of the following lines in turn

```` ```
  cl = makeCluster(detectCores())
``` ```````` ```
   # Fit the model
   # For 20 subjects with 14 stimuli, this takes about 12s per repetition
   mcg_model = optim.mcg(mcg_data, n.sim=5, n.iter=8)
``` ````

### Model Parameters

You can obtain the model parameters for each subject using the getElement function applied to each subject

```` ```
   disparities = mcg_model$disparities
``` ```````` ```
   thresholds = clip(sapply(mcg_model$subjs, getElement, 'threshold'), range=THRESHOLD_RANGE)
``` ```````` ```
   noises = clip(sapply(mcg_model$subjs, getElement, 'sd'), range=SENSORY_NOISE_RANGE)
``` ````

### Model Fit Statistics

You can obtain the model fit (RMSE) for each subject using the getElement function applied to each subject

```` ```
   rmses = sapply(mcg_model$subjs, getElement, 'rmse')
``` ````

### Predicted Susceptibility Values

To obtain the actual and predicted fusion rates, use the predict function on each subejct

```` ```
   # mean illusion percept
   pF.mean = colMeans(sapply(mcg_model$subjs, getElement, 'y'))
``` ```````` ```
   #mean predicted percept
   fitted = t(sapply(mcg_model$subjs, predict, disparities))
   pF.mean.pred = rowMeans(fitted)
``` ````

### Save model output to a csv file

You can save all the model results to a csv file for further processing/graphing

```` ```
   write.csv(cbind(noises, thresholds, rmse, pF.mean, pF.mean.hat), file='model_results.csv')
``` ````

## Advanced Functions

We mention here some other useful functions for those comfortable analyzing data with the R language. These functions assume you have run all the code in the previous section. Intrepid users are encouraged to let the source be their guide.

### Load previously fitted models

If you have previously saved a model fit with save(...) you can load the model using load(...)
`load(file='mcg_model.RDATA')`
Once loaded, the variable will be in the current scope. Note that there is no explicit assignment with the load() function

## Contact Information

If you run into trouble with any step, please contact me: john dot magnotti at gmail dot com. If the model fitting fails to converge for your dataset, you may need to send me at least a portion of the data so I can replicate the error.

## Copyright/Licensing

<http://i.creativecommons.org/l/by-sa/3.0/88x31.png>

This work is licensed under a [Creative Commons Attribution-ShareAlike 3.0 Unported License](http://creativecommons.org/licenses/by-sa/3.0/).

If you find this code useful, please cite our work:

Magnotti JF and Beauchamp MS (in press). The noisy encoding of disparity model of the McGurk effect. Psychonomic Bulletin & Review.
