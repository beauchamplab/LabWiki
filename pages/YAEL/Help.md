---
title: Help
parent: YAEL
---
# Help

|  |  |
| --- | --- |
| [RAVE logo](../../attachments/RAVE/RAVE_Logo_new.jpg) | **Y**our **A**dvanced **E**lectrode **L**ocalizer   ***YAEL*** |

- [Home](index.md "YAEL")
- [Install](Install.md "YAEL:Install")
- [Update](Update.md "YAEL:Update")
- [Launching](Launching.md "YAEL:Launching")
- Tutorials and Help
- [Community](Community.md "YAEL:Community")

## Trying YAEL

A sample dataset is included with YAEL. Click on the "3D Viewer" tab in the YAEL GUI to get started with the sample dataset. Each time you double-click on a CT blob, a new electrode will be created.

## YAEL Videos

**Tutorial video showing electrode localization process with the sample dataset**:

**Videos showing visualization of time series data.**
At left, with activation projected to cortical surface; at right, without activation projected to cortical surface (only electrodes change color):

Load video

YouTube

YouTube might collect personal data. [Privacy Policy](https://www.youtube.com/howyoutubeworks/user-settings/privacy/)

Continue
Dismiss

Load video

YouTube

YouTube might collect personal data. [Privacy Policy](https://www.youtube.com/howyoutubeworks/user-settings/privacy/)

Continue
Dismiss

## YAEL Workflow

The YAEL GUI will guide you through the key steps of selecting MRI and CT volumes; aligning them; entering the electrode plan; and selecting each electrode. For a video demonstration, watch:
Introductory Video

Load video

YouTube

YouTube might collect personal data. [Privacy Policy](https://www.youtube.com/howyoutubeworks/user-settings/privacy/)

Continue
Dismiss

[A step-by-step guide](#)").

## Which CT-MRI Co-registration to use

Installing YAEL automatically installs two popular tools for co-registering the MRI and CT datasets, Advanced Normalization Tools (ANTs) and Nifty Reg. Users may also call the FLIRT registration tool if FSL is installed. ANTs is recommended for most users because it is very fast (typically less than 5 minutes) and provides many options in case the YAEL default selection of rigid-body registration fails. Nifty Reg is fast but offers fewer adjustable parameters in the event of registration failure, while co-registration with FLIRT is flexible but can take several hours. Regardless of the registration tool selected, it is important to verify the CT-MRI alignment.

## Support

To help get you up to speed with YAEL, please contact the developers to schedule an online (Zoom) tutorial. Using your own data, we will walk you through the steps to localize electrodes.
Personalized support is also provided via a dedicated **#support** channel in the RAVE Slack workspace *rave-brain.slack.com*. E-mail slack@rave.wiki for an invitation to the support channel.

## Troubleshooting

**Browser disconnected from server**. A common issue is that the RAVE GUI in the browser window appears dim or grayed out. This indicates that the browser has become disconnected from the server (e.g. if the computer has gone to sleep mode and then woken up). To reconnect to the server, try refreshing the browser window (right-click and select "reload" or highlight the URL the browser address bar and press enter). If this does not work, then follow the instructions for shutting down the RAVE server, then relaunch.

**Other browser issues**
YAEL is developed and tested using Google Chrome; some features, such as recording videos and loading volumetric MRIs, may not work in other browsers.
