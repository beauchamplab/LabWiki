# img pipe

> **Navigation:** [Home](index.md) | [Publications](Publications.md) | [Resources](DataSharing.md)

|  |  |
| --- | --- |
|  | Beauchamp Lab wiki |

- [Home](index.md "Beauchamp")
- [Publications](Publications.md "Beauchamp:Publications")
- [Resources](DataSharing.md "Beauchamp:DataSharing")

|  |
| --- |
| Notes from Qi Liu:  This package generates surface pial and subcortical structure surface, and electrodes coordinate to be the .mat file in folder Meshes/, which is MATLAB readable and might fit Brett's requirement. I have the note .txt file in subjects folder under /lab/Qi/img\_pipe/YAI( and Sub1) with all the command history. You labmates could easily follow the notes and get electrodes coordinate with .mat file in folder elecs/. Your lab could also convert it to be compatible 1d file and export into SUMA. Here are two tricky points when preparing CT data, so your lab doesn't have to solve the problems I have met. 1. the CT.nii should be converted with mri\_convert from FREESURFER, not 3dcopy of AFNI, as they treat nan value in a different format. This is why you met the problem with patient.mark\_electrodes. 2. the original CT.nii before registration should have the same spatial resolution as T1.nii. |
