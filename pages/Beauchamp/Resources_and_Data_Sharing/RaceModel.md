---
layout: default
title: "RaceModel"
parent: Resources and Data Sharing
grand_parent: Beauchamp
---
# RaceModel


|  |  |
| --- | --- |
| [Brain picture](../../../attachments/AuditoryTactile/BrainPic.0023.png) | Beauchamp Lab Notebook |

- [Home](../index.md "Beauchamp")
- [Lab Members](../Lab_Meetings_and_Notes/Lab_Members.md "Beauchamp:Lab Members")
- [Lab Alums](../Lab_Meetings_and_Notes/Lab_Alums.md)
- [Projects](../Publications_and_Talks/Projects.md)
- [Publications](../Publications_and_Talks/Publications.md "Beauchamp:Publications")
- [*Lab Notebook*](../Lab_Meetings_and_Notes/Lab_Notebook.md "Beauchamp:Lab Notebook")
- [Subjects](../Lab_Meetings_and_Notes/Subjects.md "Beauchamp:Subjects")

- [Software Installation](../Data_Processing/Software_Installation.md)
- [Ordering](../Lab_Meetings_and_Notes/Ordering.md)
- [MRI Data Analysis](../Data_Processing/MRI_Data_Analysis.md "Beauchamp:MRI Data Analysis")
- [Electrophysiology](../Data_Processing/Electrophysiology.md "Beauchamp:Electrophysiology")
- [TMS](../Data_Processing/TMS.md "Beauchamp:TMS")

Race model (Raab 1962) analysis is to test whether reduced reaction time when more than one sensory modality exist is the result of multisensory integration and not just the statistical advantage of having multiple sources of information. One common way of estimating it is:

```
P(Race Model) = P(modality 1) + P(Modality 2) - P(modality 1) * P(modality 2)
```

Here is an example:

[![](../../../attachments/RaceModel/Rmi_example.jpg)](../../../attachments/RaceModel/Rmi_example.jpg)

where red and blue lines show the distribution of RTs for unisensory trials. Green shows what would be expected for multisensory trials from the race model. Black shows what was actually seen in multisensory trials which for RTs less than ~575ms is better than the race model, showing the advantage of multisensory integration. (data is made up for illustration purposes)

RMI is a software for this test developed by Ulrich and Miller. It can be downloaded from

<http://psy.otago.ac.nz/miller/index.htm> [[1]](http://psy.otago.ac.nz/miller/index.htm)

For more info see:

Ulrich, R, Miller, J & Schröter, H (2007) "Testing the race model inequality: An algorithm and computer programs" *Behavior Research Methods* 39, 291-302.
