---
layout: default
title: "InitialAutoVOIforIT"
parent: Beauchamp
---
# InitialAutoVOIforIT


DTI Query allows any number of cuboid VOIs to be used isolate fiber pathways

Automatically specifying the center and extents of these VOIs is useful when you have lots of points derived from stimulation mapping, blobs from fMRI activation, or electrode locations.

This part of the wiki shows you how to take multiple points or blobs and automatically generate cuboid VOIs in DTI Query.

VOIs in DTI Query are defined in a state file (.qst). The following examples will show how to generate state files for DTI Query which can then be loaded to automatically select VOIs. Two different MATLAB functions are defined below for use depending on the type of VOI that you wish to create.

## Generating VOIs from stimulation mapping or electrode locations

VOIs from either stimulation mapping or electrode locations are generated from a predefined ".1D" file with the following format:

```
#spheres
x y z 1 1 1 1 1.5 2 
x y z 1 1 1 1 1.5 2
```

where x, y, and z are coordinates of a particular stimulation site or grid electrode. It is important that there are no extra lines of white space at the end of the file or the MATLAB function will not function properly and all of your VOIs might not be generated.

```
Cortical surface model displayed in SUMA with 1D file overlaid depicting the locations of stimulation:
![](../../attachments/InitialAutoVOIforIT/Sumapoints.jpg)
```

To generate the .qst state file you will need to start MATLAB and call the **read\_1DtoQST** function

```
read_1DtoQST(fname,patientnumber,pdb_fname)
```

Where fname is the .1D file name, patientnumber is patient identifier, and pdb\_fname is the precomputed fiber pathways.
An example of this would be:

```
read_1DtoQST('TA313_Hypotheses.1D','TA313','TA313_orig_precomputed.pdb')
```

The read1DtoQST function will output a .qst state file with name patientnumer\_VOI.qst. In the above example the state file generated would be TA313\_VOI.qst. The file may take several minutes to generate depending on the number of pathways defined in pdb file.

To display the automatically generated VOIs you first need to start DTI Query and load a background image. Next you must Load Pathways, these have to be the same pathways used to generate the state file. In the above example it would be TA313\_orig\_precomputed.pdb. Finally you will be able to load a state file to begin exploring your automatically created VOIs.

The VOIs that are generated will have centers located at x,y, and z as defined by the 1D file and will have dimensions of 10mm x 10mm x 10mm.

```
DTI Query displaying automatically generated VOIs from a 1D file:
![](../../attachments/InitialAutoVOIforIT/Dtivoi.jpg)
```

```
Note: The read_1DtoQST function is in /Volumes/data9/matlab/ORStim_functions you may have to add this to your matlab path before the function will work.
```

## Generating VOIs from fMRI activation sites
