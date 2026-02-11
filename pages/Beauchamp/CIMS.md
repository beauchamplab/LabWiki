# CIMS

> **Navigation:** [Home](index.md) • [Publications](Publications.md) • [Resources](DataSharing.md)

## Fitting the Causal Inference of Multisensory Speech Model to Data

### System setup

1. Install [GNU R](http://cran.cnr.berkeley.edu)
2. Download the [R code](../../attachments/CIMS/Cims_code_pack.zip "Cims code pack.zip") zip file
3. Extract the zip file to your Desktop/ or other preferred location

### Data setup

The model code assumes the data are stored in a matrix format with rows as subjects and each column a separate asynchrony. The first row is used as labels for the columns. Each cell stores the number of times the subject judged the stimulus at the given asynchrony as synchronous. If there are 17 subject and 15 asynchronies, the file will have 18 rows (1st row is header row) and 15 columns. For multi-condition experiments, place each asynchrony/condition combination in a separate column. Asynchronies within a condition must be contiguous. If the study has 4 conditions and 15 asynchronies, then the columns 1-15 will be treated as condition 1, 16-30 as condition 2, and so on. See *data.csv* in the code pack for the data used in Magnotti, Ma, & Beauchamp.

If you are unfamiliar with R, the best approach is to run through all the model building steps using the included data.csv file, and then try with your own data.

### Program setup

We need to ensure R can find the data and code files

1. Launch R

2. Open the file **fit\_models.R**: File-> Open Document

3. We need to make 4 changes before running the code. See the comments in the code file for additional direction

Set the path to be the location of the downloaded files. If you extracted the code pack to your desktop, the path may already be correct

```
  setwd('~/Desktop/cims_code_pack/')
```

Set the location of the data to be fit

```
  count_mat = as.matrix(read.csv(file='data.csv') )
```

Set the value of **max\_count** to be the total number of trials at each asynchrony for each condition.

```
  max_count = 12
```

Set the **asyncs** used in each condition. The order of the asynchronies must match the order in the data file. For multiple condition experiments, list the asynchronies only once.

```
  asyncs = c(-300, -267, -200, -133, -100, -67, 0, 67, 100, 133, 200, 267, 300, 400, 500)
```

4. Run the setup code to make sure there are no errors

1. Highlight lines 1 through 16 using the mouse
2. Execute the code by using the R menu: Edit -> Execute

### Fitting the model

Highlight and execute each of the following lines in turn

```` ```
  cl = makeCluster(detectCores())
``` ```````` ```
  # This takes about 15 seconds per repetition on a fast computer
  cims.model = cims(n.reps=512)
``` ```````` ```
  gauss.model = gauss(n.reps=512)
``` ````

### Model Parameters

1. The resulting parameters for each model are saved to **cims\_out.csv** and **gauss\_out.csv**.
2. The predicted values for each model are saved to **cims\_predicted.csv** and **gauss\_predicted.csv**.

### Model Comparisons

```
   # make sure these values correspond to the appropriate degrees of freedom for each model
   n.par.cims = 8
   n.par.gauss = 12
```

```
   #calculate the number of conditions
   n.conditions = ncol(count_mat) / length(asyncs)
```

```
   #calculate the BIC for each model using the separate=T function to get the log likelihood for each condition
   BIC.c = -2*logLik(cims.model, separate=T) + (log(max_count*ncol(count_mat)) * n.par.cims) / n.conditions
   BIC.g = -2*logLik(gauss.model, separate=T) + (log(max_count*ncol(count_mat)) * n.par.gauss) / n.conditions
```

## Advanced Functions

We mention here some other useful functions for those comfortable analyzing data with the R language. These functions assume you have run all the code in the previous section. Intrepid users are encouraged to let the source be their guide.

### Load previously fitted models

```` ```
  cims.model = load_cims_model('cims_out.csv')
  gauss.model = load_gauss_model('gauss_out.csv')
``` ````

### Obtain predicted values

```` ```
  cims.p = predict(cims.model)
  gauss.p = predict(gauss.model)
``` ````

### Plot model fits

```` ```
  #create proportion data from count data
  actual = count_mat / max_count
``` ```````` ```
  #create condition indicies
  c1 = 1:15
  c2 = 16:30
``` ```````` ```
  #plot conditions (see function in model_plotters.R for further plot customization)
  plotMeanWithFitted(asyncs, actual[,c1], cims.p[,c1], gauss.p[,c1])
  plotMeanWithFitted(asyncs, actual[,c2], cims.p[,c2], gauss.p[,c2])
``` ````

### Obtain model log likelihoods

```` ```
  cims.nlnL = -logLik(cims.model, separate=T)
  gauss.nlnL = -logLik(gauss.model, separate=T)
``` ````

*NB:* Remove the separate=T to return a logLikelihood object representing total log likelihood. Generic functions AIC and BIC will also work (e.g., AIC(cims.model) ) but be sure that the degrees of freedom reported by the function is appropriate for your model

```
  attr(logLik(cims.model), 'df')
```

## Contact Information

If you run into trouble with any step, please contact me: john dot magnotti at gmail dot com. If the model fitting fails to converge for your dataset, you may need to send me at least a portion of the data so I can replicate the error.

## Copyright/Licensing

<http://i.creativecommons.org/l/by-sa/3.0/88x31.png>

This work is licensed under a [Creative Commons Attribution-ShareAlike 3.0 Unported License](http://creativecommons.org/licenses/by-sa/3.0/).

If you find this code useful, please cite our work:

Magnotti JF, Ma W and Beauchamp MS (2013). Causal inference of asynchronous audiovisual speech. Front. Psychol. 4:798. doi: 10.3389/fpsyg.2013.00798
