# AFNI Install

> **Navigation:** [Home](index.md) | [Publications](Publications.md) | [Resources](DataSharing.md)

|  |  |
| --- | --- |
|  | Beauchamp Lab wiki |

- [Home](index.md "Beauchamp")
- [Publications](Publications.md "Beauchamp:Publications")
- [Resources](DataSharing.md "Beauchamp:DataSharing")

1. [How To Install Software and set up new computers](Software_Installation.md)

### AFNI

Follow the directions on the AFNI website to install AFNI

```
 https://afni.nimh.nih.gov/pub/dist/doc/htmldoc/background_install/install_instructs/steps_mac.html
```

On a Mac with 10.11.6, it was necessary to add the following lines to the .cshrc file:

```
 setenv DYLD_LIBRARY_PATH  /opt/X11/lib/flat_namespace 
 setenv DYLD_FALLBACK_LIBRARY_PATH XXXXX
```

Replace XXXXX with the directory AFNI is installed in

It can be nice to customize AFNI with your favorite settings. To do this, you can copy the default AFNI setup file into your home directory and edit it as follows:

```
 cd ~
 open -e .afnirc
```

Alternately, there is a lab version that is already customized on the server:

```
 cd ~
 cp /Volumes/data/script/.afnirc .
```

##### Notes on OSX 10.11

