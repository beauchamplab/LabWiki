> **Navigation:** [Home](index.md) • [Install](Install.md) • [Help](Help.md)

# RAVEGUI Help

|  |  |
| --- | --- |
| [RAVE logo](../../attachments/RAVEGUI_Help/RAVE_Logo_new.jpg "RAVE logo") | **R**eproducible **A**nalysis and **V**isualization of i**E**EG   ***RAVE*** |

## Launching RAVE

Open R (or RStudio) and enter the following command into the console:

```
 rave::start_rave2()
```

A new web browser window should open with the RAVE splash screen. RAVE is developed and tested using Google Chrome; some features in the Volume/Surface viewer, such as recording videos and loading volumetric MRIs, may not work in other browsers.

In the [RAVE Toolbar](ravemodules.md#RAVE_Toolbar "RAVE:ravemodules") click on [Select Data](select_data.md "RAVE:select data") to explore the provided demo data. If you receive a "No valid project detected" message, see the "Install RAVE" tab and follow the instruction to download demo data. To load your own data, [follow these steps.](ravepreprocess.md "RAVE:ravepreprocess") User interactions with RAVE occur through a web browser.

## Shutting down RAVE

Closing the browser window containing the RAVE GUI does not affect the RAVE server. To stop the server:

1. If RAVE was launched from "R", select the R Console window and press the "Esc" key. If RAVE was launched from "RStudio", click the red "stop sign" icon in the RStudio window. These action stop the RAVE server. The browser window will turn gray, indicating that the browser is disconnected from the RAVE server; close the window if desired. (Note that you will still be able to interact with the browser window but it will appear dim.)
2. Quit "RStudio" or "R" if desired.

## Advanced: Launch RAVE in server mode

To launch a RAVE server, enter the following command on the server machine:

```
rave::start_rave(host = 'Server_IP_Address', launch.browser=FALSE, port = 8787)
```

Port numbers 0-1023 are reserved and should not be used but any other port value should be fine. Client computers on the local network can interact with the RAVE server using a web browser:

```
http://Server_IP_Address:8787
```

where Server\_IP\_Address and 8787 match the server values above. A server can host multiple RAVE instances by opening a new RStudio session ("Session"/"New Session") and launching RAVE with a different port number.

## Troubleshooting

see the [Troubleshooting section on the Help tab](ravemodules.md#Troubleshooting "RAVE:ravemodules")

## Running RAVE on servers

[Run RAVE on remote servers via VSCode and SSH](VScode.md "RAVE:VScode")

[How to use RAVE on the BeauchampLab MacPro](MacPro.md "RAVE:MacPro")

[How to use RAVE on the UAB Cheaha Cluster](UAB.md "RAVE:UAB")

[Older notes](Deprecated.md "RAVE:Deprecated")
