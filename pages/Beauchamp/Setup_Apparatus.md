# Setup Apparatus

> **Navigation:** [Home](index.md) • [Publications](Publications.md) • [Resources](DataSharing.md)

|  |  |
| --- | --- |
|  | Beauchamp Lab wiki |

- [Home](index.md "Beauchamp")
- [Publications](Publications.md "Beauchamp:Publications")
- [Resources](DataSharing.md "Beauchamp:DataSharing")

## Electrophysiology Set Up Procedure

**Day 0 - electrode implantation**

1. Set up cabling for ITC to record from 16 channels (unplug channel 1 to test stimulation circuit).   
2. Using the oscilloscope, check TTL pulse for gate and monitor out signal with stimulation circuit online.  
3. Pick up CT scan from radiology library (signed HIPAA release required) after surgery (~11AM).  
4. Merge 2nd structural MRI with CT on Stealth.  
5. Merge 2nd structural MRI with CT on AFNI and view with functional activation on cortical surface to select candidate electrodes.  
6. Have Lisa or Rodney (our friendly neighborhood EMU techs) jumper the candidate electrodes from the jackbox to our amplifiers.  
7. Double check that the jumpered electrodes are the ones we want.  
8. Make sure cart, display, and eye tracker are room-ready.  
9. Have tape measure, several surgical grounding pads available.  
*If microstimulating:*  
1. Check batteries on BAK stimulator, and change if reading lower than 115V (reads ~ 135V with brand new complement of batteries). Be very careful not to yank internal wires.  
2. Check batteries on patient interface, and change if reading lower than 18V (reads ~ 27V with brand new complement of batteries).

**Experiment Day Setup**   
1. Have Lisa or Rodney place reference (on the scalp) and ground electrodes.   
2. Turn on our two amplifiers in the equipment closet in the EMU.  
3. Check for good signals on all 16 channels. If there is 60 Hz noise on all channels, consider relocating either the reference, ground, or both. Fresh reference/ground electrodes and/or reapplication of the electrode gel may be required from day to day, as they seem to wear overnight. Other sites of signal corruption may be the jumpered cables (which might have loosened overnight or the cabling in the closet that connects the amplified signal to the control computer.  
4. Turn on KNOT.  
5. RTA: Make sure electrode names are correctly entered in Knot's files, to make it easier to retrieve electrode names during data analysis. If electrodes are switched out or if electrode assignments flip, make sure to change electrode names to coincide with the changes.   
5. Set up display cart and [eye tracker](Eye_Tracker.md).  
6. Run [Experimental Protocol](Electrophysiology.md "Beauchamp:Electrophysiology")  
7. [Shut Down](Shut_Down_Apparatus.md).
