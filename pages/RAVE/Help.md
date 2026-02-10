> **Navigation:** [Home](index.md) | [Install](Install.md) | [Help](Help.md)

# Help

|  |  |
| --- | --- |
| [RAVE logo](../../attachments/Help/RAVE_Logo_new.jpg "RAVE logo") | **R**eproducible **A**nalysis and **V**isualization of i**E**EG   ***RAVE*** |

## Sharing Data

RAVE allows you to export an HTML file (viewable in any web browser) that can be shared with other scientists or uploaded to journals or an archive. The file combines a viewer with subject data, allowing users to interactively explore the dataset, facilitating replication, reliability, and new discoveries.
Just click on the download arrow in the 3D Viewer (red circle below) and the HTML file will be downloaded to your computer, and can then be distributed.

[![3D Viewer Download Button](../../attachments/Help/RAVE_Download_Button.jpg)](../../attachments/Help/RAVE_Download_Button.jpg "3D Viewer Download Button")

[Click here to download a sample exported HTML file.](../../attachments/Help/Share.zip "Share.zip") After downloading, find the file, double-click once to unzip, and then double-click again on the unzipped file to open in your default browser.

## Typical workflow

RAVE's file locations (directories for Raw and Processed data) can be set/viewed using RAVE options (type into the RStudio console):

```
   rave::rave_options()
```

If you are not using the included sample data, preprocess your own data (includes electrode localization): [Preprocessing](ravepreprocess.md "RAVE:ravepreprocess").

Analysis of data usually begins with single-subject analysis in the [Power Explorer module](Tutorial_PowerExplorer.md "RAVE:Tutorial PowerExplorer").

Analysis continues with the [Group Analysis module](ravebuiltins_linearmixedeffectmodel.md "RAVE:ravebuiltins:linearmixedeffectmodel").

For data exploration of single-subjects or groups: [Electrodes Clustering module](raveclusters.md "RAVE:raveclusters").

For real-time analysis of iEEG data in the EMU: [Real-time RAVE](realtime.md "RAVE:realtime").

To use the 3dViewer on your own spreadsheets, make use of the [Surface+Volume Viewer](ravebuiltins_surfaceandvolumeviewer.md "RAVE:ravebuiltins:surfaceandvolumeviewer").

For general GUI information, see [Introduction to the Rave Toolbar](ravebuiltins_toolbar.md "RAVE:ravebuiltins:toolbar").

Clicking on the help icon ("?") in any RAVE menu opens a help page. Help is also searchable *e.g.* search **outlier in the local wiki pages** to find help on outliers.

## RAVE Workshops

[2021 Computational Memory Lab's Workshop on Cognitive Electrophysiology](CML_Workshop_2021.md "RAVE:CML Workshop 2021")

[Suthana lab YAEL tutorial, June 2023](SuthanaDemo_2023.md "RAVE:SuthanaDemo 2023")

## Tips and Tricks

1. In the Power Explorer 3D Viewer, it can be handy to display only a subset of electrodes. Open the "Controls" panel and the "Data Visualization" subpanel. Change "Threshold Data" selector to "Selected\_Electrodes". Electrodes can be selected by clicking them on them (selects one electrode at a time) or entering an electrode range in the "Select Electrodes" panel in the Power Explorer menu. To hide the other electrodes, open the "Electrodes" subpanel in 3D Viewer and change the Visibility selector to "hide inactives" (the shortcut for this is "v"). The "d" shortcut in 3D Viewer cycles through different data.
2. In the Power Explorer 3D Viewer, it can be handy to display a number of electrodes on a single MRI slices. Select "Show Panels" under "Volume Settings" and increase the "Dist. Threshold" slider to the desired value, e.g 10 mm. This will display all electrodes within 10 mm of the selected slice.
3. Avoid parentheses in Group names in the "Create condition contrasts" panel in power explorer.

## Troubleshooting

Personalized support is provided via our Slack workspace *rave-brain.slack.com*. E-mail slack@rave.wiki for an invitation to the support channel.

**Full Disks** One problem that can lead to performance issues or difficult-to-diagnose symptoms is if your primary storage device is full or nearly full. This can generate errors that are not obviously due to low disk space, such as this one:

```
Warning in mccollect(jobs = jobs, wait = TRUE) :
 1 parallel job did not deliver a result
x Failed to retrieve the result of MulticoreFuture (<none>) from the forked worker
```

In the event of errors like this, the first step should be to check the amount of free disk space (on Mac, click on the icon for "Macintosh HD" and type Apple-I to show the amount of free disk space.) iEEG data is very large and can easily fill up even large file systems. During processing, RAVE creates large cache files to improve performance, but these cache files can fill disks. Cache files can be manually deleted from the cache directory. Check or set the cache directory with rave::rave\_options(). A common location would be

```
 ~/rave_data/cache_dir
```

This directory should be placed on a disk with fast read and write access, and does not need to be backed up. To free up space, it is OK to delete any cache files that may have accumulated. The cache directory can also be changed to a disk with more free space, such as a RAID.

**Browser disconnected from server**. Another common issue is that the RAVE GUI in the browser window appears dim or grayed out. This indicates that the browser has become disconnected from the RAVE server (e.g. if the computer has gone to sleep mode and then woken up). To reconnect to the RAVE server, try refreshing the browser window (right-click and select "reload" or highlight the URL the browser address bar and press enter). If this does not work, then follow the instructions for shutting down the RAVE server, then relaunch.
