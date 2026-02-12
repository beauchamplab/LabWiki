---
layout: default
title: "HowToScan"
parent: Beauchamp
---
# HowToScan


|  |  |
| --- | --- |
|  | Beauchamp Lab wiki |

- [Home](index.md "Beauchamp")
- [Publications](Publications.md "Beauchamp:Publications")
- [Resources](DataSharing.md "Beauchamp:DataSharing")

## How to Scan

For full details, see [CAMRI wiki on how to scan](../CAMRI/HowToScan.md)

Next step is [Getting raw data from the scanner](CreateAFNIBRIKfromMR.md "Beauchamp:CreateAFNIBRIKfromMR")

## Using the fORP

For Beauchamp Lab experiments, do the following:

1. Push in fORP front button
2. Go to changes modes, select YES
3. Select Autoconfigure
4. Scroll down to HID NAR BYGRT, Select
5. Confirm that Mode is 002 in top right of display

This gives a trigger as a T rather than a 5. An extra step needs to be taken to make sure that the right USB device is selected in Matlab (from the three possibilities).

## Accessing Pulse Sequences

To access pulse sequences, Click on Ctrl-Esc and select the "Advanced User" program. Type in the password (meduser1). Then go back, and open a Windows Explorer window. The pulse sequences are located under

```
C:/medcom/mricustomer/seq
```

The diffusion vectors are stored in the file

```
DiffusionVectors.txt
```

## Using Real-Time

If the real-time is not working, make sure you are using the correct pulse sequence (VB17rt EPI). Also check the tabs computer (MacPro):

1. Change user to admin\_local

```
$ su admin_local
```

2. Kill afni:

```
$ kill -9 'cat /Uses/tabs/tabs/var/afni.pid'
```

3. If that does not help reboot tabs
4. You can check the log on the scanner for hints:

```
Type logviewer from the command prompt.
```

More stuff on real-time:

1. Register subject, open Patient Database
2. Find subject, click on MP-RAGE first, "Send to TABS"
3. Once AFNI is up, then run rt fMRI sequence (look on "Special card")
