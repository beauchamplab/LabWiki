---
layout: default
title: "ALICE"
parent: Beauchamp
---
# ALICE


This page shows the steps used by the ALICE package to localize electrodes. These steps are called from within a Matlab GUI.

The GUI has three steps.
Here is the log file from the first step (an edited version of /Volumes/data/UT/YBK/ALICE/log\_info/Step1\_log.txt with comments added )

**STEP 1: MRI and CT Alignment**

```
 MRI scan selected: /Users/fosterlab/Documents/MATLAB/CTMR/DATA/YBK/ALICE/data/MRI/YBK_T1.nii
```

```
 FS segmentation selected: /Users/fosterlab/Documents/MATLAB/CTMR/DATA/YBK/ALICE/data/FreeSurfer/t1_class.nii
```

This file was originally called YBK\_fs\_ribbon\_rh\_class.nii (renamed version of rh.ribbon.nii)

```
 CT scan selected: /Users/fosterlab/Documents/MATLAB/CTMR/DATA/YBK/ALICE/data/CT/CT_highresRAI.nii
```

This file was originally called YBK\_CT.nii

```
  Aligning CT to MRI... This might take several minutes. Please wait...
  tcsh -x alignCTtoT1_shft_res.csh -CT_path CT_highresRAI.nii -T1_path../MRI/YBK_T1.nii
```

This shell script contains the following steps:

```
 @Align_Centers -base $t1  -dset $ct
 3dresample -input CT_highresRAI_shft.nii -prefix CT_highresRAI_res_shft.nii  -master $t1  -dxyz 1 1 1 -rmode NN
 align_epi_anat.py -dset1 $t1 -dset2  CT_highresRAI_res_shft.nii -dset1_strip None -dset2_strip None -dset2to1 -suffix _al  -feature_size 1  -overwrite -cost nmi -giant_move -rigid_body > status.txt
 3dcopy  CT_highresRAI_res_shft_al+orig CT_highresRAI_res_al.nii
 3dcopy $t1 ./temp_ANAT.nii
 afni -com "SWITCH_UNDERLAY temp_ANAT.nii" -com "SWITCH_OVERLAY CT_highresRAI_res_al.nii"
```

**STEP 2: Clustering and Electrode Selection**

The log file from the second step does not contain the called commands, the list below has been extracted from the Matlab file ctmrGUI.m
Three parameters are set in the GUI: electrode max intensity, electrode volume, inter electrode space.
For subject YBK, the max intensity that worked best was 3500. Electrode volume was set to “2”, space was set to “1”.
The GUI then calls this script:

```
([tcsh -x 3dclustering.csh -CT_path ../CT/CT_highresRAI.nii -radius ' num2str(obj.settings.R) ' -interelectrode_space ' num2str(obj.settings.IS) ' -clip_value ' num2str(obj.settings.CV)]);
```

This script contains the following commands:

```
 3dclust -savemask 3dclusters_r${r}_is${is}_thr${cv}.nii -overwrite -1Dformat -1clip $cv $is $r $ct  > clst.1D 
 # make sure the clusters all show up in afni with distinct colors
 3drefit -cmap INT_CMAP 3dclusters_r${r}_is${is}_thr${cv}.nii 
 # now resample the clusters, erode, dilate and cluster again
 # this helps separate the clusters that overlap
 3dresample -prefix temp_clusts_rs0.5 -overwrite -rmode NN -dxyz 0.5 0.5 0.5 -inset 3dclusters_r${r}_is${is}_thr${cv}.nii
 3dmask_tool -dilate_inputs -1 +2 -prefix temp_clusts_rs0.5_de2 -overwrite -inputs temp_clusts_rs0.5+orig
 3dclust -savemask 3dclusters_r${r}_is${is}_thr${cv}.nii -overwrite -1Dformat -1clip $cv $is $r temp_clusts_rs0.5_de2+orig > clst.1D 
 3drefit -cmap INT_CMAP 3dclusters_r${r}_is${is}_thr${cv}.nii 
 rm temp_clusts*.HEAD temp_clusts*.BRIK*
 IsoSurface -isorois+dsets -mergerois+dset -autocrop -o_gii 3dclusters_r${r}_is${is}_thr${cv}.gii -input 3dclusters_r${r}_is${is}_thr${cv}.nii  
 echo "Clustered dataset saved as 3dclusters_r${r}_is${is}_thr${cv}.nii"
 echo "Table of coordinates saved as clst.1D"
```

