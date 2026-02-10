# SurfaceMetrics

> **Navigation:** [Home](index.md) | [Publications](Publications.md) | [Resources](DataSharing.md)

|  |  |
| --- | --- |
| [Brain picture](../../attachments/AuditoryTactile/BrainPic.0023.png) | Beauchamp Lab Notebook |

- [Home](index.md "Beauchamp")
- [Lab Members](Lab_Members.md "Beauchamp:Lab Members")
- [Lab Alums](Lab_Alums.md "Beauchamp:Lab Alums")
- [Projects](Projects.md "Beauchamp:Projects")
- [Publications](Publications.md "Beauchamp:Publications")
- [*Lab Notebook*](Lab_Notebook.md "Beauchamp:Lab Notebook")
- [Subjects](Subjects.md "Beauchamp:Subjects")

- [Software Installation](Software_Installation.md "Beauchamp:Software Installation")
- [Ordering](Ordering.md "Beauchamp:Ordering")
- [MRI Data Analysis](MRI_Data_Analysis.md "Beauchamp:MRI Data Analysis")
- [Electrophysiology](Electrophysiology.md "Beauchamp:Electrophysiology")
- [TMS](TMS.md "Beauchamp:TMS")

To find the closest node on the surface from a point in the space use SurfaceMetrics function. This is useful for finding the closest node on the surface to a stimulator (electrode, TMS coil, etc.). Here is an example to find the closest node to each electrode on the right hemishphere of subject DE:

```
SurfaceMetrics -spec DE_rh.spec -sv DE_SurfVol_Alnd_Exp+orig -surf_A rh.pial.asc -closest_node ElectrodesRight.1D \
-prefix DEClosestNodesRight
```

see also
[Beauchamp:Electrophysiology](Electrophysiology.md "Beauchamp:Electrophysiology")
