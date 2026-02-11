# FSAverageReadme

> **Navigation:** [Home](index.md) • [Publications](Publications.md) • [Resources](DataSharing.md)

This is the FreeSurfer group average subject.

DO NOT EDIT OR MODIFY THIS SUBJECT!

The surfaces were constructed from 40 subjects resmapled to a 7th
order icosahedron using make\_average\_subject. See
scripts/make\_average\_{surface,volume}.log for more info. It is
similar to the old "average7", except that average7 did not retain
information about the surface areas of the original subjects, so
it was difficult to relate the metric properties (eg, cluster surface
area) of average7 to that of a typical subject.

The annotations in the label dir are those from the probabilistic
atlases, ie, curvature.buckner40.filled.desikan\_killiany.gcs for
?h.aparc.annot, and atlas2005\_simple.gcs for ?h.aparc.a2005s. The
individual labels for each of these were extracted and placed in
the label directory:

cd label
mri\_annotation2label --subject fsaverage --hemi lh \

```
 --annotation aparc \
 --table aparc.annot.ctab \
 --outdir .
```

mri\_annotation2label --subject fsaverage --hemi rh \

```
 --annotation aparc \
 --table aparc.annot.ctab \
 --outdir .
```

mri\_annotation2label --subject fsaverage --hemi lh \

```
 --annotation aparc.a2005s \
 --table aparc.atlas2005_simple.ctab \
 --outdir .
```

mri\_annotation2label --subject fsaverage --hemi rh \

```
 --annotation aparc.a2005s \
 --table aparc.atlas2005_simple.ctab \
 --outdir .
```

The volumes were derived from the MNI305 (www.bic.mni.mcgill.ca). See
also the mni305.cor.readme file. The MNI305 is the target for linear
talairaching (more on this below). orig.mgz and T1.mgz are
linked to mni305.cor.mgz. brainmask.mgz is linked to
mni305.mask.cor.mgz. brain.mgz was created with mri\_mask. The full
volume creation process is:

cp $FREESURFER\_HOME/average/mni305.cor.mgz .
cp $FREESURFER\_HOME/average/mni305.mask.cor.mgz .
cp $FREESURFER\_HOME/average/mni305.cor.readme .
mri\_add\_xform\_to\_header -c auto mni305.cor.mgz
mri\_add\_xform\_to\_header -c auto mni305.mask.cor.mgz
ln -s mni305.cor.mgz orig.mgz
ln -s mni305.cor.mgz T1.mgz
ln -s mni305.mask.cor.mgz brainmask.mgz
mri\_mask T1.mgz brainmask.mgz brain.mgz

The volumes orig.group.mgz, T1.group.mgz, and brain.group.mgz were
those originally produced by make\_average\_subject.

As mentioned above, the MNI305 is the target for linear
talairaching. All volumes and surfaces are aligned to this brain.

This has several implications:

```
 1. The mri/talairach.xfm is identity
 2. tkregister2 --fstal --s fsaverage will bring up the same volume
    for movable and target.
 3. The surfaces coordinates are in talairach space, so they align
    with the MNI305 volume, so "tkmedit fsaverage T1.mgz lh.white",
    shows the surfaces overlaid properly on the brain.
 4. The c_{ras} for all volumes is 0. If you don't know what this
    means, consider yourself lucky.
```
