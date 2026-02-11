# Creating a Surface Model and Electrode Localization (by Muge Ozker Sertel)

> **Navigation:** [Home](index.md) • [Publications](Publications.md) • [Resources](DataSharing.md)

|  |  |
| --- | --- |
|  | Beauchamp Lab wiki |

- [Home](index.md "Beauchamp")
- [Publications](Publications.md "Beauchamp:Publications")
- [Resources](DataSharing.md "Beauchamp:DataSharing")

Also see: [Beauchamp:Electrode Localization and Naming](Electrode_Localization_and_Naming.md "Beauchamp:Electrode Localization and Naming")

**Step 1:** Get the MR and CT scans of the patient from SLEH Film Library

**Step 2:** Create a patient folder on the server:

i.e. /Volumes/data/UT/YAR (YAR is the patient ID in this example case)

Copy in MR and CT scans with OsiriX, then export the images to the patient's folder. Choose Hierarchical and Decompress DICOMs options during the export.
Take out the spaces in MR and CT folder names. The folder names should look like as follows:

```
/Volumes/data/UT/YAR/LastName_FirstName_MR/MRBRAINWITHOUTCONTRAST
/Volumes/data/UT/YAR//LastName_FirstName_CT/CTBRAINWITHOUTCONTRAST
```

**Step 3:** Process anatomical MR data:

```
set ec = YAR 
set session = /Volumes/data/UT/YAR/afni
```

This way the processed anatomical files will be saved in the afni folder under the patient's directory.

There should be two different T1 scan folders in the MRBRAINWITHOUTCONTRAST folder. These folders are usually named T1\_TFE\_NSA01 (include images from 1st T1 scan) and T1\_TFE\_NSA02 (include images from 2nd T1 scan). We use the images in these folders.

- Create 3D datasets for use with AFNI from these 2D MR image files

For the 1st T1:

```
cd /Volumes/data/UT/YAR/LastName_FirstName_MR/MRBRAINWITHOUTCONTRAST/T1_TFE_NSA01
to3d -session $session -prefix {$ec}anatr1 IM-0011-0*
```

For the 2nd T1:

```
cd /Volumes/data/UT/YAR/LastName_FirstName_MR/MRBRAINWITHOUTCONTRAST/T1_TFE_NSA02
to3d -session $session -prefix {$ec}anatr2 IM-0012-0*
```

- Align the 1st T1 to the 2nd T1

This takes approximately 7 minutes.

```
cd /Volumes/data/UT/YAR/afni 
3dAllineate -base YARanatr2+orig -source YARanatr1+orig -prefix ${ec}anatr1_1RegTo2 -verb -warp shift_rotate -cost mi -automask -1Dfile ${ec}anatr2toanatr1
```

- Average the two aligned T1s into one dataset

This takes approximately 30 seconds.

```
3dmerge -gnzmean -nscale -prefix ${ec}anatavg ${ec}anatr2+orig  ${ec}anatr1_1RegTo2+orig
```

**Step 4:** Make the surface model:

Follow the steps listed here:
[Cortical Surface models overview](CorticalSurfaceOverview.md "Beauchamp:CorticalSurfaceOverview")
Include the optional step (listed in the above page) to create a brain boundary file:

```
 recon-all -s fs -localGI
```

- Create skull stripped anatomy to render the electrodes with

```
cd /Volumes/data/UT/YAR/afni
set ec = YAR
3dSkullStrip -input {$ec}anatavg+orig -prefix {$ec}anatavgSS
```

- Transform the skull stripped anatomical image to match a template in TLRC space

This takes approximately 3 minutes.

```
@auto_tlrc -base TT_N27+tlrc -no_ss -input {$ec}anatavgSS+orig
```

**Step 5:** Process CT data:

- Create 3D datasets for use with AFNI from these 2D CT image files

```
set ec = YAR
set session = /Volumes/data/UT/YAR/afni
cd /Volumes/data/UT/YAR/LastName_FirstName_CT/CTBRAINWITHOUTCONTRAST/Axial__Supine_Scan_3 
to3d -session $session -prefix {$ec}_CT IM-0001-0*
```

**Step 6:** Align the CT to the T1:

In this step use the 2nd T1 (YARanatr2+orig) as the base.

```
3dAllineate -base YARanatr2+orig -source {$ec}_CT+orig -cmass -prefix {$ec}CT_REGtoanat2 -verb -warp shift_rotate -cost mutualinfo -1Dfile {$ec}CT_REGtoanat2
```

- In afni display YARanatr2 as underlay and YARCT\_REGtoanat2 as overlay to check if the alignment worked well.

**Step 7:** Locate the electrodes on the brain:

- Tag the Electrodes