Afni and SUMA were opened using this script:

```
 (['tcsh -x open_afni_suma.csh -CT_path ../CT/CT_highresRAI.nii -clust_set ' clust_set ' -clust_surf ' clust_surf ], '-echo')
```

The script contains the following commands:

```
 # script to write out electrode positions
 # assumes one has previously run this previous script and created the roi surfaces for all the electrodes
 # with these commands
 # tcsh @3dclustering -CT_path CT.nii -radius 4 -interelectrode_space 3 -clip_value 2999
 # IsoSurface -isorois+dsets -mergerois+dset -autocrop -o_gii 3dclusters.gii -input 3dclusters_r?_is?.nii
 set PIF = DriveAfniElectrodes    #A string identifying programs launched by this script
 @Quiet_Talkers -pif $PIF   #Quiet previously launched programs
 #Get a free line and tag programs from this script
 set NPB = "-npb `afni -available_npb_quiet` -pif $PIF -echo_edu" 
 echo $NPB > ecognpb.txt
 set surfcoords = "surf_xyz.1D"  # record the electrode positions in a text file - this one gets the position at the surface
 #set surfcoords_i = "surf_ixyz.1D"  # record the electrode positions in a text file - this one gets the position at surface with index
 set sumasurf = lastsurfout.txt 
 set ct = "CT+orig"
 set clust_surf = "3dclusters.gii"
 set clustset = 
 ####### START new code for el cluster shading v2.0 (MPBranco 300617)###########################
 set clust_surf_base = `basename -s .gii $clust_surf`
 set clust_niml_set = ${clust_surf_base}.niml.dset
 rm lastsurfout.txt temproilist.txt
 # make a temporary copy of the coloring dataset to recolor as we go
 set nlabels = `3dinfo -labeltable $clust_niml_set | grep ni_dimen | awk -F\" '{print $2}'`
 @ nlabels ++
 # copy just the labels from the niml dset
 3dinfo -labeltable $clust_niml_set | tail -$nlabels | grep -v VALUE_LABEL_DTABLE \
 | tr -d \" > temp_labels.txt
 MakeColorMap -std ROI_i256 |tail -256 > roi256.1D
 # now create a proper SUMA compatible colormap by combining the two files
 #  index label RGBA
 @ nlabels --
 rm tempcmap.txt
 foreach li (`count -digits 1 1 $nlabels`)
 set ind_label = `sed "${li}q;d" temp_labels.txt`
 set rgb = `sed "${li}q;d" roi256.1D`
 # put them all together (RGB are fractional values, Alpha=1)
 # index label R G B A
 # 1 electrode_1 0.1 0.4 0.02 1
 echo $ind_label $rgb 1 >> tempcmap.txt
 end
 # create a non-colored copy of the dataset - just nodes and cluster indices
 ConvertDset -overwrite -input $clust_niml_set -dset_labels 'R' -o temp_marked_clusters.1D
 # make color map used below and updated too
 MakeColorMap -usercolutfile tempcmap.txt \
 -suma_cmap tempcmap -overwrite >& /dev/null
 #      -sdset temp_marked_clusters.niml.dset \
 ####### END of new code for el cluster shading v2.0###########################
 # if cluster dataset was not specified, try to find one
 if ($clustset == ) then
 set clustsets = (3dclusters_r?_is?.nii)
 set clustset = $clustsets[0]
 endif
 afni $NPB -niml -yesplugouts -dset $ct $clustset  >& ./afniout.log &
 sleep 1
 # delete copy of previous surface coordinates and region if it exists
 if -e $surfcoords then
 mv $surfcoords $surfcoords.old
 #  mv $surfcoords_i $surfcoords_i.old
 endif
 # coordinates sent to text file by AFNI with plugout xyz
 setenv AFNI_OUTPLUG $surfcoords
 # text output from suma driven command with cluster index with surface name
 setenv SUMA_OUTPLUG  $sumasurf
 suma $NPB -DSUMA_AllowDsetReplacement=YES -i $clust_surf -sv $ct >& ./sumaout.log  & #####edited for v2.0
 DriveSuma $NPB -com surf_cont -view_object_cont y
 # We need a way to click on the electrodes in the clinical order and 
 # find the correspondent center of mass coordinates in clst.1D file. 
 # The optimal output would be a txt file with four columns, namely:
 # Number_of_the_cluster_in_clinical_order coord_x coord_y coord_z
 plugout_drive  $NPB                                               \
 -com 'SWITCH_SESSION A.afni'                       \
 -com 'OPEN_WINDOW A.axialimage geom=600x600+416+44 \
 ifrac=0.8 opacity=5'                         \
 -com 'OPEN_WINDOW A.sagittalimage geom=+45+430     \
 ifrac=0.8 opacity=5'                         \
 -com "SWITCH_UNDERLAY $ct"                         \
 -com "SWITCH_OVERLAY $clustset"                    \
 -com 'SEE_OVERLAY +'                               \
 -com "SET_OUTPLUG $surfcoords"                     \
 -quit
 # suma sends surface object output to a particular file
 # and start talking to afni
 DriveSuma $NPB \
 -com  viewer_cont -key t
 #        set l = `prompt_user -pause 
 ####### START new code for el cluster shading v2.0 (MPBranco 300617)###########################
 sleep 2
 # update coloring to ROI_i256 instead of IsoSurface coloring (which might be the same anyway)
 #  and use copy of cluster niml dset for colors that gets updated below
 DriveSuma $NPB -com surf_cont -load_dset temp_marked_clusters.1D.dset \
 -surf_label $clust_surf
 DriveSuma $NPB -com surf_cont -switch_dset temp_marked_clusters.1D.dset 
 DriveSuma $NPB -com surf_cont -load_cmap tempcmap.niml.cmap
 DriveSuma $NPB -com surf_cont -switch_cmap tempcmap -Dim 0.6 \
 -switch_cmode Dir -1_only Y
 ####### END new code for el cluster shading v2.0 (MPBranco 300617)###########################
