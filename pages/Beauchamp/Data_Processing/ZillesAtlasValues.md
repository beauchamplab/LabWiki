---
layout: default
title: "ZillesAtlasValues"
parent: Data Processing and Analysis
grand_parent: Beauchamp
---
# ZillesAtlasValues


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

## Zilles Atlas Values

Note that these values can be verified by examining the Anatomy Toolbox values in AFNI or SPM.
A comprehensive list can be generated with the AFNI command

```
 whereami -show_atlas_code
```

```
 AIPS_IP1 = 185 
 AIPS_IP2 = 115 
 Amygdala_CM = 120 
 Amygdala_LB = 215 
 Amygdata_SF = 150 
 BA_44 = 160 
 BA_45 = 110 
 Hippocampus_CA = 100 
 Hippocampus_EC = 135 
 Hippocampus_FD = 170 
 Hippocampus_HATA = 200 
 Hippocampus_SUB = 240 
 PAC_TE10 = 130 
 PAC_TE11 = 195 
 PAC_TE12 = 230 
 PMC_4a = 125 
 PMC_4p = 175 
 premotor_6 = 210 
 PSC_1 = 180 
 PSC_2 = 225 
 PSC_3a = 220 
 PSC_3b = 140 
 SII_OP1 = 105 
 SII_OP2 = 205 
 SII_OP3 = 155 
 SII_OP4 = 235 
 visual_V1 = 145 
 visual_V2 = 190
 visual_v5 = 165
```

Other atlases are also available, such as the Talairach demon and FreeSurfer parcellation.
The integer assigned to an area can change from version to a version of an atlas (e.g. v1.3 to v1.5 of the Zilles atlas) so check your work carefully!
