# InflationMovies

> **Navigation:** [Home](index.md) | [Publications](Publications.md) | [Resources](DataSharing.md)

## Making Movies of the Inflation Process

Let's make a movie of inflation
quit and restart X11 after every movie made because of memory bugs

```
 cd /Volumes/data9/surfaces/brown_katie/GW/SUMA
 set ec = GW
 suma -niml -spec {$ec}_lh.spec &
```

1. set up view; load nice color map; then press "R" to record all images; note that initial view must be smoothwm

```
 set sd = /Volumes/data9/surfaces/scripts/
 DriveSuma -com surf_cont -load_dset lh.sulc.asc -I_sb 4 -surf_label lh.smoothwm.asc  -view_surf_cont y -load_cmap {$sd}/nice.1D.cmap -Dim 0.6
 DriveSuma -com viewer_cont -key b  -1_only n
 rm junk.ply
 SurfSmooth -spec {$ec}_lh.spec -surf_A lh.smoothwm.asc -met NN_geom \
 -surf_out junk.ply -Niter 500 -match_area 0.01 -talk_suma
```

saved as Infl\_sm\_500.mpg
for display, I wonder if we can inflate the folded brain---
also, this is a bit too slow
only use every 10th frame, also cut out last two (when it expands it greatly)

```
 rm junk.ply
 SurfSmooth -spec {$ec}_lh.spec -surf_A lh.pial.asc -met NN_geom \
 -surf_out junk.ply -Niter 500 -match_area 0.01 -talk_suma  -send_kth 10
```

saved as Infl\_pial\_500.mpg

go all the way

```
 rm junk.ply
 SurfSmooth -spec {$ec}_lh.spec -surf_A lh.pial.asc -met NN_geom \
 -surf_out junk.ply -Niter 2500 -match_area 0.01 -talk_suma  -send_kth 20
```

can we rotate the brain while inflating?? Yes!

```
 rm junk.ply
 SurfSmooth -spec {$ec}_lh.spec -surf_A lh.pial.asc -met NN_geom \
 -surf_out junk.ply -Niter 1750 -match_area 0.01 -talk_suma  -send_kth 5
```

18 to 355
this is with 5 degree step

```
 setenv SUMA_ArrowRotAngle 1
```

for smoother rotation

```
 SurfSmooth -spec {$ec}_lh.spec -surf_A lh.pial.asc -met NN_geom \
 -surf_out junk.ply -Niter 1750 -match_area 0.01 -talk_suma  -send_kth 1
```

this is like super slo mo

```
 setenv SUMA_ArrowRotAngle 3
 rm junk.ply
 SurfSmooth -spec {$ec}_lh.spec -surf_A lh.pial.asc -met NN_geom \
 -surf_out junk.ply -Niter 1750 -match_area 0.01 -talk_suma  -send_kth 4
```