```

The electrodes were manually selected using the 3-D clustering image in SUMA. Electrodes were selected individually and in order. SUMA was quit after selection was completed. The following script was used:

```
 ['tcsh -x select_electrode.csh -electrode_i ' num2str(electrode_i) ' -afni_sphere ' afni_sphere]
```

This script contains the following commands for electrode selection:

```
 #get the xyz coordinate in the volume
 # really only need this for the afni_sphere case
 # could be a tiny bit faster without this check most of the time
  plugout_drive  $NPB                                         \
  -com 'GET_DICOM_XYZ'                               \
  -quit
 # have suma report its current surface label - which cluster
 DriveSuma $NPB -com "get_label"
 set clustindex = `tail -2 $sumasurf|head -1` #v2.0. old version=-1 $sumasurf`
 set xyzstr = `tail -1 $surfcoords`
 # output from plugout is of form "RAI xyz: x y z"
 # we can use just part of that
 # if we are using the exact location for a sphere, let's mark that here
 echo $electrode_i $clustindex $xyzstr[3-5] $afni_sphere >> $surfcoords_i
 set clustval = `echo $clustindex | sed  's/roi//' |sed 's/(I,T,B)R=//'|\
         sed 's/(I,T,B)numeric=//'`
 # make 1/3 bright and add it to the list
 # this doesn't change the data in any way here
 # much smaller memory leak, 1000 iterations less that 256MB total for suma
 set roistr = `ccalc -form "roi%3.3d" $clustval`
 # commented lines only useful for checking if roi's have already been recolored
 # for coloring with white, gray or other constant color, skip these lines
 # use grep to be sure this cluster number is legit and to check status
 # don't put any commands beween the grep and status check
 #      grep $roistr temproilist.txt
 # If first time cluster has been identified, recolor to 1/3 brightness
 #  could make else condition, rebrighten electrode
 #      if ($status) then
 set roirgb = `grep $roistr tempcmap.niml.cmap`
 set rgbout =  ("1.0" "1.0" "1.0")         #old version: `1deval -a "1D:$roirgb[1-3]" -expr a/3`
 # change niml file (redirect, then rename rather than in place with "sed -i ..." because of MacOS oddities)
 cat tempcmap.niml.cmap | sed "s/$roirgb/$rgbout 1 $roirgb[5] ${roistr}/" > tempcmap2.niml.cmap
 mv tempcmap2.niml.cmap tempcmap.niml.cmap
 #          DriveSuma $NPB -com surf_cont -switch_dset temp_marked_clusters.1D.dset 
 DriveSuma $NPB -com surf_cont -load_cmap tempcmap.niml.cmap
 #          echo $roistr >> temproilist.txt
 #      endif
