> **Navigation:** [Home](index.md) • [Install](Install.md) • [Help](Help.md)

# Tutorial Importing

|  |  |
| --- | --- |
| [RAVE logo](../../attachments/Tutorial_Importing/RAVE_Logo_new.jpg "RAVE logo") | **R**eproducible **A**nalysis and **V**isualization of i**E**EG   ***RAVE*** |

# Import and Preprocess Raw Data Tutorial

To begin, launch the RAVE Preprocessing Module from R or RStudio with the following command:

```
 ravedash::start_session(new = TRUE)
```

The Preprocessing Module will launch in a browser window or tab, if the browser is already opened. The initial page should be the Overview page. If not, select “Overview” from the black panel list at left.

The Overview page has two sections, called panels, that contain text boxes, droplists, or checkboxes with which the files and settings for the current RAVE session are selected, or data calculated from the current panel entries. All panels have a header with the panel’s name and a minimize icon (a minus sign, “-”) that will hide the panel without altering the data therein. There may also be a help icon (a question mark, “?”), a refresh icon (a pair of circled arrows), or an expand icon (a segmented box). Those will be covered as they appear.

Look first at the left panel. The panel is organized into Steps for loading a subject’s data for preprocessing. Step 1 is the subject code. This is the name of the folder in which the subject’s raw data, in the form of .h5 files from an iEEG recording, are stored. In the Beauchamp lab, we use a three-letter subject code such as YAB or YAD. The demo data set includes these subjects as well as one named “demo.”

Step 2 is to select a project folder in which to store the subject data. The project folders are stored in the RAVE directory; each project will have a folder for each subject included, and a subject can be included in any number of projects. To create a new project here, select “new…” from the drop-down menu labeled “Project.” A text box will appear in the Step 2 section. Enter the desired name of the project here and click “Create” to make that folder in the RAVE directory. From this point on, this project folder can be selected from the “Project” droplist.

Step 3 is to select the data that will be loaded for preprocessing. RAVE uses iEEG data stored in numerically-identified recording sessions, henceforth referred to as “blocks,” named with a zero-padded integer according to the order in which they were recorded. Select the subject’s recording blocks associated with the set project from the uppermost droplist in this section. In the text box below, enter the range of electrodes to be loaded. It is recommended to run the preprocessing steps on all electrodes at once (i.e., the range entered should be “1-max” up to the largest electrode value of the subject’s recording). The lowermost textbox sets the sample rate at which the preprocessing will be run. This should be identical to the sample rate of the iEEG recording equipment.

Look now at the right panel. This panel displays the current entries of the left panel for review. At the bottom it displays a log of events that occur to the currently-selected dataset.

Click the “Load Subject” button to set the current selection and begin preprocessing.

IMPORTANT NOTE: Currently, all blocks for a subject must be preprocessed at once. This is to make sure that all blocks have the same number of electrodes and sampling rate. If additional blocks need to be added later, a second subject must be created (e.g. YDJ2) and preprocessed. If the same parameters are used, the two subjects (e.g. YDJ and YDJ2) can then be merged.
