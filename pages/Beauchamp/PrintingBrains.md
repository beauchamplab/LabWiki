---
layout: default
title: "PrintingBrains"
parent: Beauchamp
---
# PrintingBrains


|  |  |
| --- | --- |
|  | Beauchamp Lab wiki |

- [Home](index.md "Beauchamp")
- [Publications](Publications.md "Beauchamp:Publications")
- [Resources](DataSharing.md "Beauchamp:DataSharing")

## Notes on 3D Printing Brains

The basic process is very simple. Scan the subject and create the cortical surface model, then convert to .STL format with mris\_convert e.g. for the LH pial surface

```
 mris_convert lh.pial lh.pial.stl
```

Then send to .STL format to a 3D printer. Billy Gill at UT has a very nice one, prices was $750 for a brain and some brainstems. The BioE core at BCM is buying one.
There are some other steps that can printing easier. This website has some suggestions: <http://imgur.com/a/3mFsX>
They recommend downsampling the .STL file with MeshLab

```
 http://meshlab.sourceforge.net/
 http://downloads.sourceforge.net/project/meshlab/latest
```

to <20K face sets.

```
 Filters -> Remeshing, Simplification, and Reconstruction ->  Quadratic Edge Collapse Decimation
```

Then Export Mesh to a new file.
Some more advanced steps are needed if you want to print out only part of the brain, like the STS.
Load the brain in SUMA, then load the parcellation dataset (e.g. lh.aparc.a2009s.annot.niml).
Determine the Value or Label for the nodes that you want (e.g. wm\_lh\_S\_temporal\_sup (I,T,B)node label=3988703; col=0.699, 0.690, 0.188)