- Load AFNI and SUMA together

```
cd /Volumes/data/UT/YAR
set ec = YAR
./@ec
```

- In afni set underlay to fs\_SurfVol\_Alnd\_Exp+orig and overlay to YARCT\_REGtoanat2

Setting the background to overlay to see just see the CT scan sometimes makes it easier to see the electrodes. 'u' key can be used to switch the background between underlay and overlay.

- Go to Define Datamode --> Plugins --> Edit Tagset

- Set Dataset as fs\_SurfVol\_Alnd\_Exp

- Name Tag File as YARelectrodetags.tag

- Find the densest view of an electrode, make sure it's centered in all views (axial, saggital and coronal) and press 'Set' and then 'Save'

- Press 'Write' once all the electrodes are tagged. This will write the YARelectrodetags.tag file and save it in the afni folder.

- Open the tag file YARelectrodes.tag in Excel and re-order the electrode tags in the order of the channel numbers

- Make a copy of YARelectrodes.tag with the file name extension .1D

```
cp {$ec}electrodetags.tag {$ec}electrodetags.1D
```

- Open in {$ec}electrodetags.1D in Excel and edit the file so that it only has the 3 columns of x,y,z

- Project the tagged electrodes onto the closest node on the pial-outer-smoothed surface

```
SurfaceMetrics -spec /Volumes/data/UT/YAR/fs/SUMA/fs_both.spec -sv fs_SurfVol_Alnd_Exp+orig -surf_A lh.pial-outer-smoothed.gii -closest_node YARelectrodetags.1D -prefix {$ec}ClosestNodes_pialenvelope
```

- Open YARClosestNodes\_pialenvelope.1D.dset in Excel and copy 3 columns of Xn, Yn, Zn coordinates. Paste Xn, Yn, Zn coordinates in a new Excel sheet and enter #spheres in the first cell of the document and format it as follows:

Xn Yn Zn 1 1 1 1 1.5 2.2

Electrode color is black for [0 0 0] and white for [1 1 1]. Electrode size is 1.5 for regular, 0.5 for mini electrodes.

- Save it as YARClosestProjected.txt and copy is as a .do file

```
cp {$ec}ClosestProjected.txt {$ec}ClosestProjected.do
```

- Display the projected electrodes on the brain surface

- Open "Select Displayable Objects File" shell by pressing "Comman & Control & s" on the keyboard. Set filter in shell to \*do and select the appropriate .do file.

**HINT**s to make electrode tagging easier:

**1)** Display electrodes on the brain surfer in SUMA window

- Load AFNI and SUMA together by the ./@ec command

- Set underlay to fs\_SurfVol\_Alnd\_Exp+orig and overlay to YARCT\_REGtoanat2

- Increase the threshold so that in the SUMA window, electrodes look as colorful spots on the gray brain surface. Right clicking on these colorful spots on the SUMA window will take the Xhairs to the corresponding electrode position in the AFNI display window.

**2)** Display electrodes on the brain by using AFNI C Renderer

- Go to Define Datamode --> Plugins --> Render Dataset

- Choose YARanatSS as underlay and YARCT\_REGtoanat2 as overlay

- Select See Overlay and DynaDraw. Increase the threshold so that everthing on the brain surface doesn't look green. Hit automate to generate the surface image with electrodes on it

- Play with the Roll, Pitch and Raw values to see the brain surface from different views

- Select See Xhairs. This way the Xhairs in the rendering window will move together with the Xhairs in the AFNIdisplay window

**Step 8:** Label the electrodes:

- Go to Define Datamode --> Plugins --> Edit Tagset

- Load the electrode tags with the same dataset setting (fs\_SurfVol\_Alnd\_Exp)

- Enter a Tag Label for each electrode and press 'Relabel' and 'Save'

- Press 'Write' after relabeling all the electrodes

- In Matlab, generate a **generateOBJSetting.m** script for the subject with the channel list.

- Generate a YAR\_Label\_Input.txt file with the closest projected x,y,x coordinates and run the **read\_write\_elec\_labels.m** script.

- Copy the generated YAR\_ElectrodeLabels.niml.do file into the patient's afni folder and paste the following line at the beginning of the file:

```
<nido_head													
coord_type	=	mobile											
default_SO_label	=	CURRENT		
bond	=	none	
/>	
```

Electrode labels can now be displayed on the brain surface next to the corresponding electrodes. In SUMA window, "Select Displayable Objects File" shell by pressing "Command & Control & s" on the keyboard. Set filter in shell to \*do and select the appropriate .do files that correspond to the electrode locations (i.e. YARClosestProjected.do) and electrode labels (i.e. YAR\_ElectrodeLabels.niml.do).
