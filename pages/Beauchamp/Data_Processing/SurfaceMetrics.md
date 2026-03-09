---
layout: default
title: "SurfaceMetrics"
parent: Data Processing and Analysis
grand_parent: Beauchamp
---
# SurfaceMetrics


|  |  |
| --- | --- |
| [Brain picture](../../../attachments/AuditoryTactile/BrainPic.0023.png) | Beauchamp Lab Notebook |

- [Home](../index.md "Beauchamp")
- [Lab Members](../Lab_Meetings_and_Notes/Lab_Members.md "Beauchamp:Lab Members")
- [Lab Alums](../Lab_Meetings_and_Notes/Lab_Alums.md "Beauchamp:Lab Alums")
- [Projects](../Publications_and_Talks/Projects.md "Beauchamp:Projects")
- [Publications](../Publications_and_Talks/Publications.md "Beauchamp:Publications")
- [*Lab Notebook*](../Lab_Meetings_and_Notes/Lab_Notebook.md "Beauchamp:Lab Notebook")
- [Subjects](../Lab_Meetings_and_Notes/Subjects.md "Beauchamp:Subjects")

- [Software Installation](../Data_Processing/Software_Installation.md "Beauchamp:Software Installation")
- [Ordering](../Lab_Meetings_and_Notes/Ordering.md "Beauchamp:Ordering")
- [MRI Data Analysis](../Data_Processing/MRI_Data_Analysis.md "Beauchamp:MRI Data Analysis")
- [Electrophysiology](../Data_Processing/Electrophysiology.md "Beauchamp:Electrophysiology")
- [TMS](../Data_Processing/TMS.md "Beauchamp:TMS")

To find the closest node on the surface from a point in the space use SurfaceMetrics function. This is useful for finding the closest node on the surface to a stimulator (electrode, TMS coil, etc.). Here is an example to find the closest node to each electrode on the right hemishphere of subject DE:

```
SurfaceMetrics -spec DE_rh.spec -sv DE_SurfVol_Alnd_Exp+orig -surf_A rh.pial.asc -closest_node ElectrodesRight.1D \
-prefix DEClosestNodesRight
```

see also
[Beauchamp:Electrophysiology](../Data_Processing/Electrophysiology.md "Beauchamp:Electrophysiology")
