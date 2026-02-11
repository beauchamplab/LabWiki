---
title: MacPro
parent: RAVE
---
# MacPro

|  |  |
| --- | --- |
| [RAVE logo](../../attachments/MacPro/RAVE_Logo_new.jpg "RAVE logo") | **R**eproducible **A**nalysis and **V**isualization of i**E**EG   ***RAVE*** |

# Using RAVE on the BeauchampLab MacPro at Penn

To run RAVE on the BeauchampLab MacPro (or any server) installation on the local machine is not required. However, some local steps are required. On Macs, Xcode must be installed

```
xcode-select --install
```

Xcode may need to be reinstalled after after major MacOS updates.

[Click here to download the script](../../attachments/MacPro/MacPro-Command-220727.zip "MacPro-Command-220727.zip"). After download, double-click to unzip the file. This will create two files, one for launching pre-processing and one for launching RAVE. Drag the unzipped icons to your desktop or other convenient location.
**The first time the script is run, you must right-click on it to open a context menu**, then select "Open", then "Open" again to bypass the security warnings. Then, answer the question

```
 Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

with "yes". You will be prompted for the server password. A "Terminal" window will open, necessary to connect to the MacPro, and a browser window will open showing the RAVE GUI.
After the first usage, just double click on the icon to run RAVE.

**If the script fails, connect to the MacPro with TeamViewer, open Preferences/Sharing, stop and start "Remote Login"**

Note that the script will not work unless you are on PennNet; access via vpn.upenn.edu

The BeauchampLab MacPro has a 3.2 GHz 16-Core Intel Xeon W CPU and 786 GB 2933 MHz DDR4 RAM. The MacPro also has a direct fiber channel connection to the RAID where the iEEG data is stored. In combination, this allow for much faster performance than on a user's local machine. RAVE runs on the MacPro and the RAVE GUI is displayed in a web browser on the local machine. To run RAVE in this mode:

1. Connect to the institutional network VPN (if outside of campus).
2. Start a RAVE session on the MacPro.
3. Connect to the MacPro RAVE session with a web browser on your local machine.

#### Shutting down a RAVE Client

Closing the browser window on your local machine will NOT terminate RAVE running on the MacPro. You must click on the "Terminal" window (opened above). Click on the red circle in the top left of the window to close it. Select "Terminate" to terminate running processes. This will shut down the RAVE server and disconnect the RAVE client, graying out the web browser window containing the RAVE GUI, which can be safely closed.

#### Computer Sleeping Terminates RAVE Session

The client machine starts RAVE on the server using ssh. When the ssh session stops for any reason (such as the client computer sleeping), the RAVE server on the MacPro will be terminated. As a work-around, start RAVE on the server using VNC or try one of the following
<https://www.tecmint.com/keep-remote-ssh-sessions-running-after-disconnection/>

#### Troubleshooting

1. if you have previously connected to the server with ssh, you may need to clear the ssh cache with

```
 ssh-keygen -R serverIP
```

before you execute the script for the first time.

1. If the browser window shows an error, such as "Host not found", wait a few seconds and then refresh the window. You may wish to copy the script to the desktop or to the /Applications folders.

### Older instructions (also a template for other client/server configurations)

#### Setup a RAVE instance on the server (only required once).

ScreenShare with the server. e.g.

```
 vnc://serverIP
```

On the server, run
RStudio/Session/new session

```
 rave::start_rave(host = 'serverIP', launch.browser=FALSE, port = 1111)
```

where 1111 is a port number.

### Access the RAVE instance from your local machine

VPN into the same network as the server if necessary (most universities have firewalls that will block incoming web browser connections). Start a Chrome browser on your local machine, enter this into address bar:

```
 http://serverIP:1111
```

where 1111 is the port number used above for your RAVE instance. You will the RAVE GUI in Chrome on your local (client) machine, connected to RAVE on the remote server.

#### Troubleshooting

If no data appear on the "Select Data" screen in RAVE, close RAVE, go to RStudio Console and run

```
 rave::rave_options()
```

change Raw subject data path to the appropriate path, e.g.

```
 [...]/data/rave_data/ent_data
```

change RAVE subject data path to

```
 [...]/data/rave_data/raw
```

Make sure to click "Set Directory".
Sometime it may be necessary to clear variables and restart the session.

```
 rm(list=ls(all.names = TRUE)) 
 rstudioapi::restartSession()
```

*Return to [Other Notes](index.md#Other_Notes "RAVE").*
