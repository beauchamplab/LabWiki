# SurfDist

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

We may wish to find the distance between two points on the cortical surface. The AFNI program to do this is SurfDist, e.g.

```
 echo 500 1000 > test.1D
 SurfDist -i lh.inflated.asc -input test.1D
```

Gives the result

```
 Note SUMA_LoadNimlDset: ./test.1D has no element and no group. 
 Perhaps it is a .1D read in as a niml dset.
 #Internodal distance along graph of surface lh.inflated.asc
 #A distance of -1 indicates an error of sorts.
 #From   to     Dist. 
 500    1000   26.91
```

In SUMA, we may open the same surface, open a surface controller, and type the node number into the node window to see the node on the surface.
This also gives the x,y,z, co-ordinate.
e.g. for nodes 1000 and 500

```
 26.8501, -134.36, -61.247
 29.5528, -137.10, -35.658
```

The Cartesian distance between these points is

```
 SQRT( (A1-A2)^2 + (B1-B2)^2 + (C1-C2)^2 ) = 25.87
```

This makes sense because the distance along the surface will always be longer than the distance through space. In this case the difference between the Cartesian and surface distances isn't too much because the inflated surface is fairly flat already. In contrast, if we examine the distance between the same nodes on the folded pial surface, it is considerably longer.

```
 SurfDist -i lh.white.asc -input test.1D
 Note SUMA_LoadNimlDset: ./test.1D has no element and no group. 
 Perhaps it is a .1D read in as a niml dset.
 #Internodal distance along graph of surface lh.white.asc
 #A distance of -1 indicates an error of sorts.
 #From   to     Dist. 
 500    1000   28.58
```

To find the distance from a cardinal point, like the back of the brain, we must first find the node number of the desired point.
This can be done manually by clicking in SUMA. For this surface, manual clicking gives

```
 node 62, -2.3346, -102.37, 1.18054
```

A more automated way is to sort the node-coordinates by their y-position. The most posterior point will have the most negative y-coordinate.

```
 sort -n --key=2 lh.white.asc | more 
 (or if you are using a different unix shell)
 sort -n -k 2 lh.white.asc | more
```

returns

```
  -4.324205  -102.659935  4.546391  0
  -4.107368  -102.637810  5.588718  0
  etc.
```

To find the node number for this co-ordinate, we first need to number the lines in the file. Then we can sort by the y-position (now it is field number 3).
This will show all nodes:

```
 cat -n lh.white.asc | sort -n --key=3 -| more
```

To find only the posterior node, we can use the head command

```
 cat -n lh.white.asc | sort -n --key=3 - | more | head -1
```

returns

```
     41  -4.324205  -102.659935  4.546391  0
```

The first number, 41, is the line number in the file with the smallest y-value. The numbering is slightly off. If you subtract three, this will give you the actual node number. i.e.

```
 node number = 38.
```

Three must be subtracted because the first two lines of the surface file are header information, and then SUMA node numbering begins at "0" (unlike UNIX line numbering, which begins at 1). Bonus points if you construct a UNIX command to subtract three automatically!

Use the SUMA Surface Controller to verify that the chosen node number is the most posterior, and has the specified x,y,z co-ordinates.

Node that the most posterior node will vary slightly depending on which version of the surface (white, pial, inflated) that you examine. It should probably be the same surface used for other computations, such as mapping the electrodes to.
