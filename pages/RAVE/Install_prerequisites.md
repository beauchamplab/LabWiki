---
layout: default
title: "Install prerequisites"
parent: RAVE
---

# Install prerequisites

|  |  |
| --- | --- |
| [RAVE logo](../../attachments/Install_prerequisites/RAVE_Logo_new.jpg "RAVE logo") | **R**eproducible **A**nalysis and **V**isualization of i**E**EG   ***RAVE*** |

All user interaction occur via a web browser, and Google Chrome is recommended (other browsers may have worse performance for complex graphics operations). Chrome can be installed from <https://www.google.com/chrome/dr/download>

## Prerequisites for MacOS

### 0. Login to an admin account

MacOS requires users to have administrator (admin) privileges to install applications. At several points during the installation, MacOS will ask for your account password to verify installation. Installation will fail if your MacOS account doesn't have admin privileges.

**How to check if I have an admin account?** Open "terminal" (in the /Applications/Utilities folder). Copy the command line shown below into the terminal window.

```
 sudo ls
```

You will be prompted for a password. This is the password of the MacOS account you are logged in as. If you have an admin account, MacOS will show the files in the current directory. If not, you will receive an error message. Alternately, click anywhere on the desktop to activate the MacOS menu bar, click on the Apple icon at the top left of the menu bar, then "System Preferences" or "System Settings", then "Users & Groups". Find your current account and verify that it has admin privileges.

**What if I don't have an admin account?** You will need to create a new account with admin privileges or change the privileges of your current account, see <https://support.apple.com/guide/mac-help/change-users-groups-settings-mtusr001/mac> . If your computer is administered by others, ask them to create an admin account for you.

### 1. Install R, version 4 or higher

