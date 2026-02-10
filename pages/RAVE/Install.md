> **Navigation:** [Home](index.md) | [Install](Install.md) | [Help](Help.md)

# Install

|  |  |
| --- | --- |
| [RAVE logo](../../attachments/Install/RAVE_Logo_new.jpg "RAVE logo") | **R**eproducible **A**nalysis and **V**isualization of i**E**EG   ***RAVE*** |

Thank you for visiting the RAVE wiki Install instructions, for the current version, visit:

### [New RAVE installation instructions](https://rave.wiki/posts/installation/installation.html)

[Click here for notes on editing the new website](https://rave.wiki/posts/editor-notes/how-to-edit-this-website.html)

## Step 1: Install prerequisites

**[Before doing anything else, click here to install the prerequisites.](Install_prerequisites.md "RAVE:Install prerequisites")**

❗The most common installation problem is that the prerequisites are not installed.❗

## Step 2: Install RAVE for the First Time

If you have installed RAVE before, please check [How to update RAVE](Update.md "RAVE:Update").

1. Open the "R" application if it is not already open ("RStudio" may also be used). Copy and paste the following command into the "R" (or "RStudio") console:

```
 install.packages('ravemanager', repos = 'https://rave-ieeg.r-universe.dev')
```

2. Copy and paste the following command into the "R" console:

```
 ravemanager::install()
```

Wait until you see the "Done finalizing installations!" message and the R Console command prompt reappears. This may take a few minutes depending on the speed of your internet connection. After installation, it is recommended to close all instances of "R" and restart "R".

Common installation problems:

* The following packages are found that cannot be unloaded...

Some processes are still using RAVE scripts. Please make sure all R and RStudio windows are closed. Close them, re-open, and retry the installation.

---

* [ravemanager] The installer's major version has been updated (from xxx -> xxx)...

Please make sure all R and RStudio windows are closed. Close them, re-open, and retry the installation.

---

* Your R version (xxx) is too low....

R major version is too low, return to [install the prerequisites.](Install_prerequisites.md "RAVE:Install prerequisites")

---

## Step 3: Launch RAVE

Copy and paste the following command into the "R" console:

```
   rave::start_rave2()
```

In a few seconds a web browser window showing RAVE should appear. Success!
Explore RAVE by clicking on one of the module names on the left-hand side such as "Subject 3D Viewer" to view a brain or "Power Explorer" to view sample iEEG data.

## Step 4 (optional): Guided Analysis Demo

Copy and paste the following command into the "R" console:

```
   rave::launch_demo()
```

Follow along with the Demo Video here

Load videoYouTubeYouTube might collect personal data. [Privacy Policy](https://www.youtube.com/howyoutubeworks/user-settings/privacy/)

Continue
Dismiss

## Step 5 (optional but recommended): Install Isolated Python Environment

Copy and paste the following command into the "R" console:

```
   ravemanager::configure_python()
```

Some advanced RAVE features (such as CT to MRI alignment via nipy or ants) call Python libraries. To prevent conflicts with existing Python installations and ensure stability and reliability, this step uses miniconda to install an isolated Python environment and useful Python packages (numpy, scipy, jupyterlab, mne, nipy, pynwb, ants).

## Other Methods To Install RAVE

[Other methods for installing RAVE.](Install_deprecated.md "RAVE:Install deprecated")
