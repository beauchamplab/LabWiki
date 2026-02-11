# Software Installation OLD

> **Navigation:** [Home](index.md) • [Publications](Publications.md) • [Resources](DataSharing.md)

|  |  |
| --- | --- |
|  | Beauchamp Lab wiki |

- [Home](index.md "Beauchamp")
- [Publications](Publications.md "Beauchamp:Publications")
- [Resources](DataSharing.md "Beauchamp:DataSharing")

## Current Version (Penn)

[Beauchamp:Software\_Installation](Software_Installation.md "Beauchamp:Software Installation")

## Instructions For Installing AFNI are now here

[Beauchamp:AFNI\_Install](AFNI_Install.md "Beauchamp:AFNI Install")

## Computer Problems

If you have having software or hardware problems, submit a help ticket describing the problem.
Do not be afraid to request help from MSIT. They are paid to help you!
The link for help tickets is
<http://med.uth.tmc.edu/msit/mshelp.htm>
For installing software, you will need to get administrator privileges. Use Directory Utility to set the superuser password (see <http://support.apple.com/kb/HT1528> for details). Then reboot, try to login as user "root". This same password can then be used in X11 sudo.

## Install Microsoft Office

Log in to the Microsoft Office365 website using your BCM ID and use Office online or install the apps locally.
Alternately, install Microsoft Office 2016 from the server at

```
 beauchampsrv/data/SoftwareISOs/Office2016Mac/Office_Mac_Standard_2016.iso
```

Double click on the ISO, then on the PKG. You may wish to uninstall Office 2011 (drag to the trash from the applications folder). Microsoft will keep updating Office 2011 which wastes time if you are not using it.

### Setting up Mendeley

To help us share PDFs we use Mendeley + a shared Dropbox folder.

1. Assuming you have a dropbox account, ask a lab member to share the folder "LabReferences" with you
2. Go to <http://www.mendeley.com>, setup an account, and download/install the software

Once you have downloaded and installed Mendeley, we need to add a "watch folder" to Mendeley

1. Open Mendeley
2. File -> Watch Folder
3. Navigate the file tree to Dropbox and check the LabReferences box
4. Select OK

If you want to have your own copy of the PDFs (for annotations, etc), we need to setup Mendeley to organize your library into another directory

1. Mendeley Dekstop -> Preferences
2. Choose the File Organizer Tab
3. Check the box for Organize my files and select an appropriate directory
4. You may also check the boxes for "Sort files into subfolders" and "Rename document files" to have Mendeley create a more structured file hierarchy

When you have a PDF that you would like to share, simply copy it to the LabReferences/ folder in your Dropbox. Because all Mendeleys are watching that folder, it will be imported to everyone's library automatically.

**NB:** If people have setup their Mendeley to organize files into a separate directory, once you copy a file into LabReferences, you may not be able to "take it back."

### Additional Software

For additional software you might like (Adobe Illustrator, EndNote, Parallels, etc), check the Installing Software section. If we don't have a valid license number anymore we may need to purchase a new one.

It is also a good idea to set up TimeMachine on your computer to backup everything to the server. If you have Parallels already installed, go to TimeMachine > Options and exclude that folder from the backup.

BCM has a site license for Symantec anti-malware protection. Download from <https://bcm.service-now.com/bcmsp?id=kb_article&sys_id=4dfcad40dbe60b00729c73d78c9619a2>
Please be sure and use the UnManaged versions at the bottom particularly for home users. The Managed versions install a password that only IT has and this complicates things should it have to be removed or altered.

## Installing software

### Installing Psychtoolbox and GStreamer

#### How to setup Matlab and GStreamer on Windows

Install GStreamer first from the URLs below. Only versions 1.18x are supported, later version break text display in Psychtoolbox. Ask me how I know. Click on

```
 Older 1.x binary releases are also available.
```

Then select, 1.18.6/ and msvc then download

```
 gstreamer-1.0-msvc-x86_64-1.18.6.msi
```

Make sure to do a COMPLETE install so that all needed codecs are present!
You may need to set the path so that Matlab can find GStreamer.

1. <https://docs.rocos.io/prod/docs/gstreamer-on-windows>
2. <https://gstreamer.freedesktop.org/download/>
3. <https://gstreamer.freedesktop.org/documentation/installing/on-windows.html?gi-language=c>

here is a help thread on playing movies with Psychtoolbox

1. <https://psychtoolbox.discourse.group/t/no-audio-when-movies-are-played-in-windows/4404>

#### How to setup Matlab2013b and GStreamer on Yosemite

Psychtoolbox is not compatible with Matlab 2014a and higher, so you need Matlab2013b. But Matlab 2013b needs a patch to run on Yosemite.

1. To install Matlab 2013b patch:
   1. If you do not already have Matlab2013b installed, then install it from Mathworks.
   2. Go to the Beauchamplab server>SoftwareISOs>MatlabR2013b\_patch.dmg>R2013b\_patch\_1098655.dmg

In order to make the videos run on Psychtoolbox, you need gStreamer.

1. To install gStreamer:
   1. Open bash shell in Terminal (check terminal> preferences>shells open with>default login shell >/bin/bash).
   2. Copy paste into terminal: ruby -e "$(curl -fsSL <https://raw.githubusercontent.com/Homebrew/install/master/install>)"
   3. Follow the steps.
   4. After homebrew is installed, copy paste into terminal: brew install gstreamer gst-plugins-base gst-plugins-good gst-plugins-bad gst-plugins-ugly gst-libav
   5. Open Matlab2013b and you are all set to run your experiment!

#### Installing Psychtoolbox with Matlab

These instructions can be used to install Psychtoolbox 3.0 with Matlab (64-bit versions). You will need to have administrator privileges, as well as access to ms-nbafmri.

1. Copy `DownloadPsychtoolbox.m` from the SoftwareISOs folder to the desktop.
2. Ensure that you have write access for the pathdef.m file.
   1. Open a finder window and click on Applications
   2. Right-click on Matlab -->Get Info. At the very bottom, under Custom Access, make sure you have Read & Write access. If you do not, click the picture of the lock (bottom right corner), enter your password, and then change to the correct privilege. Click on the lock again to save your changes.
   3. Right-click on Matlab --> Show Package Contents. Right-click on toolbox --> Get Info. Make sure you have Read & Write Access.
   4. Open the toolbox folder. Right-click on local --> Get Info. Make sure you have Read & Write Access.
   5. Right-click on pathdef.m. Make sure you have Read & Write Access.
3. Open Matlab, cd to the desktop, and execute the Download script.
4. Accept all certificate requests and choose defaults during installation
5. **For running Psychtoolbox codes in the new version of Matlab (2013a and over), always use the full path to direct the code to the stimulus directory.**

#### Installing GStreamer

In order to run Psychtoolbox with 64-bit Matlab, you will need to install GStreamer. **Not all versions of GStreamer are compatible!** Make sure to use the one that's on the server (and make sure you don't update this file!)