[Click here to install the latest version of the R language for Mac.](https://cran.r-project.org/bin/macosx/) Find the latest package (.pkg) file, click to download, then open and install. There are different versions of R for older Macs with Intel CPUs and newer Macs with Apple CPUs (M1/M2). Choose the correct version, either "Intel 64-bit" or "Apple silicon ARM64".

**To verify R installation:** R will be installed in the /Applications folder. Open this folder and double-click on the R icon to start R. After starting R, we recommend that you right-click on the R icon in the Dock and select "Options"/"Keep in Dock" to make it easier to launch with a single click. We also recommend starting R, opening the "Preferences"/"Startup" tab, and change "Save workspace on exit from "R" to "No". Uncheck the box "Read history file on startup". To check the current version of "R", start R and enter the following into the console:

```
 R.version
```

This will produce a number of lines of output, beginning with something like

```
 platform       x86_64-apple-darwin17.0     
 arch           x86_64
```

### 2. homebrew package manager

Installation requires the latest version of the ["homebrew" package manager.](http://brew.sh)
Open "terminal" (in the /Applications/Utilities folder). Copy the command line shown below into the terminal window.

```
 /usr/bin/env bash
```

Copy the line below into the terminal window.

```
 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

This step will take several minutes to complete. Wait until the installation is finished and the command prompt reappears before moving to the next step.

**Add brew to your path or the next installation steps will fail.** The installer provides the necessary command lines in the Terminal window at the conclusion of the previous step. Execute them in the same terminal window by copying and pasting. They will look something like

```
 echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
 eval "$(/opt/homebrew/bin/brew shellenv)"
```

These commands will not produce any output.

**To verify brew installation:** Copy the command line shown below into the terminal window.

```
 brew --version
```

Should produce a result like

```
 Homebrew 3.4.1
 Homebrew/homebrew-core (git revision f03c984ad7; last commit 2022-03-08)
```

### 3. Install libraries using brew

Enter this command into the terminal window:

```
 brew install hdf5 fftw pkg-config cmake libpng
```

This step will install the hdf5 (high-performance file system), fftw (fast-fourier transform library), pkg-config (package configuration toolbox), cmake (cross-platform make for compiling optional packages such as ant), libpng (library for manipulating png images) and takes several minutes to complete. Wait until the installation is finished and the command prompt reappears before moving to the next step.

### 4. Finished with prerequisites

Scroll to the top of the page and click on the "Install" tab to return to the full installation guide.

### 5. Troubleshooting

You may receive this message

```
 Warning: macOS is reporting that you have not yet agreed to the Xcode license. This can occur if Xcode has been updated or reinstalled (e.g. as part of a macOS update). Some features (e.g. Git / SVN) may be disabled.
```

To make this error go away, open the "Terminal" app in the Applications folder, enter

```
 sudo xcodebuild -license accept
```

Then restart RStudio.
[A helpful article in case of XCode installation errors.](https://www.moncefbelyamani.com/how-to-install-xcode-homebrew-git-rvm-ruby-on-mac/)

If the XCode download from the RStudio install in step 2 fails, install the command line tools manually. First, [download XCode.](https://apps.apple.com/us/app/xcode/id497799835?mt=12) Click "GET" (if instead you see "OPEN", then Xcode is already installed.) Open the "Terminal" app in the Applications folder, enter

```
 xcode-select --install
```

Click "yes" to proceed with installing the command-line tools. The message "xcode-select: error: command line tools are already installed" means that you can proceed.

## Prerequisites for Windows

These instructions are for Windows 10 with "bash" enabled. You will be asked many questions by the installers; the default response is fine for all of them.

1. [Install the latest version of the R language](https://cran.r-project.org/bin/windows/base/)
2. [Install the latest version of RTools.](https://cran.r-project.org/bin/windows/Rtools/) The version of RTools must match your version of R. RTools contains compilers used to compile routines for faster execution.
3. Finished with prerequisites. Scroll to the top of the page and click on the "Install" tab to return to the full installation guide.

## Prerequisites for Linux

To install R, please go to <https://cran.r-project.org/> and read installation guide for Linux system.
The following guide is for Ubuntu 20.x (x86\_64) system. Please do ALWAYS read R's official installation guide.

:   1. Add R-Cran repository to your app list:

Open terminal (if you don't know how, look at your sidebar in ubuntu, `search your computer` enter "terminal", and open it), type the following code:

```
 # update indices
 sudo apt update -qq
 # install two helper packages we need
 sudo apt install --no-install-recommends software-properties-common dirmngr
 # import the signing key (by Michael Rutter) for these repo
 sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
 # add the R 4.0 repo from CRAN -- adjust 'focal' to 'groovy' or 'bionic' as needed
 sudo add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/"
```

:   2. Install R

Copy the following command line by line into your terminal and run

```
 sudo apt-get install r-base r-base-dev
```

:   3. Type and enter "R" your terminal. This launches R from your terminal.

Copy the following command line by line into your terminal and run

```
 install.packages('ravemanager', repos = 'https://rave-ieeg.r-universe.dev')
 ravemanager::system_requirements(sudo = TRUE)
```

If your operating system is supported, it will print out all the system libraries needed.

:   4. Install compiling tools and system dependencies

Open a new terminal window, copy the installation script generated from the last step into this new window.
For example, on Ubuntu 20.x,

```
 sudo apt-get install -y build-essential file git psmisc procps sudo wget make cmake \
   libsodium-dev libffi-dev libbz2-dev libpcre2-dev libcairo2-dev libssh2-1-dev libtiff5-dev libv8-dev \
   libicu-dev zlib1g-dev libcurl4-openssl-dev libssl-dev libfontconfig1-dev libfreetype6-dev \
   libfribidi-dev libharfbuzz-dev libjpeg-dev libpng-dev libtiff-dev pandoc libxml2-dev git libgit2-dev \
   libfftw3-dev libhdf5-dev libglpk-dev libgmp3-dev libzmq3-dev python3
```

The packages `libv8-dev` is for `V8` package to enable JavaScript. `libxml2-dev` is for `xml2`. `libfftw3-dev` `libtiff5-dev` are necessary for fast-fourier transformations and `libhdf5-dev` is for reading and writing data in open data format `HDF5`. All the other packages are necessary for `devtools` (compilers)

:   5. Install the free version of RStudio Desktop here:

Go to <https://www.rstudio.com/products/rstudio/download/#download> and download one with keywords "Ubuntu 16.04+/Debian 9+ (64-bit)", move the downloaded file to your \*\*desktop\*\*, rename it "rstudio.deb".

Open terminal, type the following command in your terminal

```
 cd ~/Desktop
 sudo dpkg -i ./rstudio.deb
```

and `RStudio` should be in your application list. If not, look at your sidebar in ubuntu, click \*\*search your computer\*\* and enter "RStudio".
See [[1]](https://github.com/beauchamplab/rave/blob/master/inst/markdowns/Installation_questions.md#recommended-settings) for more help.

**Finished with prerequisites. Scroll to the top of the page and click on the "Install" tab to return to the full installation guide.**

## For Developers and Power Users

RStudio provides many useful tools for R developers. If you expect to be developing your own tools, we recommend that you install RStudio. If you have an older version of RStudio installed, be sure to update to the newest version.

1. Install RStudio Desktop from the RStudio website [Install RStudio Desktop](https://www.rstudio.com/products/rstudio/download/). Choose the RStudio Desktop (Free) version. Alternatively, RStudio can be installed from the command line. Enter the following command into the terminal window:

```
 brew install --cask rstudio
```

For either method on Macs, RStudio will be installed in the /Applications folder. We recommend that you open this folder, and right-click on the RStudio icon and select "Options"/"Keep in Dock" to make launching easier. We also recommend starting RStudio, opening the "Preferences" menu, and changing two items: uncheck the "Restore .RData into workspace at startup" option, and change "Save workspace to .RData on exit:" to "Never". Click "Apply" and follow the prompts to restart RStudio.
