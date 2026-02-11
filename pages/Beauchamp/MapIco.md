---
layout: default
title: "MapIco"
parent: Beauchamp
---
# MapIco


Return to [Notes on Cortical Surface Averages](SurfaceAveraging.md "Beauchamp:SurfaceAveraging")

## Old and New

In March 2017, the AFNI team discovered a bug in the MapIcosahedron program. Here is a comparison of group average results with the old and new (fixed) versions.
If you have old surface averages and would like to fix them, you can use a script like this to create new surfaces, then re-run your surface averaging processing stream.

```
 set ss = (MS MT MU MW MX MY MZ NA NB NC ND NE NF NG NH NU NV NW OA )
 foreach s ( $ss )
 set sd = /Volumes/data/BCM/{$s}/fs/SUMA
 cd $sd  
 pwd 
 mkdir oldstd
 mv *141* *60* oldstd/
 set sid = fs
 foreach size (60 141)
   foreach hem ( lh rh )
      MapIcosahedron -spec ${sid}_$hem.spec -ld $size   \
           -dset_map $hem.thickness.gii.dset            \
           -dset_map $hem.curv.gii.dset                 \
           -dset_map $hem.sulc.gii.dset                 \
           -prefix std.$size.
   end
   inspec -LRmerge std.$size.${sid}_lh.spec std.$size.${sid}_rh.spec \
          -prefix std.$size.${sid}_both.spec 
end
end
```

## Anatomical Data

New

```
![](../../attachments/MapIco/NewFuncs.Anats.0000.jpg)  ![](../../attachments/MapIco/NewFuncs.Anats.0001.jpg)  ![](../../attachments/MapIco/NewFuncs.Anats.0003.jpg) ![](../../attachments/MapIco/NewFuncs.Anats.0002.jpg)
```

Old

```
 ![](../../attachments/MapIco/OldFuncs.Anats.0000.jpg)  ![](../../attachments/MapIco/OldFuncs.Anats.0001.jpg) ![](../../attachments/MapIco/OldFuncs.Anats.0002.jpg) ![](../../attachments/MapIco/OldFuncs.Anats.0003.jpg)
```

## Functional Data

Functional data of the Mouth vs. Eye contrast mapped to the average surface. It is hard to quantify the difference, but one way is to compare the maximum statistical values; with better intersubject alignment, these would presumably increase.

1. NEW: Max t-value for Mouth: 9.3 Eye:10.1 Eye vs Mouth: 5.6
2. OLD: Max t-value for Mouth: 7.9 Eye:8.8 Eye vs Mouth: 5.8

data from Zhu LL, Beauchamp MS. Mouth and Voice: A Relationship between Visual and Auditory Preference in the Human Superior Temporal Sulcus. Journal of Neuroscience 8 March 2017, 37 (10) 2697-2708; DOI: <https://doi.org/10.1523/JNEUROSCI.2914-16.2017>. [Click here to download the PDF.](../../attachments/MapIco/Zhu_Beauchamp_JNS_2017.pdf "Zhu Beauchamp JNS 2017.pdf") Surface averages were not used in this paper so the bug did not affect the published results.

New

```
![](../../attachments/MapIco/NewFuncs.0000.jpg) ![](../../attachments/MapIco/NewFuncs.0001.jpg)
```

Old

```
![](../../attachments/MapIco/OldFuncs.0000.jpg) ![](../../attachments/MapIco/OldFuncs.0001.jpg)
```
