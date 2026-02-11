# AutomatingAFNI

> **Navigation:** [Home](index.md) • [Publications](Publications.md) • [Resources](DataSharing.md)

Many times it is useful to automate AFNI and SUMA. For instance, if you have scanned 20 subjects and would like to print out the results of your analysis for each one without having to manually set the viewer settings for each subjects.
For AFNI, the program to use is plugout\_drive. Here are some sample commands to load AFNI and set the viewer settings. It is good to wait for AFNI to load before sending commands, hence the "sleep" command.

```
 echo "wait 10 seconds"                             \
 sleep 10                                           \
 plugout_drive  -com 'SWITCH_UNDERLAY anatavg'      \
              -com 'SWITCH_OVERLAY stats.PL_MoEy' \
              -quit          
 plugout_drive  -com 'SET_FUNCTION stats.PL_MoEy[0 11 0]'  -quit
 plugout_drive  -com 'SET_THRESHOLD A.5000 1'  -quit
 plugout_drive  -com 'SET_PBAR_ALL A.-7 40.0=yellow 26.4=oran-yell 13.2=oran-red 2.0=green -2.0=blue -13.2=lt-blue1 -26.4=lt-blue2 -40=blue-cyan' -quit
 plugout_drive  -com 'SET_FUNC_RANGE 1'  -quit
```

For SUMA, the program to use is DriveSuma. After the functionals are setup correctly in AFNI, we can tell SUMA to automatically save the images that we want.
Using the Ctrl-R command, each viewer change automatically saves a new JPG into the "SUMA\_Recordings" directory.

```
 echo Save lateral view pictures  
 DriveSuma -com viewer_cont -key ctrl+R -key ctrl+right -key ctrl+left -key ctrl+R
```

We can also combine this with the mv command to rename them properly

```
 echo Save medial view pictures by turning off each hemisphere. Turn off left hemisphere first  
 DriveSuma -com viewer_cont -key [
 DriveSuma -com viewer_cont -key ctrl+R -key ctrl+left -key ctrl+R
```
