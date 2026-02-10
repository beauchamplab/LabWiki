# GroupAna

> **Navigation:** [Home](index.md) | [Publications](Publications.md) | [Resources](DataSharing.md)

Using GroupAna.m to do ANOVA's with different group sizes
<http://afni.nimh.nih.gov/sscc/gangc/Interface.html/>

1. Make sure you have the most updated version (~2005)
<http://afni.nimh.nih.gov/afni/community/board/read.php?f=1&i=37940&t=37940#reply_37940>

2. Need individual subBRIKs in individual files (you can't just reference a single subBRIK in a bigger dataset)

```
    foreach ec  (CAM CAS CAV CBA CBB CBD CBE CBI CBJ CBK CBL CBM CBN CBO CBP CBQ CBU)
       3dbucket -prefix {$ec}_McG {$ec}bl6+tlrc'[2]'
       3dbucket -prefix {$ec}_InC {$ec}bl6+tlrc'[5]'
       3dbucket -prefix {$ec}_Cong {$ec}bl6+tlrc'[8]'
    end
```

3. Run from whatever folder has all of the Matlab files in it (/Applications/abin\_old/matlab), since GroupAna.m calls many of the other Matlab functions.

Reference datafiles from the server
( for example, /Volumes/data1/UT/ChildMcGurk/CAM\_McG+tlrc.BRIK)

Example of commands

%-- 4/22/11 9:59 AM --%

GroupAna
0
3
3
0
1

PercGroup
2
NonPerc
Perc

StimulusType
3
McG
Inc
Cong

Subject
7
CAM
CBM
CBP
CAV
CBK
CBB
CBQ
10
CBD
CAS
CBE
CBO
CBU
CBI
CBA
CBJ
CBL
CBN
1
1

/Volumes/data1/UT/ChildMcGurk/CAM\_McG+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBM\_McG+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBP\_McG+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CAV\_McG+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBK\_McG+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBB\_McG+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBQ\_McG+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CAM\_InC+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBM\_InC+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBP\_InC+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CAV\_InC+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBK\_InC+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBB\_InC+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBQ\_InC+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CAM\_Cong+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBM\_Cong+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBP\_Cong+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CAV\_Cong+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBK\_Cong+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBB\_Cong+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBQ\_Cong+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBD\_McG+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CAS\_McG+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBE\_McG+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBO\_McG+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBU\_McG+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBI\_McG+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBA\_McG+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBJ\_McG+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBL\_McG+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBN\_McG+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBD\_InC+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CAS\_InC+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBE\_InC+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBO\_InC+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBU\_InC+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBI\_InC+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBA\_InC+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBJ\_InC+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBL\_InC+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBN\_InC+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBD\_Cong+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CAS\_Cong+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBE\_Cong+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBO\_Cong+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBU\_Cong+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBI\_Cong+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBA\_Cong+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBJ\_Cong+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBL\_Cong+tlrc.BRIK
/Volumes/data1/UT/ChildMcGurk/CBN\_Cong+tlrc.BRIK
GroupAna\_Child\_6mm
1
3

Perc-NonPerc
2
100
-1
200
1

McG-InC
2
010
1
020
-1

McG-Cong
2
010
1
030
-1
1

PercMcG-NonPercMcG
2
110
-1
210
1
0

4. Add Full F stat (make sure datum type is float!!)

```
    3dbucket -glueto GroupAna_Child_6mm+tlrc -fbuc NewFullF_17_float+tlrc'[0]'
    3drefit -sublabel 18 NewFullF GroupAna_Child_6mm+tlrc
```
