# ActivityMaps

> **Navigation:** [Home](index.md) • [Publications](Publications.md) • [Resources](DataSharing.md)

Make an activity map to show the percent gamma change on the brain surface:

- Extract percent gamma change values from Matlab. It should be a single column each row representing the average gamma activity recorded from an electrode. Call this file 'YAR\_Gamma.txt' (YAR is an example subject ID here).

- In the afni folder of the corresponding subject ,open the ClosestProjected.do file. This file contains the electrode coordinates on the brain surface. Copy the coordinate values in a separate text file and call this file 'YAR\_Elec.txt'.

- Concatenate the electrode coordinate values and gamma values such that the first 3 colums are the xyz coordinates and the forth column is the gamma values:

Both the YAR\_Elec.tx and the YAR\_Gamma.txt files should be in the afni folder of the subject.

```
cd afni
1dcat YAR_Elec.txt YAR_Gamma.txt> temp1.txt
```

Now temp1.txt contains the coordinate values for each electrode together with their gamma activity values.

- Dump the gamma values onto the electrodes:

Let's assume we have 32 electrodes

```
set electrode = 0
while ($electrode < 32)
1dcat temp1.txt'{'{$electrode}'}' > temp2.txt
3dUndump -prefix elec{$electrode} -datum float -master fs_SurfVol_Alnd_Exp+orig.BRIK -xyz -srad 5 temp2.txt
@ electrode++
echo $electrode
end
```

- Blur the gamma activity:

```
3dmerge -overwrite -prefix Gamma_Blurred -1blur_fwhm 1 -gnzmean elec*+orig.HEAD
```

All the electrodes will be combined in a single BRIK file called 'Gamma\_Blurred+orig.BRIK.

- Show the activity map on the brain surface

- First load AFNI and SUMA together

```
cd ..
./@ec
```

- Click on the SUMA window and press Control+Command+s. Choose ClosestProjected.do to display the electrodes on the brain surface

- In the AFNI window set Underlay as fs\_SurfVol\_Alnd\_Exp and Overlay as Gamma\_Blurred