```

Electrodes were indexified using the following script:

```
 (['tcsh -x indexify_electrodes.csh ./surf_ixyz.1D 3dclusters_r' num2str(obj.settings.R) '_is' num2str(obj.settings.IS) '_thr' num2str(obj.settings.CV) '.nii'])
```

The script calls the following commands:

```
 setenv AFNI_1D_ZERO_TEXT YES
 set surfcoords_i = $argv[1]
 set clustset = $argv[2]
 # make a smaller dataset that only has the non-zero voxels
 #  for speed. 3dCM and 3dcalc steps below should go faster
 #  make box a little bigger for isosurface to work correctly
 3dAutobox -prefix temp_clusts.nii.gz -noclust -npad 2 -overwrite -input $clustset
 set clustset = temp_clusts.nii.gz
 # name of reordered electrodes
 set eclustset = eclusts+orig
 # name of spheres at electrode positions
 set sclustset = sclusts+orig
 # output centers of mass to 1D text file
 set electrodeCM = electrode_CM.1D
 # spheres of some radius will be put at each center of mass
 set srad = 1.5
 # look around xyz location to find a voxel value
 #  at any particular xyz, might be off because of rounding
 #  or surface node correspondence
 set voxrad = `ccalc '0.5'`
 set elabel = elabels.txt
 # make unique list of electrodes first
 #  we only want the last electrode reported
 set electrodes_list = (`1dcat "${surfcoords_i}[0]" | uniq`)
 # build two corresponding lists
 # list of electrode indices
 set elist = ()
 # list of corresponding indices
 set clist = ()
 # list of required spheres
 set alist = ()
 echo "# x      y     z       electrode  " > $electrodeCM
 echo "" > $elabel
 # at each electrode position, need to update with correct
 #  electrode index
 foreach electrode ($electrodes_list)
 # get the last occurrence of the electrode in i x y z file
 #  look for the electrode i at beginning of line
 #  user may have selected the same electrode multiple times
 #  to correct a previous bad selection
 set xyz = ( `grep "^$electrode " $surfcoords_i| tail -1` )
 # now have suma given cluster index, so don't need to get value at xyz coordinate
 # get closest cluster value around the electrode xyz
 #   don't look far,slightly more than a voxel
 set clustxyzval = `3dmaskave -max -dball $xyz[3] $xyz[4] $xyz[5] $voxrad -quiet $clustset`
 set clustroi = $xyz[2]
 set clustval = `echo $clustroi | sed  's/roi//'`
 set diff = `ccalc -int "equals($clustval,$clustxyzval)"`
 if $diff == '1' then
 echo "Cluster number $clustval does not match value from volume $clustxyzval"
 echo "   Using $clustval as cluster index"
 endif
 if ($clustval != 0) then
 # if user had put 'A' then a sphere will be placed at the exact coordinate
 if ($#xyz == 6) then
 if (($xyz[6] == 'A') || ($xyz[6] == 'a')) then
 set cm = ( $xyz[3-5] )
 # set list to use coordinate directly and put sphere there instead of cluster
 set alist = ( $alist 1 )
 else
 set alist = ( $alist 0 )
 endif
 else
 set cm = `3dCM "${clustset}<$clustval>"`
 set alist = ( $alist 0 )
 endif
 echo  "$cm $electrode" >> $electrodeCM
 set elist = ( $elist $electrode )
 set clist = ( $clist $clustval )
 echo $electrode "Electrode_$electrode" >> $elabel
 else
 echo "No value found at electrode position - $electrode"
 endif
 end
 # put the list of required spheres in a single column
 echo $alist > required_spheres.1D
 # put spheres at each center of mass with electrode index value
 set sbase = `@GetAfniPrefix $sclustset`
 3dUndump -xyz -orient RAI -master $clustset -overwrite -datum byte \
 -srad $srad -prefix $sbase $electrodeCM
 # "atlasize" the sclustset here for labels to show up
 @Atlasize -space ORIG -dset $sclustset \
 -lab_file $elabel 1 0
 # color in AFNI with banded colorscale
 3drefit -cmap INT_CMAP $sclustset
 # now build new reordered cluster dataset with just the electrodes
 #  in the correct order (method suggested by Paul Taylor - thanks!)
 # start with empty dataset
 3dcalc -a $clustset -expr '0' -prefix $eclustset -overwrite
 set n = $#elist
 set ebase = `@GetAfniPrefix $eclustset`
 foreach ei (`count -digits 3 1 $n `)
 # take value from old list and replace with electrode index
 #  from new list, adding each electrode, one at a time to the
 #  same dataset (unless voxel value not already set in output)
 set sreq = $alist[$ei]
 3dcalc -a $clustset -b $eclustset -c $sclustset    \
 -expr "(b + $elist[$ei]*equals(a,$clist[$ei])*not(b)*not($sreq)) \
 +c*(equals($elist[$ei],c)*step($sreq))"  \
 -prefix $ebase -overwrite
 end
 # color in AFNI with banded colorscale
 3drefit -cmap INT_CMAP $eclustset
 # "atlasize" the eclust dataset too here for labels to show up
 @Atlasize -space ORIG -dset $eclustset -lab_file $elabel 1 0
```

**STEP 3: Electrode Projection**

The log file from the third step does not contain the called commands, the list below has been extracted from the Matlab file runMethod1.m. "Method 1" (Hermes et. al 2010), the subject name "YBK" and the hemisphere "right" were selected in the GUI. The grid settings were then manually created consisting of a label "G", the desired electrodes from the previous selection in step 2 "[1:32]", and grid dimensions "4,8".

The script calls the following commands: (Note that these commands are directly from the MATLAB script, as no .csh file exists for it)

```
 %% NOTES;
 % This script uses freesurfer surface with electrode position extracted from 
 % high res CT 3dclusters (using ctmr scirpt from Dora).
 %% 1.1) generate surface to project electrodes to
 hemisphere = obj.settings.Hemisphere;
 if strcmp(hemisphere, 'Left')
 hemi = 'l';
 else
 hemi = 'r';
 end
 if exist(['./results/' subject '_balloon_11_03.img'])==0
 % if using freesurfer:
 get_mask_from_FreeSurfer(subject,... % subject name
 './data/FreeSurfer/t1_class.nii',... % freesurfer class file
 './results/',... % where you want to safe the file
 hemi,... % 'l' for left 'r' for right
 11,0.3); % settings for smoothing and threshold
 %Visualize the surface with afni or mricron
 %saved as subject_balloon_11_03, where 11 and 0.3 are the chosen parameters.
 end
 %% 1.2) Convert DICOM to NIFTI + Coregistration + 3dClustering + electrode selection and sorting
 % coregister CT to anatomical MR using Afni and preserving CT resolution.
 % extract electrodes clusters using 3D clustering
 % extract CM using AFNI-SUMA plug-in.
 CM = importdata('./data/3Dclustering/electrode_CM.1D');
 %remove repeated electrodes.
 [~, index] = unique(CM.data(:,4), 'last');
 CM = CM.data(index,[1:4]);
 elecCoord = [-CM(:,1:2) CM(:,3)];
 elecNum    = CM(:,4);
 %check for empty rows and put NANs
 elecmatrix = zeros(elecNum(end),3); % create empty array 
 auxk = 2;
 elecmatrix(1,:) = elecCoord(1,:);
 for k=2:length(elecNum)
 if elecNum(k)-elecNum(k-1)~= 1
 elecmatrix(elecNum(k-1)+1:elecNum(k)-1,:) = nan;
 auxk = elecNum(k);
 elecmatrix(auxk,:) = elecCoord(k,:);
 auxk = auxk+1;
 else
 elecmatrix(auxk,:) = elecCoord(k,:);
 auxk = auxk +1;
 end
 end
 save([mypath 'CM_electrodes_sorted_all.mat'],'elecmatrix');
 %% 4) Tansform coordinates to subject ANAT space:
 load([mypath 'CM_electrodes_sorted_all.mat']);
 Tmatrix = dlmread('./data/coregistration/CT_highresRAI_res_shft_al_mat.aff12.1D');
 Tmatrix2 = dlmread('./data/coregistration/CT_highresRAI_shft.1D');
 T = [reshape(Tmatrix',4,3)  [0 0 0 1]']';
 T2 = [reshape(Tmatrix2',4,3)  [0 0 0 1]']';
 T3 = T2*T;
 coord_al_anatSPM = [];
 coord_al_anat = [];
 for i = 1:size(elecmatrix,1)
 coord = [-elecmatrix(i,1:2) elecmatrix(i,3) 1];
 coord_al_anat(i,:) = T3\coord' ; % = inv(T)*coord'
 coord_al_anatSPM(i,:) = [-coord_al_anat(i,1:2) coord_al_anat(i,3)]; 
 end
 %%%%%%% SPM alignement:
 % T = [0.9979    0.0622    0.0154  -13.5301;...
 %   -0.0629    0.9971    0.0428   -7.2991;...
 %   -0.0127   -0.0437    0.9990  -19.1397;...
 %         0         0         0    1.0000];
 %
 %coord_al_anatSPM = [];
 %
 %for i = 1:size(elecmatrix,1)  
 %  coord = [elecmatrix(i,1:3) 1]; %spm mode
 %  coord_al_anatSPM(i,:) = inv(T)*coord' ;  
 %end
 %%%%%%%%%%%%%%%%%
 % check result:
 % figure,
 % plot3(coord_al_anatSPM(:,1),coord_al_anatSPM(:,2),coord_al_anatSPM(:,3),'.','MarkerSize',20); hold on;
 % plot3(elecmatrix(:,1),elecmatrix(:,2),elecmatrix(:,3),'.r','MarkerSize',20); legend('aligned');
 elecmatrix = coord_al_anatSPM(:,1:3);
 save([mypath 'CM_electrodes_sorted_all_aligned.mat'],'elecmatrix');
 %% 5) project electrodes 2 surface
 system(['rm ./results/' subject '_singleGrid*']);
 load([mypath 'CM_electrodes_sorted_all_aligned.mat']);
 % electrodes2surf(subject,localnorm index,do not project electrodes closer than 3 mm to surface)
 % electrodes are projected per grid with electrodes2surf.m
 % in this example there were 7 grids
 % electrodes2surf(
 % 1: subject
 % 2: number of electrodes local norm for projection (0 = whole grid)
 % 3: 0 = project all electrodes, 1 = only project electrodes > 3 mm
 %    from surface, 2 = only map to closest point (for strips)
 % 4: electrode numbers
 % 5: (optional) electrode matrix.mat (if not given, SPM_select popup)
 % 6: (optional) surface.img (if not given, SPM_select popup)
 % 7: (optional) mr.img for same image space with electrode
 %    positions
 % automatically saves:
 %       a matrix with projected electrode positions 
 %       a nifti image with projected electrodes
 % saved as electrodes_onsurface_filenumber_inputnr2
 electrodes_path = [mypath 'CM_electrodes_sorted_all_aligned.mat'];
 surface_path = [mypath subject '_balloon_11_03.img'];
 anatomy_path = './data/FreeSurfer/t1_class.nii';
 for g=1:size(obj.settings.Grids,2)
 grid = obj.settings.Grids{g};
 %find comas:
 comas = strfind(grid,',');   
 gridLabel = grid(1:comas(1)-1);
 gridEls   = str2num(grid(comas(1)+1:comas(2)-1));
 gridSize  = str2num(grid(comas(2)+1:end));
 if min(gridSize)==1
 %strip
 parm(1) = 0;
 parm(2) = 2;
 elseif min(gridSize)==2
 %small grid 2xN
 parm(1) = 4;
 parm(2) = 1;
 elseif min(gridSize)>2
 %big grids: 3xN, 4xN, 6xN, 8xN
 parm(1) = 5;
 parm(2) = 1;
 else
 disp('! WARNING: Grid cannot have dimension 0. Please add grid again.');
 %log
 str = get(obj.controls.txtLog, 'string');
 if length(str)>=obj.settings.NUM_LINES
 str = str( (end - (obj.settings.NUM_LINES-1)) :end);
 end
 set(obj.controls.txtLog, 'string',{str{:},'>! WARNING: Grid cannot have dimension 0. Please add grid again.'});
 loggingActions(obj.settings.currdir,3,' >! WARNING: Grid cannot have dimension 0. Please add grid again.');        
 end
 try
 [out_els,out_els_ind]=electrodes2surf_FreeSurfer(subject,parm(1),parm(2),gridEls,electrodes_path, surface_path, anatomy_path, mypath);
 catch
 parm(2) = 2;
 [out_els,out_els_ind]=electrodes2surf_FreeSurfer(subject,parm(1),parm(2),gridEls,electrodes_path, surface_path, anatomy_path, mypath);
 end
 elecmatrix(gridEls,:) = out_els;
 end
 %save as subject_singleGrid_projectedElectrodes_FreeSurfer_X_parm1_parm2,
 %where X is the number of the generated file (1 for the first file with
 %parameters X, Y and 2 for second file with same parameters),
 %and parm1 and parm2 the 2nd and 3rd of the projection function.
 %% 6) combine electrode files into one 
 % save all projected electrode locaions in a .mat file
 save([mypath subject '_projectedElectrodes_FreeSurfer_3dclust.mat'],'elecmatrix');
 % make a NIFTI image with all projected electrodes
 [output,els,els_ind,outputStruct]=...
 position2reslicedImage2(elecmatrix,anatomy_path);
 for filenummer=1:100
 outputStruct.fname=[mypath subject '_projectedElectrodes_FreeSurfer_3dclust' int2str(filenummer) '.img' ];
 if ~exist(outputStruct.fname,'file')>0
 disp(['saving ' outputStruct.fname]);
 % save the data
 spm_write_vol(outputStruct,output);
 break
 end
 end
 %% 7) generate cortex to render images:
 hemisphere = obj.settings.Hemisphere;
 if strcmp(hemisphere, 'Left')
 % from freesurfer: in mrdata/.../freesurfer/mri
 gen_cortex_click_from_FreeSurfer(anatomy_path,[subject '_L'],0.5,[15 3],'l',mypath);
 display_view = [270 0];
 % load cortex
 load([mypath subject '_L_cortex.mat']);
 save([mypath '/projected_electrodes_coord/' subject '_L_cortex.mat'],'cortex');  
 elseif strcmp(hemisphere, 'Right')
 % from freesurfer: in mrdata/.../freesurfer/mri
 gen_cortex_click_from_FreeSurfer(anatomy_path,[subject '_R'],0.5,[15 3],'r',mypath);
 display_view = [90 0];
 % load cortex
 load([mypath subject '_R_cortex.mat']);
 save([mypath '/projected_electrodes_coord/' subject '_R_cortex.mat'],'cortex');
 end
 %% 8) plot electrodes on surface
 % load electrodes on surface
 load([mypath subject '_projectedElectrodes_FreeSurfer_3dclust.mat']);
 % save final folder
 save([mypath '/projected_electrodes_coord/' subject '_projectedElectrodes_FreeSurfer_3dclust.mat'],'elecmatrix')
 ctmr_gauss_plot(cortex,[0 0 0],0);
 el_add(elecmatrix,'r',20);
 label_add(elecmatrix)
 loc_view(display_view(1), display_view(2));
```

A number of MATLAB scripts were also used in the process of running the Hermes Method. The .m file names are the following and located under the folder "Hermes2009":

```
 ctmr_guass_plot.m
 ell_add_withr2.m
 el_add.m
 electrodes2surf_FreeSurfer.m
 gen_cortex_click_from_FreeSurfer.m
 get_mask_from_FreeSurfer.m
 getCursorinfo.m
 hollow_brain.m
 label_add.m
 loc_view.m
 p_zoom.m
 position2reslicedImage2.m
 sm_filt.m
 tripatch.m
```

Some other MATLAB scripts used were:

```
 runHD.m
 NeuralAct package
```
