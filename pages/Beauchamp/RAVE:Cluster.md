---
layout: default
title: "Cluster"
parent: Beauchamp
---

# Cluster

|  |  |
| --- | --- |
|  | Beauchamp Lab wiki |

* [Home](index.md "Beauchamp")
* [Publications](Publications.md "Beauchamp:Publications")
* [Resources](DataSharing.md "Beauchamp:DataSharing")

|  |
| --- |
| RAVE  RAVE Logo   R Analysis and Visualization of intracranial EEG Data (RAVE) is a powerful software tool for the analysis of intracranial electroencephalogram (iEEG) data, including data collected using strips and grids (ECoG) and depth electrodes (stereo EEG). Funding provided by NIH 1R24MH117529-01. Using RAVE on the BCM Cluster The first step is to request a login ID and password from the BCM Cluster administer. The username will be your BCM username but the password will be different and must be reset. Login to the cluster from a terminal window on your iMac   ``` ssh beaucham@chemo.dldcc.bcm.edu Load the required modules for RAVE module load R module load hdf5 module load fftw Check what the IP address will be  ifconfig ```   e.g.   ``` eth3     inet addr:10.22.223.200  Bcast:10.22.223.255  Mask:255.255.252.0 ```   tells you that IP address will start with 10.22.223.200  Start R and launch RAVE   ``` R -e "rave::init_app(host='10.22.223.200')" ```   this should tell you what IP and port to use, e.g.   ```  Now listening on X:Y ```   On your local machine, point your browser to this address   ```  http:\\10.22.223.200:XXXX ```   If needed, copy data to the cluster   ``` cd /Volumes/Data/data/rave_data/raw  sftp beaucham@chemo.dldcc.bcm.edu cd /projects/camri put YAB.zup ```   Before starting R, you can request more resources   ``` qsub -I  -l vmem=200GB ```   To kill a job, use   ``` qdel <jobid> ```   Use ps to determine the jobid.  For initial setup, must make the raw directory   ``` mkdir /project/camri/raw chmod -R 777 /project/camri/raw mkdir /project/camri/data chmod -R 777 /project/camri/data ```   And tell RAVE where they are   ``` rave::rave_options(raw_data_dir = '/project/camri/raw') rave::rave_options(data_dir = '/project/camri/data') ```  Launching RAVE on BCM Cluster from OSX First install XQuartz if not installed   ``` https://www.xquartz.org/ ```   Next, on the local machine, open terminal, type   ``` echo $DISPLAY ```   If nothing returns, run   ``` dispdir=`dirname $DISPLAY` dispfile=`basename $DISPLAY` dispnew="$dispdir/:0" if [ -e $DISPLAY -a "$dispfile" = "org.x:0" ]; then   mv $DISPLAY $dispnew fi export DISPLAY=$dispnew ```   Then open or create a new file at   ``` ~/.ssh/config ```   Insert/edit the following lines:   ``` Host *     ForwardAgent yes     ForwardX11 yes     XAuthLocation /opt/X11/bin/xauth ```   Save and exit. Also exit terminal.  Open another terminal, test again   ``` echo $DISPLAY ```   It should print out result similar to   ``` /private/tmp/com.apple.launchd.q16FRU1JYw/org.macosforge.xquartz:0 ```   Connect to server   ``` ssh -Y beaucham@chemo.dldcc.bcm.edu ```   Test firefox   ``` firefox ```   (TODO write sh script to launch rave in qsub and port forward) |
