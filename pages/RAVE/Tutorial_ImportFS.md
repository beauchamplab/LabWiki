---
title: Tutorial ImportFS
parent: RAVE
---
# Tutorial ImportFS

|  |  |
| --- | --- |
| [RAVE logo](../../attachments/Tutorial_ImportFS/RAVE_Logo_new.jpg "RAVE logo") | **R**eproducible **A**nalysis and **V**isualization of i**E**EG   ***RAVE*** |

## Import FreeSurfer Data Tutorial

RAVE’s 3D Viewer is fully compatible with FreeSurfer and all surface files from the full surface reconstruction process. This tutorial assumes that the reconstruction process is complete and the local gyrification index (LGI) has been calculated. All files from this process are stored in a standard FreeSurfer directory, set up upon installation of the software, and organized by subject. For detailed instructions on reconstructing a patient’s brain in 3D space with FreeSurfer, [click here for the FreeSurfer Wiki.](https://surfer.nmr.mgh.harvard.edu/fswiki)
First, open the current subject’s folder in your computer’s FreeSurfer directory. There will be a number of folders listed here; RAVE only requires three to display a subject’s data: ./label, ./mri, and ./surf. Copy these folders and the files therein.

Next, open the current subject’s folder in the current project of the RAVE directory. There will be two folders here: ./fs and /rave. If there is no /fs folder, create one now. Copy the three FreeSurfer folders into the /fs folder.

To display electrodes on or within the subject’s brain, enter the subject’s /rave/meta folder and select the file “electrodes.csv”. This file lists all electrodes processed in the Preprocessing Module ans their coordinates. Electrodes with the coordinates (0,0,0) will not be displayed, Enter the coordinates of each electrode and save the file. Upon next loading, RAVE will display these electrodes along with the surface files from the FreeSurfer folder.

Now launch RAVE through RStudio with the command:

```
>rave::start_rave()
```

At the top bar, there are three options: Modules, Input Panels, and Select Data. Click the “Select Data” option to launch a pop-up panel to load a subject’s information.
This panel is divided into five subsections. Look first at the top-right section, “Project/Subject.” There are two droplists; on the right, select the current project, and on the left, select the current subject’s identifier. If in this session the Group Analysis Module will be used, check the box “Load for group analysis.” If not, this box can be left blank to reduce load times.

The next subjection is “Epoch Selection.” Select an epoch file from the droplist at left. If the desired epoch file is not displayed in this list, check the file’s name in the subject’s /rave/meta folder. Epoch files must be named “epoch\_filename.csv” for RAVE to recognize them in the Select Data panel. If the file name is correct but the file still does not appear in the droplist, try refreshing the browser page. With an epoch file selected, look to the two textboxes to the right, “Pre” and “Post.” In the first textbox, enter the number of seconds before the event start listed in the epoch file to be loaded. This value can be an integer or a decimal, but not a fraction. In the second textbox, enter the number of seconds after the event start to be loaded. Be sure to load enough time before each event to account for a baseline period and enough time after to cover all potential responses. At the bottom of this section, a line of text will appear describing the number of trials in the epoch file, the number of condition types therein, and the total time loaded for each event.

Now look at the “Electrode and Reference” section. If this is the first time loading this subject, select “default” from the Reference Table droplist and enter the full range of electrodes (1-max) in the Electrodes textbox. A mask file can be loaded as well but is not necessary. If this subject has already been referenced, select the exported reference from the Reference Table droplist. All electrodes or any subset thereof can be loaded, though for the initial processing it is recommended to load and reference all electrodes. There will be a line of text at the bottom of this section stating the number of electrodes loaded.

The “Load Estimation” section automatically updates with details of the current selection. This section approximates the size of the voltage, phase, and power data to be loaded in MB or GB and the required memory resources to load them. At the very bottom, it estimates the loading time for each data type based on the amount of memory and CPU cores available to the current RAVE section. Resources can be reallocated in the rave\_options menu.

The final and largest subsection is the “3D Viewer” section. If there’s no need to display this subject’s surface files in any part of the current RAVE session, uncheck the “Load Mesh” box at the top right. Otherwise leave the box checked. The first time a subject’s FreeSurfer data is loaded, RAVE automatically converts the needed surface files to ASCII format and stores them in a new folder. This one-time process adds several seconds to the initial load time, but allows faster loading for all future sessions including this subject. This panel also serves as a miniature version of RAVE’s 3D Viewer; the brain surface that loads is a full 3D object that can be rotated and adjusted as needed. If there are electrode coordinates in the file “electrodes.csv”, these will be displayed as well; click on an electrode to see details such as its coordinates, label, and current loading status. Keyboard shortcuts for the 3D Viewer will work within this panel. For a list of these, click here.

When the desired subject, epoch, and reference are set, click “> Load Data” at the bottom-left corner of the panel to begin the loading process. A small notification will appear in the lower left corner of the browser page with RAVE’s current function and loading bars for the current information.
