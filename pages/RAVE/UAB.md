---
title: UAB
parent: RAVE
---
# UAB

|  |  |
| --- | --- |
| [RAVE logo](../../attachments/UAB/RAVE_Logo_new.jpg "RAVE logo") | **R**eproducible **A**nalysis and **V**isualization of i**E**EG   ***RAVE*** |

## How to use RAVE on the UAB Cheaha Cluster

### First time only (installs RAVE for an account)

1. Establish Cheaha account with Office of Research Computing. Be sure to request a 16 gb RAM HPC desktop
2. Open Terminal to Cheaha

type

```
 module load FriBidi/1.0.10-GCCcore-10.3.0
 module load HarfBuzz/2.8.1-GCCcore-10.3.0
 module load R/4.1.0-foss-2021a
```

type

```
 R
```

to start R. Then,

```
 install.packages('ravemanager', repos = 'https://beauchamplab.r-universe.dev')
 ravemanager::install()
```

### To use RAVE (after installation)

```
 module load R/4.1.0-foss-2021a
 R
```

Then, start RAVE within R using the commands

```
 rave::start_rave()
```

or

```
 rave::launch_demo()
```

This may launch a "graphics device". This can be safely minimized.
For analysis of large datasets, you may need to request additional resources. To check on resource usage, type

```
 seff <jobid>
```

where <jobid> found on My Interactive sessions
or

```
 sacct -u <blazerid> -X
```

### Set your data directory to point toward shared data

After you have loaded RAVE under your personal account, you may need to set your RAVE data dir and raw dir to point to data stored in a shared project directory.

To view your data dir, run in the R console:

```
   raveio::raveio_getopt('data_dir')
```

To set your data dir:

```
   rave_options(data_dir = 'path/to/shared_data_dir')
```

To view/set your raw data dir:

```
   raveio::raveio_getopt('raw_data_dir')
   rave_options(raw_data_dir = 'path/to/shared_raw_data_dir')
```
