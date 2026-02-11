---
title: DownloadDataPenn
parent: Beauchamp
---
# DownloadDataPenn

|  |  |
| --- | --- |
|  | Beauchamp Lab wiki |

- [Home](index.md "Beauchamp")
- [Publications](Publications.md "Beauchamp:Publications")
- [Resources](DataSharing.md "Beauchamp:DataSharing")

# Download iEEG data from ieeg.org (UPENN data)

Once you've received confirmation (usually from Dhanya/Ashley) that data are available on the ieeg.org portal, you can download data with the DownloadFromiEEGorg.m script. The script is located on the server in the rave\_data directory. You need to connect to beauchamplab server to use this script. Here are the steps:

## Connect to MacPro

Connect to the server, in Terminal, type in:

```
 ssh beauchamplab@<server_IP>
```

When asked "Are you sure you want to continue?", Answer "yes"
When asked for the password, type in the beauchamplab password. Note that you won't see the password when typing.

If you see prompt: `(base) beauchamplab@beauchampsrv ~ % ` you are on the server now

If you get the error:

```
 ssh: Could not resolve hostname <server_IP>: nodename nor servname provided, or not known
```

You need to (re)connect to the Upenn VPN or try accessing the server from the campus network.

## Running the script

Navigate to script location and start headless matlab

```
 cd "/Volumes/PennRAID/Dropbox (PENN Neurotrauma)/BeauchampServe/rave_data"
```

```
 /Applications/MATLAB_R2020a.app/bin/matlab -nodesktop -nosplash
```

Start the downloading script in matlab in terminal, specifying the ProjectID and the runs (you must use double quotes " not ' when concatenating run names, else matlab creates a length 1 character array)

```
 DownloadFromiEEGorg ("HUP217_Cohort2", ["run1","run2","run3","run4","run5"])
```

The script attempts to download only non-zero data by querying the event annotations. If there are more than 2 events, the user will be asked which events are correct. e.g.:

```
 Found multiple events!
 (1) Mask run 1
 (2) Tech notation: Video/EEG monitoring taking place
 (3) mask task run 1 end
 Pick two events to use for data range(separated by comma):
```

Please pick accordingly, usually 1, and 3 (start and end of the run) to download. If there are only 2 events, you won't be prompted with this question.

Before downloading the data, the user confirms the size of the data:

```
 About to download 434.926758 seconds of data at 1024 Hz from 154 channels.
 Download the data? [Y]/n?
```

Raw data will be automatically downloaded to the rave\_raw directory, organized by subject and run name (/Volumes/OneDrive/data/rave\_data/raw/HUP211/run#). Confirmation of data download and photodiode detection are provided, followed by writing out the channel labels and detected sample rate to files in the subject's top-level directory.

```
 Writing out data to disk...done.
 Looking for photodiode on DC1...found. Downloading...done.
  Saving to photodiode.pd in /Volumes/OneDrive/data/rave_data/raw/HUP212/run1
 Writing out channel labels subject raw dir...done.
```

```
 Sample rate is: 1024. Writing to subject folder...done.
```

Note: If you requested more than one run, the script will effectively run once per run.

For the AV\_NoisyWords project, the naming is different (adding cohort):

```
 DownloadFromiEEGorg ("HUP217_Cohort2", ["run1","run2","run3","run4","run5"])
```

Repeat the other steps to confirm downloading. You have to answer the following 'Y' before each run to be downloaded:

```
   About to download ####### seconds of data at 1024 Hz from ### channels.
   Download the data? [Y]/n?
```

## Optional script parameters

You can change the ieeg.org user name, password file, and save location by specifying optional parameters:

```
 DownloadFromiEEGorg (subject, block, path_for_data, ieeg_user_name, path_to_pwd_file)
```

For example, if you want to save the raw data to the desktop:

```
 DownloadFromiEEGorg ("HUP211", ["run1","run2"],"/Users/beauchamplab/Desktop")
```

## Finishing up

To exit matlab, use the quit function

```
 >> quit()
 (base) beauchamplab@beauchampsrv rave_data %
```

To terminate the ssh connection:

```
 ctrl+d
```

Alternatively, you could simply close the terminal window.
