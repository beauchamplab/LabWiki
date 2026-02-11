> **Navigation:** [Home](index.md) • [Install](Install.md) • [Help](Help.md)

# Install deprecated

|  |  |
| --- | --- |
| [RAVE logo](../../attachments/Install_deprecated/RAVE_Logo_new.jpg "RAVE logo") | **R**eproducible **A**nalysis and **V**isualization of i**E**EG   ***RAVE*** |

## Other methods for installing RAVE

### Docker (special-purpose containerized installation)

RAVE-within-Docker is not recommended for day-to-day (production) usage as performance is worse and usage is more complex.
[For more information, see the GitHub Rave Docker page.](https://github.com/beauchamplab/rave-docker/blob/master/README.md)

### Additional Demo data

Additional sample subjects are available with the commands

```
 raveio::install_subject("YAB")
 raveio::install_subject("YAI")
```

RAVE includes time series data from one subject for single subject processing and collated data from many subjects for learning group analysis. Additional time series data can be obtained with

```
 options('timeout' = 100000); rave::download_sample_data('XX')
```

Where XX is one of the following: KC, YAB, YAD, YAF, YAH, YAI, YAJ, YAK (~ 1GB per subject). For sample data included with RAVE, XX is 'DemoSubject' and '\_group\_data'.

By default, R limits the amount of time a script can attempt to download a file to 60 seconds. Depending on your Internet connection speed, demo datasets may not download within 60 seconds. You can increase the download timeout by setting a global option. The options('timeout' = 100000) command sets the timeout to 100,000 seconds (27 hours), long enough for even slow connections. You can query the current timeout with:

```
 options('timeout')
```

### Ubuntu Linux Installer (Experimental)

For Ubuntu users, the following command will install R and RAVE bundle. This is an experimental script.

Open terminal (if you don't know how, look at your sidebar in ubuntu, `search your computer` enter "terminal", and open it), type the following code:

```
 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/dipterix/instrave/master/brew/ubuntu-patch.sh)"
```

The terminal will prompt for password. This is because some installations require administrator privilege. Please enter your password (it won't show up on the screen), and hit return key.

### Native Installation (deprecated)

1. **[Install the prerequisites.](Install_prerequisites.md "RAVE:Install prerequisites") The most common installation problem is that the prerequisites are not installed.**  RAVE is written in the programming language "R", so before installing RAVE, "R" must be installed along with RStudio, an integrated development environment for "R". RAVE requires the latest versions of R and RStudio. Trying to install RAVE on older versions of R and RStudio will lead to unpredictable error messages.

2. Open the RStudio application if it is not already open. In Windows, you should open RStudio as an administrator so that you have the appropriate permissions to install the required libraries. Copy and paste the following commands (one at a time) into the RStudio console to install RAVE. In the case of errors, relaunch RStudio and repeat the commands.

```
 install.packages("remotes")
 remotes::install_github('beauchamplab/rave')
 remotes::install_github('beauchamplab/ravebuiltins@migrate2')
```

You will probably be asked the two questions below several times. Each time, for the question:

```
 Do you want to install from sources the package which needs compilation? (Yes/no/cancel)
```

Answer "no". For the question:

```
 These packages have more recent versions available. It is recommended to update all of them. Which would you like to update?
```

Answer "2: CRAN packages only".

3. Once everything gets installed, RAVE needs to download and compile some internal configuration files. In your RStudio console, type the following command:

```
 rave::check_dependencies(nightly = TRUE)
```

4. Finalize installation and install demo data.

```
 rave::finalize_installation(upgrade = 'ask')
```

Downloading data will take minutes. To check on progress, click on the "Jobs" tab. When a single job finishes, click the small left blue arrow in the top left to see the screen with all jobs. When all downloads are shown as complete, click on the "Console" tab and launch RAVE.

### OSX Installer (Experimental)

For Mac users, the following command will install brew, R, RStudio, and RAVE bundle. This is an experimental script.

Warning: the script will REMOVE currently installed R, RStudio and install the latest version according to your system architecture (for example, both R and RStudio will be ARM build on Apple M1 chip). Please use the default installation guide if you have already got R for other projects.

Please open termina.app at /Applications/Utilities folder, copy-paste the following command, and hit return. The terminal will prompt for password. This is because some installations require administrator privilege. Please enter your password (it won't show up on the screen), and hit return key.

```
 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/dipterix/instrave/master/brew/osx-patch.sh)"
```

### Mac Install via script (recommended for Intel Macs only)

[Click here to download the Mac installation script.](https://github.com/dipterix/instrave/raw/master/rave-installer-macosx.command.zip)

This script has only been tested with Catalina (MacOS 10.15). May not work with newer OS or Mac. For the new Mac architecture with Apple silicon (instead of Intel) follow the [full installation guide](Install.md#Full_Installation_Guide_For_Any_Platform "RAVE:Install"). The forthcoming R version 4.1 is expected to include a native Apple silicon binary. Until then, R will use Apple's Rosetta2 Intel emulation.

1. After download, find the file "rave-installer-macosx.command.zip" in the "Downloads" folder.
2. If it has not automatically been unzipped, double-click to extract the file named "rave-installer-macosx.command".
3. To run the the commands in the script, right click (with no right mouse button, hold down the control key on the keyboard and click the mouse button or trackpad) on the file to bring up an actions menu and select the first choice, "Open". The warning "rave-installer-macosx.command is from an unidentified developer. Are you sure you want to open it?" will be presented, choose "Open" to proceed. If "Open" is not shown (only "OK") you may have left-clicked instead of right-clicked on the installer script. Select "OK" and try again.

The script installs R, RStudio, RAVE and all dependencies including the 3D Viewer, the N27 brain and demo data. You will be asked various "Do you accept this license?"-type questions along the way. The installer will place a "RAVE" icon on your desktop. Double-click the icon to launch RAVE.

### Mac Install via package

Installation via package can be useful in some cases, such as a computer that is not connected to the Internet; the package can be loaded on the machine with a USB key. This script has only been tested with Catalina (MacOS 10.15) and may not work with other OS versions.

1. Download the RAVE installer package from <https://github.com/beauchamplab/ravecmd/raw/main/osx/RAVE%20Bundled%20Installer/build/rave-bundled-installer-1.0.2.pkg>. Double click on the package, Click "Continue", then click "Install." You will be prompted for your Mac password, as when installing any other software. You should be rewarded with the message "The installation was successful." Click "Close". You will be given the choice to move the Installer to "Trash"; either option is fine. These steps will place the installer in the /Applications folder.
2. Click anywhere on the Mac desktop to go the Finder. Click "Go/Applications" in the menu bar to open the Applications folder. Open the /Applications/RAVE folder, then double-click on the "RAVE Bundled Installer" icon (you will be prompted for your Mac password, as when installing any other software).
3. If asked, click "Accept" to install the Apple Xcode command line toolbox. Drag the RStudio icon to the /Applications folder. (These steps are optional but recommended).
4. Verify that the installation is complete by waiting until the "[Process completed]" messages appears in the console window. This may take ~30 minutes.
5. Go to Finder and find the /Applications/RAVE/bin folder. Click on the "rave" icon to launch the main application.
6. To install demo data, double-click on "rave-demo-data" located in /Applications/RAVE/bin (optional but recommended)
7. To update RAVE, simply repeat the steps above. To ONLY update the utility scripts in /Applications/RAVE/bin double-click on "Update Scripts".

### Experimental RAVE

For the latest experimental features, install the development build. Check GitHub for latest versioning information.

```
devtools::install_github('beauchamplab/ravebuiltins@migrate2')
devtools::install_github('beauchamplab/rave')
devtools::install_github('dipterix/threeBrain')
devtools::install_github('dipterix/dipsaus')
```

if asked

```
 These packages have more recent versions available. It is recommended to update all of them. Which would you like to update?
```

Type

```
 3: None
```

Restart the RStudio session after installing the new version.