1. Double-click on `gstreamer-sdk-2013.6-universal.pkg` in the SoftwareISOs folder.
2. Proceed through the installation until you get to Installation Type (where it asks for your installation location). Click on Customize (at the bottom of the window) and click on any boxes that aren't checked. Finish the installation.
3. To ensure that Psychtoolbox is installed correctly, you can test a demo by opening Matlab and typing  `LoadMovieIntoTexturesDemo` .

#### Installing Octave and Psychtoolbox

These instructions were tested under Mac OSX 10.7.4 with Octave 3.2.6 and Psychtoolbox (PTB) 3.0. They should be completed AFTER the initial UNIX installation steps, including installing XCode tools, including command line tools; this installs "svn" which is needed.
The instructions require access to ms-nbafmri, so make sure you are connected to the network via ethernet, UTHSC wifi, or have an open VPN connection

1. Install `Octave-3.2.3-i386.dmg` from `ms-nbafmri/data/SoftwareISOs` (i.e., double-click the dmg file)
   1. Optional: In the Extras/ directory of the Octave dmg there is Gnuplot†, which is necessary if you want to make quick plots with Octave
2. Copy `DownloadPsychtoolbox.m` from `ms-nbafmri/data/SoftwareISOs` to the desktop
3. Open Octave (default install is /Applications/Octave), cd to the desktop, and execute the Download script

