# CIMS McGurk

> **Navigation:** [Home](index.md) • [Publications](Publications.md) • [Resources](DataSharing.md)

## A Causal Inference Model for the McGurk Effect

### View the stimuli

1. Example stimuli can be view on the [CI Stimuli page](McGurk_CI_Stimuli_McGurk.md)

### System setup

1. Install [GNU R](http://cran.cnr.berkeley.edu)
2. Download the  [Code File and Data](../../attachments/CIMS_McGurk/Cims_mcg_code_pack.zip "Cims mcg code pack.zip")
3. Extract the zip file to your Desktop/ or other preferred location

### Program Information

We need to ensure R can find the data and code files

1. The main file is *mcgurk\_causal\_inference.R*

2. Set the path to be the location of the downloaded files. If you extracted the code pack to your desktop, the path may already be correct

```
  setwd('~/Desktop/cims_mcg_code_pack/')
```

3. Run the code as needed to reproduce the graphs

4. Changing values in *mcgurk\_causal\_inference\_constants.R* will change model predictions

5. There is a code file in the data/ folder that analyzes the behavioral data.

## Contact Information

If you run into trouble with any step, please contact me: john dot magnotti at gmail dot com.

## Copyright/Licensing

<http://i.creativecommons.org/l/by-sa/3.0/88x31.png>

This work is licensed under a [Creative Commons Attribution-ShareAlike 3.0 Unported License](http://creativecommons.org/licenses/by-sa/3.0/).

If you find this code useful, please cite our work:

Magnotti JF and Beauchamp MS (in press). Causal Inference Explains Perception of the McGurk Effect and Other Incongruent Audiovisual Speech. *PLOS Computational Biology*

<http://crossmark.crossref.org/dialog/?doi=10.1371/journal.pcbi.1005229>
