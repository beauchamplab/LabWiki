> **Navigation:** [Home](index.md) • [Install](Install.md) • [Help](Help.md)

# Imaging Data Formats

|  |  |
| --- | --- |
| [RAVE logo](../../attachments/Imaging_Data_Formats/RAVE_Logo_new.jpg "RAVE logo") | **R**eproducible **A**nalysis and **V**isualization of i**E**EG   ***RAVE*** |

[Detailed tutorial on importing FreeSurfer data.](Tutorial_ImportFS.md "RAVE:Tutorial ImportFS")

### Import volumetric MRI data and cortical surface models

RAVE imports MRI volumetric data and cortical surface models that have been processed by FreeSurfer. [See the FreeSurfer website for complete information](https://surfer.nmr.mgh.harvard.edu/fswiki). For additional help, see the [Beauchamp Lab wiki](../Beauchamp/CorticalSurfaceOverview.md "Beauchamp:CorticalSurfaceOverview") (ignore instructions for converting FreeSurfer surfaces for AFNI/SUMA; this is not required for RAVE.) Copy the FreeSurfer output folder into the RAVE subject folder, e.g.

```
 rave_data/data_dir/congruency/YAB/rave/fs
```

RAVE will read all of the files that are needed directly from this directory.

##### Special Cases

Note that it is not required to have any MRI data or a cortical surface model, although RAVE works best if these are available.

##### No cortical surface model

RAVE reads volumetric MRI data from the file

```
 fs/mri/brain.finalsurfs.mgz
```

##### Partial cortical surface model

If no cortical surface model is found, RAVE will display only the volumetric MRI data. RAVE requires that both the left hemisphere and right hemisphere surface files be present, in either native FreeSurfer format, ASCII format, or GIFTI format. RAVE will attempt to read fs/surf/lh.pial or (if this file is not found) fs/surf/lh.pial.asc or (if this file is not found) fs/surf/lh.pial.gii .

In some cases, FreeSurfer may reconstruct only one hemisphere; in this case a work-around is to create a "fake" model of the other hemisphere. For instance, if the right hemisphere reconstruction failed, use a text editor to create the file

```
 fs/surf/rh.pial.asc
```

containing six lines:

```
 3 1
 0 0 0
 0 0 0
 0 0 0
 0 1 2
 {blank line}
```

The first line tells how many vertices and how many faces; line 2-4 create fake vertices at the origin; line 5 links these vertices. The last line of the file must be blank.

---

*[Return to preprocessing overview](ravepreprocess.md "RAVE:ravepreprocess")*