```
 octave-3.2.3:1> cd Desktop/
 octave-3.2.3:2> DownloadPsychtoolbox
```

1. Accept all certificate requests and choose defaults during installation
2. Ensure PTB is installed correctly by testing a demo:

```
 octave-3.2.3:3> LoadMovieIntoTexturesDemoOSX
```

If you get an error at this step, it may be because PTB doesn't like your dual monitor configuration. Exit Octave, Change Display Mode to "Mirrored", then Open Octave and run the demo again

Happy PTB'ing!!

† If you try to plot from Octave ( `plot( 1:10)` ) and get an error about DYLD\_LIBRARY\_PATH, then we need to make one more edit for plotting to work:

```
 sudo open -e /Applications/Gnuplot.app/Contents/Resources/bin/gnuplot
```

Find the line: `DYLD_LIBRARY_PATH="${ROOT}/lib:${DYLD_LIBRARY_PATH}"`
and replace it with `DYLD_LIBRARY_PATH="${ROOT}/lib"`
Save the file then relaunch Octave and try to plot again

```
  octave-3.2.3:1> sombrero()
```

### Installing Matlab

If you want to use Psychtoolbox with Matlab (and who wouldn't?) a 32-bit version is needed; R2010a was the last 32-bit release. R2010 a located in the SoftwareISOs folder on the server. Follow the instructions in the UT\_License.rtf file.
for Intel 32-bit OSX will do the trick) as well.

see Ismael for Instructions

### Presentation

**How to get**