Peter Molfese writes:
Just a warning for users upgrading to Mac OS X 10.11 "El Captain". A new security feature called "System Integrity Protection" prevents Python from directly accessing variables such as DYLD\_FALLBACK\_LIBRARY\_PATH. You may notice that the Python superscripts (e.g. afni\_proc.py, align\_epi\_anat.py) may fail at 3dSkullStrip or 3dAllineate. While running these programs individually will work fine. A workaround (at the sacrifice of some of Apple's intended security) is to disable the new feature by doing the following:

1. Reboot your computer holding Command+R to enter Recovery Mode
2. Under the Utilities Menu select Terminal
3. Run: csrutil disable
4. Reboot

### XCode and Terminal

For the complete install, you will need to download XCode from the App Store. An account on the Apple Store is required (MSB has one) but the download is free. You must also go to Preferences/Downloads in XCode and install the command line utilities.

```
  xcode-select --install
```

from the Terminal and select the Install button.
The complete install instructions also tell you how to install fink from

```
    http://www.finkproject.org/download/srcdist.php
```

The complete install instructions also mention some of the following nice but not essential steps:
Configure your terminal. Go to Applications > Utilities and drag Terminal to the dock as you will most likely be using it often. Open terminal and go to Preferences. Under "Shells open with", click "Command (complete path)" and enter:

```
  /bin/tcsh
```

Copy over a .cshrc file which will help you set up your path every time you open Terminal.

```
  cp /Volumes/data/scripts/.cshrc ~/
```

If at any point you need to add something to your path, open the .cshrc file

```
  open -e ~/.cshrc
```

and add it in the following line:

```
  set path = ( $path /sw/bin /Applications/AFNI/ /Applications/MATLAB_R2011a.app/bin)
```

## Installing/Updating Programs

### XCode/XTools

See "Configuring a new Mac", above, for info on installing XCode.

```
http://trac.macosforge.org/projects/xquartz
```

1. XcodeTools and X11SDK from the Leopard DVD.
2. Maybe the latest X11 package from trac.macosforge.org
3. glib2-dev glib netpbm openmotif from fink (stable source will do).
4. mesa mesa-libglw mesa-libglw-shlibs mesa-shlibs from fink (unstable source).

If you have an older Mac, you will periodically need to go to Apple.com and download the latest XCode and XTools. They are NOT automatically installed by the Apple Software Update routines.

"You will need to re-install this package after future OS, and Security Updates delivered through Apple's Software Update. Additionally, you should reinstall this package after installing XCode."

From: <http://xquartz.macosforge.org/trac/wiki/X112.6.1>

### Configuring your login shell

UNIX can use different command line interfaces, called shells. The shell preferred by AFNI and FreeSurfer is called tcsh.
The UNIX command line can be accessed through either the X11 program or the Terminal program. The Terminal program is preferred; it makes cutting and pasting between windows and changing window properties easier. To change the login shell used by Terminal, go to Terminal/Preferences/Startup, in "Shells open with" select Command and enter

```
 /bin/tcsh
```

For ease of access, drag the Terminal icon (or the X11 icon) to the dock.

Changing the login shell used by X11 is more complex.

Every time tcsh starts, it reads commands from the file .cshrc
To copy MSB's tcsh, type

```
 cp /Volumes/data9/surfaces/scripts/.cshrc ~/
```

Because AFNI uses all three mouse buttons, you must tell the Mac to allow this.
Click on system preferences/Mouse and Keyboard/Mouse and select the middle mouse button to be button #3 and the right mouse button to be button #2. You may also have to go to system preferences and turn off the middle mouse button to access Dashboard/Expose/Spaces.

Other software that may be handy to have:
Adobe Creative Suite; Firefox; Skype

To install software, it may be necessary to have a root password.
To create one, type sudo passwd root

NB: SUMA is unstable with some versions of X11. If SUMA crashes, upgrade your X11 as follows.
First see which is the latest version by going to

```
   http://xquartz.macosforge.org/trac/wiki/Releases
```

Next, follow these instructions (replacing 2.3.0.pkg with the latest version)

```
 quit X11
 http://xquartz.macosforge.org/downloads/X11-2.3.0.pkg
 Install the new X11
 logout, login and relaunch X11
```

The built-in Preview software in Mac OSX is the best way to view PDFs and does not require downloading anything (unlike Adobe Acrobat). For editing PDFs, the free Skim software is recommended
<http://skim-app.sourceforge.net/>

### Fink

This step may not be required for newer Macs.

Fink is a program package manager for Macs. Download the program from the Fink webpage:

<http://fink.sourceforge.net/>.

The program in the dmg file will be straightforward. You can copy finkcommander to the applications folder for a GUI interface.
You should update your libraries every few weeks by running the following:
fink selfupdate; fink update-all

To add it to your path, add
source /sw/bin/init.csh
To your .cshrc file.

#### Installing Required Libraries for AFNI

Type the following line to have Fink grab the newest versions:

```
fink install glib2-dev glib netpbm openmotif3
fink install wget
```

If you’re using OS X Lion you may not need the glib package.

#### Updating AFNI

Many common problems arise because users are using an old version of afni. Type the following command to find out what version you have. If it is older than one month, update it!

```
 afni -version
```

AFNI is frequently updated, so it is important to make sure you have the most recent version. To update, type

```
 @update.afni.binaries -defaults
```

However, this command will only install the most recent version for the operating system that you originally installed AFNI for. For instance, if you originally installed AFNI for Mac OSX 10.5, it will only install the most recent version of AFNI for OSX 10.5. If you have updated your Mac's operating system in the meantime, even the most recent version for the wrong operating system will not help you. Instead, you need to update AFNI to the correct (most recent operating system) using this command (replace 10.7 with whatever the most recent version of AFNI is):

```
 @update.afni.binaries -package macosx_10.7_Intel_64
```

An older less-automatic way to update (for Intel Macs) is the following. Set the variable "pkg" to the latest version:

```
 set pkg = macosx_10.5_Intel_64
 wget http://afni.nimh.nih.gov/pub/dist/tgz/{$pkg}.tgz
 tar xvfz {$pkg}.tgz
```

No matter how you update, you must type

```
 rehash
```

after you update so that the shell will find the newest version or programs.

When you update AFNI, you should also type

```
 suma -update_env
```

Another way to update AFNI (change the package and bindir appropriately):

```
sudo @update.afni.binaries -package macosx_10.5_Intel_64 -bindir /Applications/afni
```

Optionally, it can be good to test the new version BEFORE overwriting the old version. Here is how we can test SUMA:

```
 cd {$pkg}
 ./suma
```

If it works, we copy it over the old version (type "which afni" if you are not sure which directory afni is in)

```
 mv {$pkg}/* /Applications/AFNI/
 rm -r {$pkg}.tgz {$pkg}
```

If AFNI won't run after updating, it is probably because some of your libraries are out of date. The easiest fix is to first try adding the following line to your .cshrc file that directs to the right library path (solution found from [this](http://afni.nimh.nih.gov/afni/community/board/read.php?1,135117,135194#msg-135194) AFNI message board thread). This will help if you get an error after running 3dSkullStrip and are running a non "noglib" version of AFNI.

```
 setenv DYLD_FALLBACK_LIBRARY_PATH Applications/AFNI
```

If this still does not help, follow the instructions on the AFNI web site to install all necessary libraries; this will install the newest versions. If errors still occur, a failsafe method is to compile AFNI on your machine; this will ensure that only the available libraries are used.

Some statistical programs in AFNI require the free statistical package "R". This can be downloaded from

```
http://www.biometrics.mtu.edu/CRAN/bin/macosx/
```

### FreeSurfer

FreeSurfer is another set of programs developed at NIH for the analysis of functional neuroimaging. We mainly use it for cortical surface reconstruction. Their download page is part of an extensive wiki that describes its many functions.

<https://surfer.nmr.mgh.harvard.edu/fswiki/Download>

It can take a long time to download, so the latest version is kept in the SoftwareISOs directory on the Beauchamp Lab server. Updates to the software are normally posted on the listserv. To set the correct paths for Freesurfer paste the following lines into a terminal window:

```
echo ‘setenv FREESURFER_HOME /Applications/freesurfer‘ >> ~/.cshrc
echo ‘source $FREESURFER_HOME/SetUpFreeSurfer.csh' >> ~/.cshrc
```

FreeSurfer needs a license file. You can request on their web site or copy it.
Copy it FROM the SoftwareISOs directory into the directory where you have installed FreeSurfer:

```
 cd /Volumes/data/SoftwareISOs
 cp FreeSurferLicenseFile /Applications/freesurfer/.license
```

### Caret

Go to [Caret's Download Webpage](http://brainmap.wustl.edu/caret/#DownloadCaret), register for an account, and download the newest release.
Copy the caret folder to the Applications folder on your machine and add the following line to your .cshrc file:

```
  set path = ($path /Applications/caret/bin/)
```
