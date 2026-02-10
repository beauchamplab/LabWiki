# RealTimefMRI

> **Navigation:** [Home](index.md) | [Publications](Publications.md) | [Resources](DataSharing.md)

Real Time Notes

See case ZAE Notes files for an example of pseudo-real time fMRI

1. !/bin/tcsh

rtfeedme \

```
 -drive 'DRIVE_AFNI OPEN_WINDOW axialimage geom=285x285+3+533'               \
 -drive 'DRIVE_AFNI OPEN_WINDOW coronalimage geom=421x192+283+534 mont=2x3:2'\
 -drive 'DRIVE_AFNI OPEN_WINDOW coronalgraph geom=570x440+868+47 keypress=A' \
 -drive 'DRIVE_AFNI SET_SUBBRICKS 0 1 1'                 \
 -drive 'DRIVE_AFNI SET_DICOM_XYZ 38 42 35'              \
 -drive 'DRIVE_AFNI SET_THRESHNEW 0.4'                   \
 -dt 100 -3D blur_vr_run1_motor_AFB003+orig
```

1. !/bin/tcsh

last\_file = ""
while ( 1 )

```
   if ( -f last.par.file ) then
       last_file = `cat last.par.file`
   endif
```

```
   pfile = `\ls -1tr *.PAR | tail -1`
```

```
   if ( $pfile != $last_file ) then    # process a new dataset
       set prefix = $pfile:r
       3dPAR2AFNI.pl $pfile
       echo $pfile > last.par.file
       if ( -f $prefix+orig.HEAD ) then
           rtfeedme -drive "DRIVE_AFNI OPENWINDOW axialimage ..." -quit
       else
           echo "** failed to convert PAR/REC dataset $pfile"
       endif
   endif
   sleep 5
```

end