Download from NeuroBehavioral Systems website (<http://www.neurobs.com/>)
Trial license is free and good for 30 days. Student version is $100 good for 1 year. You will need to place the order first and then fax/email them both sides of your student ID along with the order and invoice number, as well as the name and contact of your academic advisor. You will need to make an account first to be able to order. After you have successfully purchased the license, you must sign in under the lab ID to retrieve the access code.

**Using two monitors**

- In the Windows display settings (right click on Desktop --> Properties --> Settings), choose the second monitor and select "Extend my Windows desktop onto this monitor"

- Restart Presentation, then go to Settings --> Video and add another display (bottom of page) and choose the appropriate driver for each (top of the page)

- Make sure the second monitor (the one that will show the stimulus) is selected as the primary display device.

**Getting Help**

In addition to the software Help, and looking at previous codes written in the lab, questions may be asked from NeuroBehavioral systems by posting them on their forum. Usually they are very responsive and helpful. Other users may also post a response to your question.

**Audio Setup**

From Settings-->Audio Choose Custom Mixer-->Primary Buffer
Otherwise there will be a ~20ms delay between the time of auditory stimulus presentation and the time that the voltage actually gets to the audio jack! This would be specially crucial for TMS experiments.
If you get an error when trying to play audio stimuli (something like "Device Is In Use") there is probably a strange interaction with Parallels.
This can be fixed in Parallels 7 by Virtual Machine/Configure/Sharing select all sharing options (Share Profile and SmartMount)

**Response Button affecting Parallel Port**

Make sure you set the response\_port\_output header parameter to false, otherwise whenever for example response button 3 in pressed, binary code of 3 (00000011) will be sent to the parallel port!
In SDL section, before begin type:

```
response_port_output =  false;
```

**Configuring Presentation to use USB for output**

Attaching USB to the computer
The computer first needs the NI-DAQmx software installed - download NI USB-6501 (<http://zone.ni.com/devzone/cda/tut/p/id/6913>). Before you install anything, make sure you have .NET Framework 2.0 installed (available at: <http://www.microsoft.com/downloads/details.aspx?FamilyID=0856EACB-4362-4B0D-8EDD-AAB15C5E04F5&displaylang=en>). Under the installer features menu, the bare minimum is:

```
NI-DAQmx 8.8.0
 ->.NET Framework 3.5 Lanugages
 ->.NET Framework 2.0 Lanugages
 ->.NET Framework 1.1 Lanugages
 ->ANSI C Support
```

You will have to restart after you install the software.

After the restart, connecting the device via USB, Windows will detect a "New Data Acquisition Device", and present you with a window offering several options. Select "Configure and Test This Device Using NI Measurement & Automation Explorer" and run a Self-Test when the window opens. If this passes, the USB device can now be used to control TMS through Presentation.

Configuring Presentation to use USB

Now we need to make a few adjustments to the settings. Under the 'Settings' tab, select the 'Port' option and find the 'Output Ports' box. In this box we need to have a total of 2 ports.

Add the first port, and make sure the following options are set:

```
Port: USB-6501
Data source: port0
Register span: 1
Inversion mask: 0
Default pulse width: 5 ms
```

For the second port, the following options need to be set:

```
Port: USB-6501
Data source: port1
Register span: 1
Inversion mask: 255
Default pulse width: 5 ms
```

Using Presentation via USB
The USB controller uses a new library [File:Beauchamp USB TMS library.pcl](../../attachments/Software_Installation_OLD/Beauchamp_USB_TMS_library.pcl) to control the TMS machine. A sample presentation you can use to test to the USB control of the TMS is available: [File:Beauchamp OhmanTMSScenario.sce](../../attachments/Software_Installation_OLD/Beauchamp_OhmanTMSScenario.sce). In this scenario, the up/down arrows are used to control the intensity of the TMS, while the space bar is used to toggle arming/disarming the device, and the return key is used to fire the device. The sample presentation can also be used to help write code in the future - perhaps the most important point is that it is no longer necessary to define an output port inside the pcl, including the Beauchamp\_USB\_TMS\_library.pcl is sufficient.

**Using and recording sound responses**

Sound response buttons can be defined in Presentation using Settings-->Response-->Devices-->sound device (threshold or offset)

Once you chose "sound device" click on "properties" button to the left of "Devices" window and adjust the parameters. You need to choose the correct microphone from the pull down menu, set the threshold, ...

To record a sound response, check the "save responses" button and set the recording duration. Each response will be saved in a separate wave file. You can also check the button to save all responses in one wave file (in addition to the individual wave files).

Another way to record sounds is using:

```
sound_recording{
duration = 1000;
base_filename = "some_file_name";
};
```

within a trial.

#### Parallels and Presentation

Presentation runs only under Windows, but can be run on a Mac using BootCamp OR virtualization software such as VMWare or Parallels.
Here are some benchmarks for a 2010 MacBook Pro with a 2.66 GHz Intel Core i7 and 4 GB RAM:

To assess performance under Windows 7, go to Control Panel/Performance Information and Tools.

Scores are on a scale from 1.0 to 7.9

```
 calculations per second     memory access    Windows graphics    3D graphics for games   hard drive
```

Windows 7 (boot camp)
6.8
5.5
6.4
6.4
5.9

windows 7 (parallels) (1 CPU, 1GB RAM)
4.9
4.5
5.9
4.8
6.2

windows 7 (parallels) (2 CPU, 2GB RAM)
4.9
5.5
5.9
4.8
6.2

To summarize, biggest hit is calculations per second and graphics.

## Running Windows on a Mac

Get Ismael to help you

## Connecting to the Lab Mac Server

Ask someone for the address of the lab server (currently 10.66.4.17). To connect, type Apple-K, then the server IP address.
The username is beauchamplab; ask MSB for the password. There are three share points:

1. **Backups** Used for Time Machine Backups
2. **beauchamplab** not used
3. **Data**  Where all lab data and stuff is stored.

Connect to all three (select all and click "OK"). Open a finder window and double click on "data", or open a Terminal window and type

```
 cd /Volumes/data
```

## Backing Up

Because hard disks fail, it is important to back up your files regularly. The best way to do this is to keep all important work on DropBox. Then there is one copy in the cloud and one your local machine.
It is also good to back up files on your Mac automatically, using Time Machine. Connect the Lab Mac Server (previous step) and make sure the Backups folder is mounted. Open System Preferences/Time Machine/Select Disk/Select "Backups"
**Ask MSB to type in the admin password. It will not work with the beauchamplab password.** You can exclude some directories from being backed up to save time and space. It is good to exclude the DropBox folder because this is already backed up by Dropbox.
If you have Parallels installed on your computer, you can tell Parallels (under the Preferences menu) not to back up the Parallels VM. This will save time because there is no real reason to back up Windows (can be easily reinstalled).

## Configuring a New Mac Server

The lab's data is stored on three Promise Pegasus RAID systems attached to the Mac mini.

1. January 2013: 12 TB (10 TB available with RAID5)
2. June 2013: 18 TB (15 TB available with RAID5)
3. May 2014: 32 TB

When installing a new RAID:

1. Inform all users the machine will be down for a while
2. Install all updates to the OSX
3. Disconnect all RAIDs, then connect them one at a time and perform firmware updates
4. Connect the new RAID

TimeMachine is used to back up on Pegasus RAID to the other. (This does not protect against failures of the Mac Mini but a new Mini is available quickly).
Individual Macs may also be backed up to the RAID. Go to OSX Server and turn on the Time Machine service, adding a share point. This share point can only be accessed with the admin password, assuming it is created with the admin password.

### OsiriX

OsiriX is a DICOM viewer that may be helpful if you need to upload DICOMs, especially from a CT scan taken after electrode surgery with epilepsy patients. It can be downloaded from here:

```
  http://www.osirix-viewer.com/
```

### R

This program is used for the structural equation modeling. If you plan on doing functional connectivity as part of your data analysis, this is a good program to have. You can download it here:

```
  http://cran.r-project.org/bin/macosx/
```

To utilize 1dSEM, click the R icon on the console, then locate the 1dSEM.R script in the AFNI folder and load it.

## Creating Symbolic Links

It is useful to have symbolic links from the command line so you do not need to type the full path to a file. The program ln creates such symbolic links. Here are a couple of examples:

```
ln –s /Volumes/data9/surfaces/ /surfaces
ln –s /Volumes/data1/UT /UT
```

The paths are now linked to /surfaces/ and /UT/.

## Printing

### Printing Double Sided

On a new computer you may notice that the option to print two-sided is greyed out. To fix this, go to System Preferences, Print & Scan, select the printer, then press the Options & Supplies button. Under the Driver tab, click Duplex Printing Unit.

### Dell 5100cn Color Laser Printer

Here is a copy of the manual
<../../attachments/Software_Installation_OLD/Dell_5100cn.pdf>

To use the printer, download the current drivers for your computer from the Dell website

```
 http://support.dell.com/support/downloads
```

Shortcut: drivers are on the server in

```
 /data/SoftwareISOs/MiscSoftware/Dell_5100_cn
```

On Windows XP, you must first add a port, then configure the printer.
On Mac OSX, first run the Installer. Then open System Preferences/Print & Fax
Click the "+" button to add a printer, click on "IP" and enter the IP address (above.)

- - Protocol must be Line Printer Daemon -- LPD

There are sometimes several drivers to choose from.
The PS (postscript) driver under Windows cannot collate.
The PCL driver does. So if you need to collate, use the PCL driver.

In Windows, you must add a Port with this address, then install the correct printer driver and tell it to print to the port.
On the Mac, go to System Preferences, Print & Fax, Click the +, Click IP, enter the IP into the address field.

### HP Photosmart Color Inkjet Printer

Insert the installation CD into your computer and follow the instructions.
The Mac installation software is in /Volumes/data9/Software\_isos/HPPrinter/HP Installer
The status of the printer can be checked at

```
 http://hpfd76cd.local./index.htm?cat=info&page=printerInfo
```

## Mounting Volumes

### Mounting RAID Volumes from Windows

You must have a Mac with a valid user account. On the Mac, go to System Preferences, Sharing, and enable Windows Sharing.
The menu should say

```
 Windows users can access your computer at \\XXX.XXX.XXX.XXX\YYY
```

For Mac OSX 10.5, go to System Preference, Sharing. Enable File Sharing.
Click the "+" button and add your user to the list of Users; change permissions to be Read & Write.
Click on Options and Enable "SMB" which is what Windows uses.
Click the user name (you will be prompted for your password).

You may also need to able your user account. Look for the message

```
 Enabled accounts: Ashley Kingon
```

If your account is not enabled, click on the "Accounts" button and enable it.

Additional steps for Windows VISTA:

Go to the the Start menu and choose 'Computer'

Go to Computer: Local Disk (C:): Windows: regedit

After clicking on the registry editor application:

```
 Go to HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Lsa
 Click on LmCompatibilityLevel
 Set value to 1
 Restart computer
```

In Windows, go to Internet Explorer and type in the URL above.

### Mounting a Volume after sshing to a different machine

For example. I ssh onto tellmore machine. Now I want to access data9 from his machine.

in my home directory (~) (on tellmore) I make a directory called mount, inside of mount I make a directory
called data9 (or which ever volume I am mounting), then I mount data9.

```
cd ~
mkdir mount
cd mount
mkdir data9
mount_afp -i afp://akingon@ipaddress/data9 data9
enter password
```

and now you can cd into data9

## Python

Path:

```
import sys
sys.path # this will show the current path settings
sys.path.append('C:\new_path') # this will add the new path, however only until the 
                               # current python session is open
```

To more permanently add a path, use the Windows environment variable PYTHONPATH

Control Panel --> System --> Advanced tab --> Environment Variables (Bottom of page)--> System variables --> look for PYTHONPATH, if it does not exist, use NEW to create it. Use semi-colon to add multiple paths:

```
C:\path1;C:\path2
```

**IDLE (Python's GUI editor) is slow!**

Displaying outputs on IDLE makes the loop very slow. Here is a test:

```
import time
t0 = time.clock()
counter = 0
while time.clock() <= t0 + 1:
    print "junk"
    counter += 1
```

Running this code on my 2GHz laptop, results in < 400 Hz loop rate using IDLE. Whereas rate is as high as 15 KHz if the code is run from the command line (by double clicking on the python file).

This is very important when detecting a fast event. For example reading parallel port to detect the TTL pulse from MRI scanner [the philips 3T scanner's pulse is currently only 75 microseconds long].

## Misc Unix Notes

Here is the AFNI UNIX tutorial

```
 https://afni.nimh.nih.gov/pub/dist/doc/htmldoc/background_install/unix_tutorial/index.html
```

Loops in tcsh are a handy way to automate data processing. Here is an un-commented example. The syntax varies from shell to shell.

```
set sdall = ( X Y Z P O R T Y)
set idx = 1
foreach ec (FL FM FN FQ FS FU FW FY FZ)
set sd = $sdall[$idx]
@ idx++
echo $idx
end
```

Here is a while loop for tcsh

```
 set idx = 1
 while ($idx < 10)
 @ idx++
 echo $idx
 end
```
