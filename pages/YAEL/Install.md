---
layout: default
title: "Install"
parent: YAEL
---
# Install


|  |  |
| --- | --- |
| [RAVE logo](../../attachments/RAVE/RAVE_Logo_new.jpg) | **Y**our **A**dvanced **E**lectrode **L**ocalizer   ***YAEL*** |

- [Home](index.md "YAEL")
- Install
- [Update](Update.md "YAEL:Update")
- [Launching](Launching.md "YAEL:Launching")
- [Tutorials and Help](Help.md "YAEL:Help")
- [Community](Community.md "YAEL:Community")

## Step 0: Do I need to install YAEL at all?

For more efficient software maintenance, [RAVE](../RAVE/index.md "RAVE") and YAEL are installed together because they share common elements. If you have already installed [RAVE](../RAVE/index.md "RAVE"), you do not need to install YAEL separately.

## Step 1: Install prerequisites

Click on this link to **[install the prerequisites.](Install_prerequisites.html)**

> ❗The most common installation problem is that the prerequisites are not installed.

## Step 2: Install YAEL for the First Time

If you have installed YAEL (or RAVE) before, please check [How to update YAEL](Update.md "YAEL:Update").

1. Open the "R" application if it is not already open ("RStudio" may also be used). Copy and paste the following command into the "R" (or "RStudio") console:

```
 install.packages('ravemanager', repos = 'https://rave-ieeg.r-universe.dev')
```

2. Copy and paste the following command into the "R" console:

```
 ravemanager::install(python = TRUE)
```

Wait until you see the "Done finalizing installations!" message and the R Console command prompt reappears. This may take a few minutes depending on the speed of your internet connection. After installation, it is recommended to close all instances of "R" and restart "R".

Common installation problems:

- The following packages are found that cannot be unloaded...

Some processes are still using YAEL scripts. Please make sure all R and RStudio windows are closed. Close them, re-open, and retry the installation.

---

- [ravemanager] The installer's major version has been updated (from xxx -> xxx)...

Please make sure all R and RStudio windows are closed. Close them, re-open, and retry the installation.

---

- Your R version (xxx) is too low....

R major version is too low, return to [install the prerequisites.](../RAVE/Install_prerequisites.html)

---

- Cannot find antspy or antspy installation fails

Please make sure you install all the prerequisites! If you are on M1 Mac and have Intel version of conda installed. Please uninstall that conda first. To "just" configure Python environment, run:

```
   ravemanager::configure_python()
```

## Step 3: Running the Demo

Close all instances of "R" and restart "R". Copy and paste the following command into the "R" console:

```
   rave::start_yael()
```

In a few seconds a web browser window will appear. A great deal of text will appear in the "R" console; this can be safely ignored.
